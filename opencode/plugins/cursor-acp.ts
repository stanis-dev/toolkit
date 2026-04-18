import { execFileSync, spawn } from "node:child_process"
import { existsSync } from "node:fs"
import { homedir } from "node:os"
import { isAbsolute, join, resolve } from "node:path"

const PROVIDER_ID = "cursor-acp"
const SERVICE_NAME = "toolkit-cursor-acp"
const PROXY_HOST = "127.0.0.1"
const MODEL_CACHE_TTL_MS = 5 * 60 * 1000
const AUTH_POLL_INTERVAL_MS = 1000
const AUTH_POLL_TIMEOUT_MS = 5 * 60 * 1000
const LOGIN_URL_TIMEOUT_MS = 10000

const ANSI_REGEX = /[\u001B\u009B][[\]()#;?]*(?:(?:(?:[a-zA-Z\d]*(?:;[a-zA-Z\d]*)*)?\u0007)|(?:(?:\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-nq-uy=><~]))/g
const LOGIN_URL_REGEX = /https:\/\/cursor\.com\/loginDeepControl\S*/

const ARG_KEY_GROUPS = [
  ["path", ["path", "filePath", "filepath", "file", "targetPath", "targetpath", "directory", "dir", "folder", "targetDirectory", "targetdirectory", "targetFile", "targetfile"]],
  ["pattern", ["pattern", "globPattern", "globpattern", "filePattern", "filepattern", "searchPattern", "searchpattern"]],
  ["include", ["include", "includePattern", "includepattern"]],
  ["cwd", ["cwd", "workingDirectory", "workingdirectory", "workdir", "currentDirectory", "currentdirectory"]],
  ["command", ["command", "cmd", "script", "shellCommand", "shellcommand", "terminalCommand", "terminalcommand"]],
  ["content", ["content", "contents", "text", "body", "data", "payload", "streamContent", "streamcontent"]],
  ["old_string", ["old_string", "oldString", "oldstring"]],
  ["new_string", ["new_string", "newString", "newstring"]],
  ["force", ["force", "recursive"]],
] as const

const TOOL_NAME_ALIASES = new Map<string, string>([
  ["shell", "bash"],
  ["shellcommand", "bash"],
  ["terminal", "bash"],
  ["terminalcommand", "bash"],
  ["runcommand", "bash"],
  ["executecommand", "bash"],
  ["readfile", "read"],
  ["fileread", "read"],
  ["findfiles", "glob"],
  ["searchfiles", "glob"],
  ["globfiles", "glob"],
  ["listdir", "list"],
  ["listdirectory", "list"],
  ["listfiles", "list"],
  ["ls", "list"],
  ["createdirectory", "mkdir"],
  ["makedirectory", "mkdir"],
  ["mkdirp", "mkdir"],
  ["createdir", "mkdir"],
  ["delete", "rm"],
  ["deletefile", "rm"],
  ["deletedirectory", "rm"],
  ["remove", "rm"],
  ["unlink", "rm"],
  ["rmdir", "rm"],
  ["getfileinfo", "stat"],
  ["fileinfo", "stat"],
  ["filestat", "stat"],
  ["pathinfo", "stat"],
  ["editfile", "edit"],
  ["multiedit", "edit"],
  ["writefile", "write"],
  ["updatetodos", "todowrite"],
  ["writetodos", "todowrite"],
  ["askuser", "question"],
  ["promptuser", "question"],
  ["fetchurl", "webfetch"],
  ["useskill", "skill"],
  ["runskill", "skill"],
  ["invokeskill", "skill"],
  ["subagent", "task"],
  ["delegatetask", "task"],
  ["delegate", "task"],
])

const FALLBACK_MODELS = [
  { id: "auto", name: "Auto" },
  { id: "composer-2-fast", name: "Composer 2 Fast" },
  { id: "composer-2", name: "Composer 2" },
  { id: "composer-1.5", name: "Composer 1.5" },
  { id: "gpt-5.4-medium", name: "GPT-5.4 1M" },
  { id: "gpt-5.3-codex", name: "Codex 5.3" },
  { id: "gpt-5.2", name: "GPT-5.2" },
  { id: "claude-4.6-sonnet-medium", name: "Sonnet 4.6 1M" },
  { id: "claude-4.5-sonnet", name: "Sonnet 4.5 1M" },
  { id: "claude-4.5-sonnet-thinking", name: "Sonnet 4.5 1M Thinking" },
  { id: "gemini-3.1-pro", name: "Gemini 3.1 Pro" },
  { id: "kimi-k2.5", name: "Kimi K2.5" },
] as const

type JsonRecord = Record<string, unknown>
type CursorModelInfo = { id: string; name: string }
type ProxyState = { workspaceDirectory: string; baseURL: string; server: any }
type ParsedChatBody = {
  model: string
  originalModel: string
  stream: boolean
  prompt: string
  messages: unknown[]
  tools: unknown[]
}

type StreamState = {
  assistantText: string
  reasoningText: string
  sawAssistantPartials: boolean
  sawThinkingPartials: boolean
}

type ToolCall = {
  id: string
  type: "function"
  function: {
    name: string
    arguments: string
  }
}

type ExtractedToolCall = {
  toolCall: ToolCall | null
  matchedToolName: string | null
}

let modelCache: { timestamp: number; models: CursorModelInfo[] } | null = null

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value)
}

function stripAnsi(value: string): string {
  return value.replace(ANSI_REGEX, "")
}

function isMeaningfulValue(value: unknown): boolean {
  return value !== undefined && !(typeof value === "string" && value.trim().length === 0)
}

function sanitizeToolCallID(value: string): string {
  const sanitized = value.trim().replace(/\s+/g, "_").replace(/[^a-zA-Z0-9._:-]/g, "_")
  return sanitized.length > 0 ? sanitized : `tool_${Date.now()}`
}

function normalizeToken(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]/g, "")
}

function normalizeWorkspacePath(pathValue: string): string {
  const resolved = resolve(pathValue)
  return process.platform === "darwin" ? resolved.toLowerCase() : resolved
}

function getServerRegistry(): Map<string, ProxyState> {
  const globalKey = "__toolkit_cursor_acp_server_registry__"
  const globalState = globalThis as Record<string, unknown>
  const existing = globalState[globalKey]
  if (existing instanceof Map) {
    return existing as Map<string, ProxyState>
  }
  const registry = new Map<string, ProxyState>()
  globalState[globalKey] = registry
  return registry
}

async function log(client: any, level: "debug" | "info" | "warn" | "error", message: string, extra?: JsonRecord) {
  try {
    await client?.app?.log?.({
      body: {
        service: SERVICE_NAME,
        level,
        message,
        extra,
      },
    })
  } catch {
    // Ignore logging failures.
  }
}

function extractTextFromContent(content: unknown): string {
  if (typeof content === "string") {
    return content
  }
  if (!Array.isArray(content)) {
    return ""
  }
  return content
    .map((part) => {
      if (isRecord(part) && part.type === "text" && typeof part.text === "string") {
        return part.text
      }
      return ""
    })
    .filter(Boolean)
    .join("\n")
}

function buildPromptFromMessages(messages: unknown[], tools: unknown[]): string {
  const lines: string[] = []

  let hasToolResults = false

  for (const rawMessage of messages) {
    const message = isRecord(rawMessage) ? rawMessage : null
    if (!message) continue

    const role = typeof message.role === "string" ? message.role : "user"

    if (role === "tool") {
      hasToolResults = true
      const toolCallId = typeof message.tool_call_id === "string" ? message.tool_call_id : "unknown"
      const body = extractTextFromContent(message.content)
      lines.push(`TOOL_RESULT (call_id: ${toolCallId}): ${body}`)
      continue
    }

    if (role === "system") {
      if (tools.length > 0) {
        continue
      }
      const text = extractTextFromContent(message.content)
      if (text.length > 0) {
        lines.push(`SYSTEM: ${text}`)
      }
      continue
    }

    if (role === "assistant" && Array.isArray(message.tool_calls) && message.tool_calls.length > 0) {
      const content = extractTextFromContent(message.content)
      const calls = message.tool_calls
        .map((entry) => {
          if (!isRecord(entry)) return ""
          const fn = isRecord(entry.function) ? entry.function : {}
          const id = typeof entry.id === "string" ? entry.id : "?"
          const name = typeof fn.name === "string" ? fn.name : "?"
          const args = typeof fn.arguments === "string" ? fn.arguments : "{}"
          return `tool_call(id: ${id}, name: ${name}, args: ${args})`
        })
        .filter(Boolean)
      if (content.length > 0) {
        lines.push(`ASSISTANT_TEXT_BEFORE_TOOL_CALLS: ${content}`)
      }
      lines.push(`ASSISTANT_TOOL_CALLS:\n${calls.join("\n")}`)
      continue
    }

    const text = extractTextFromContent(message.content)
    if (text.length > 0) {
      lines.push(`${role.toUpperCase()}: ${text}`)
    }
  }

  if (hasToolResults) {
    lines.push("The tool calls above have already been executed. Use their results and continue the task.")
  }

  return lines.join("\n\n")
}

function extractAssistantText(event: JsonRecord): string {
  if (!isRecord(event.message) || !Array.isArray(event.message.content)) {
    return ""
  }
  return event.message.content
    .map((part) => {
      if (isRecord(part) && part.type === "text" && typeof part.text === "string") {
        return part.text
      }
      return ""
    })
    .filter(Boolean)
    .join("")
}

function extractThinkingText(event: JsonRecord): string {
  if (event.type === "thinking") {
    return typeof event.text === "string" ? event.text : ""
  }

  if (!isRecord(event.message) || !Array.isArray(event.message.content)) {
    return ""
  }

  return event.message.content
    .map((part) => {
      if (isRecord(part) && part.type === "thinking" && typeof part.thinking === "string") {
        return part.thinking
      }
      return ""
    })
    .filter(Boolean)
    .join("")
}

function updateStreamState(state: StreamState, event: JsonRecord) {
  if (event.type === "assistant") {
    const text = extractAssistantText(event)
    if (text.length === 0) return
    const isPartial = typeof event.timestamp_ms === "number"
    if (isPartial) {
      state.sawAssistantPartials = true
      state.assistantText += text
      return
    }
    if (!state.sawAssistantPartials) {
      state.assistantText = text
    }
    return
  }

  if (event.type !== "thinking" && event.type !== "assistant") {
    return
  }

  const text = extractThinkingText(event)
  if (text.length === 0) return
  const isPartial = typeof event.timestamp_ms === "number"
  if (isPartial) {
    state.sawThinkingPartials = true
    state.reasoningText += text
    return
  }
  if (!state.sawThinkingPartials) {
    state.reasoningText = text
  }
}

function parseJsonLine(line: string): JsonRecord | null {
  if (line.trim().length === 0) return null
  try {
    const parsed = JSON.parse(line)
    return isRecord(parsed) ? parsed : null
  } catch {
    return null
  }
}

function normalizeRuntimeModel(rawModel: unknown): string {
  const raw = typeof rawModel === "string" ? rawModel.trim() : ""
  if (raw.length === 0) return "auto"
  const prefix = `${PROVIDER_ID}/`
  return raw.startsWith(prefix) ? raw.slice(prefix.length) : raw
}

function normalizeTaskSubagentType(value: unknown): string | null {
  if (typeof value === "string") {
    const normalized = normalizeToken(value)
    if (normalized.length === 0 || normalized.includes("unspecified") || normalized.includes("default") || normalized === "general") {
      return "general"
    }
    if (normalized === "explore" || normalized.includes("codeexplorer") || normalized.includes("explore") || normalized.includes("search")) {
      return "explore"
    }
    return null
  }

  if (!isRecord(value)) {
    return null
  }

  if (typeof value.name === "string") {
    return normalizeTaskSubagentType(value.name)
  }

  if (isRecord(value.custom) && typeof value.custom.name === "string") {
    return normalizeTaskSubagentType(value.custom.name)
  }

  const [firstKey] = Object.keys(value)
  return firstKey ? normalizeTaskSubagentType(firstKey) : null
}

function parseCursorModelsOutput(rawOutput: string): CursorModelInfo[] {
  const clean = stripAnsi(rawOutput)
  const lines = clean.split(/\r?\n/)
  const models: CursorModelInfo[] = []
  let seenHeader = false

  for (const rawLine of lines) {
    const line = rawLine.trim()
    if (line.length === 0) continue

    if (!seenHeader) {
      if (line.toLowerCase() === "available models") {
        seenHeader = true
      }
      continue
    }

    if (line.startsWith("Tip:")) {
      break
    }

    const match = line.match(/^([^\s]+)\s+-\s+(.+?)(?:\s+\((?:current|default)\))?$/)
    if (!match) continue

    models.push({
      id: match[1].trim(),
      name: match[2].trim(),
    })
  }

  return models
}

function discoverCursorModels(): CursorModelInfo[] {
  if (modelCache && Date.now() - modelCache.timestamp < MODEL_CACHE_TTL_MS) {
    return modelCache.models
  }

  try {
    const raw = execFileSync("cursor-agent", ["models"], {
      encoding: "utf8",
      timeout: 30000,
    })
    const models = parseCursorModelsOutput(raw)
    if (models.length > 0) {
      modelCache = { timestamp: Date.now(), models }
      return models
    }
  } catch {
    // Fall through to the fallback list.
  }

  const fallback = FALLBACK_MODELS.map((entry) => ({ ...entry }))
  modelCache = { timestamp: Date.now(), models: fallback }
  return fallback
}

function buildProviderModelMap(models: CursorModelInfo[]): Record<string, { name: string }> {
  const entries: Record<string, { name: string }> = {}
  for (const model of models) {
    entries[model.id] = { name: model.name }
  }
  return entries
}

function removeDisabledProvider(config: JsonRecord) {
  if (!Array.isArray(config.disabled_providers)) return
  config.disabled_providers = config.disabled_providers.filter((value) => value !== PROVIDER_ID)
}

function ensureCursorProvider(config: JsonRecord, baseURL: string) {
  const provider = isRecord(config.provider) ? config.provider : {}
  if (!isRecord(config.provider)) {
    config.provider = provider
  }

  const existing = isRecord(provider[PROVIDER_ID]) ? provider[PROVIDER_ID] : {}
  provider[PROVIDER_ID] = existing

  existing.npm = "@ai-sdk/openai-compatible"
  existing.name = typeof existing.name === "string" && existing.name.trim().length > 0 ? existing.name : "Cursor ACP"

  const options = isRecord(existing.options) ? existing.options : {}
  existing.options = options
  options.baseURL = baseURL
  if (typeof options.apiKey !== "string" || options.apiKey.trim().length === 0) {
    options.apiKey = "cursor-agent"
  }

  existing.models = buildProviderModelMap(discoverCursorModels())
}

function isCursorProviderModel(model: unknown): boolean {
  if (!isRecord(model)) return false

  const providerID = typeof model.providerID === "string"
    ? model.providerID
    : typeof model.providerId === "string"
      ? model.providerId
      : typeof model.provider === "string"
        ? model.provider
        : ""

  if (providerID === PROVIDER_ID) {
    return true
  }

  const modelID = typeof model.id === "string"
    ? model.id
    : typeof model.modelID === "string"
      ? model.modelID
      : typeof model.modelId === "string"
        ? model.modelId
        : ""

  return modelID.startsWith(`${PROVIDER_ID}/`)
}

function resolveWorkspaceDirectory(worktree: unknown, directory: unknown): string {
  if (typeof process.env.CURSOR_ACP_WORKSPACE === "string" && process.env.CURSOR_ACP_WORKSPACE.trim().length > 0) {
    return resolve(process.env.CURSOR_ACP_WORKSPACE)
  }
  if (typeof worktree === "string" && worktree.trim().length > 0) {
    return resolve(worktree)
  }
  if (typeof directory === "string" && directory.trim().length > 0) {
    return resolve(directory)
  }
  return resolve(process.cwd())
}

async function ensureProxyServer(workspaceDirectory: string, client: any): Promise<string> {
  const registry = getServerRegistry()
  const workspaceKey = normalizeWorkspacePath(workspaceDirectory)
  const existing = registry.get(workspaceKey)
  if (existing) {
    return existing.baseURL
  }

  const bunAny = globalThis as Record<string, any>
  if (!bunAny.Bun || typeof bunAny.Bun.serve !== "function") {
    throw new Error("Cursor ACP plugin requires Bun runtime")
  }

  const server = bunAny.Bun.serve({
    hostname: PROXY_HOST,
    port: 0,
    fetch: (request: Request, server: any) => {
      server?.timeout?.(request, 0)
      return handleProxyRequest(request, workspaceDirectory, client)
    },
  })

  const baseURL = `http://${PROXY_HOST}:${server.port}/v1`
  registry.set(workspaceKey, {
    workspaceDirectory,
    baseURL,
    server,
  })

  await log(client, "info", "Started cursor-acp proxy", {
    workspaceDirectory,
    baseURL,
  })

  return baseURL
}

function getPossibleAuthPaths(): string[] {
  const home = homedir()
  const files = ["cli-config.json", "auth.json"]
  const paths: string[] = []
  const isDarwin = process.platform === "darwin"

  if (isDarwin) {
    for (const file of files) paths.push(join(home, ".cursor", file))
    for (const file of files) paths.push(join(home, ".config", "cursor", file))
    return paths
  }

  for (const file of files) paths.push(join(home, ".config", "cursor", file))
  if (typeof process.env.XDG_CONFIG_HOME === "string" && process.env.XDG_CONFIG_HOME.trim().length > 0) {
    for (const file of files) paths.push(join(process.env.XDG_CONFIG_HOME, "cursor", file))
  }
  for (const file of files) paths.push(join(home, ".cursor", file))
  return paths
}

function hasCursorAuthFile(): boolean {
  return getPossibleAuthPaths().some((pathValue) => existsSync(pathValue))
}

async function pollForAuthFile(): Promise<boolean> {
  const start = Date.now()
  while (Date.now() - start < AUTH_POLL_TIMEOUT_MS) {
    if (hasCursorAuthFile()) {
      return true
    }
    await new Promise((resolvePromise) => setTimeout(resolvePromise, AUTH_POLL_INTERVAL_MS))
  }
  return false
}

async function startCursorOAuth(client: any) {
  return await new Promise((resolve, reject) => {
    const child = spawn("cursor-agent", ["login"], {
      stdio: ["pipe", "pipe", "pipe"],
    })

    let stdout = ""
    let stderr = ""
    let resolved = false

    const resolveOnce = (value: unknown) => {
      if (resolved) return
      resolved = true
      resolve(value)
    }

    const rejectOnce = (error: unknown) => {
      if (resolved) return
      resolved = true
      reject(error)
    }

    const extractUrl = () => {
      const collapsed = stripAnsi(stdout).replace(/\s/g, "")
      const match = collapsed.match(LOGIN_URL_REGEX)
      return match ? match[0] : null
    }

    const startTime = Date.now()
    const pollForUrl = async () => {
      while (!resolved && Date.now() - startTime < LOGIN_URL_TIMEOUT_MS) {
        const url = extractUrl()
        if (url) {
          await log(client, "info", "Captured cursor login URL")
          resolveOnce({
            url,
            instructions: "Continue the Cursor login flow in your browser.",
            method: "auto",
            callback: async () => {
              return await new Promise((callbackResolve) => {
                let callbackDone = false

                const finish = (value: unknown) => {
                  if (callbackDone) return
                  callbackDone = true
                  callbackResolve(value)
                }

                child.on("close", async (code) => {
                  if (code === 0 && (await pollForAuthFile())) {
                    finish({ type: "success", provider: PROVIDER_ID, key: "cursor-auth" })
                    return
                  }

                  finish({
                    type: "failed",
                    error: stripAnsi(stderr).trim() || `Cursor login failed with code ${String(code ?? "unknown")}`,
                  })
                })

                setTimeout(() => {
                  try {
                    child.kill()
                  } catch {
                    // Ignore kill failures.
                  }
                  finish({ type: "failed", error: "Cursor login timed out." })
                }, AUTH_POLL_TIMEOUT_MS)
              })
            },
          })
          return
        }

        await new Promise((resolvePromise) => setTimeout(resolvePromise, 100))
      }

      rejectOnce(new Error(stripAnsi(stderr).trim() || "Failed to capture the Cursor login URL."))
      try {
        child.kill()
      } catch {
        // Ignore kill failures.
      }
    }

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString()
    })

    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString()
    })

    void pollForUrl()
  })
}

function buildAllowedToolNameMap(tools: unknown[]): Map<string, string> {
  const allowed = new Map<string, string>()

  for (const rawTool of tools) {
    const tool = isRecord(rawTool) ? rawTool : null
    if (!tool) continue
    const fn = isRecord(tool.function) ? tool.function : tool
    if (typeof fn.name !== "string" || fn.name.trim().length === 0) continue
    allowed.set(normalizeToken(fn.name), fn.name)
  }

  return allowed
}

function buildToolSchemaMap(tools: unknown[]): Map<string, unknown> {
  const schemas = new Map<string, unknown>()

  for (const rawTool of tools) {
    const tool = isRecord(rawTool) ? rawTool : null
    if (!tool) continue
    const fn = isRecord(tool.function) ? tool.function : tool
    if (typeof fn.name !== "string" || fn.name.trim().length === 0) continue
    if (fn.parameters !== undefined) {
      schemas.set(fn.name, fn.parameters)
    }
  }

  return schemas
}

function inferToolName(event: JsonRecord): string {
  if (!isRecord(event.tool_call)) return ""
  const [rawName] = Object.keys(event.tool_call)
  if (!rawName) return ""
  if (rawName.endsWith("ToolCall")) {
    const base = rawName.slice(0, -"ToolCall".length)
    return base.charAt(0).toLowerCase() + base.slice(1)
  }
  return rawName
}

function resolveAllowedToolName(rawName: string, allowed: Map<string, string>): string | null {
  const normalized = normalizeToken(rawName)
  if (allowed.has(normalized)) {
    return allowed.get(normalized) ?? null
  }

  const alias = TOOL_NAME_ALIASES.get(normalized)
  if (alias && allowed.has(alias)) {
    return allowed.get(alias) ?? null
  }

  return null
}

function extractEventArgs(event: JsonRecord): JsonRecord {
  if (!isRecord(event.tool_call)) {
    return {}
  }
  const [rawName] = Object.keys(event.tool_call)
  if (!rawName) return {}
  const payload = isRecord(event.tool_call[rawName]) ? event.tool_call[rawName] : null
  if (!payload) return {}
  if (isRecord(payload.args)) {
    return { ...payload.args }
  }

  const args: JsonRecord = {}
  for (const [key, value] of Object.entries(payload)) {
    if (key === "result") continue
    args[key] = value
  }
  return args
}

function normalizeSpecialToolArgs(toolName: string, args: JsonRecord): JsonRecord {
  const normalized = { ...args }
  const lower = toolName.toLowerCase()

  if (lower === "bash") {
    if (typeof normalized.command !== "string") {
      const command = normalizeBashCommand(normalized.command)
      if (command) {
        normalized.command = command
      }
    }
    if (normalized.cwd === undefined && typeof normalized.workingDirectory === "string") {
      normalized.cwd = normalized.workingDirectory
    }
    if ((typeof normalized.workdir !== "string" || normalized.workdir.trim().length === 0) && typeof normalized.cwd === "string" && normalized.cwd.trim().length > 0) {
      normalized.workdir = normalized.cwd
    }
    if ((typeof normalized.cwd !== "string" || normalized.cwd.trim().length === 0) && typeof normalized.workdir === "string" && normalized.workdir.trim().length > 0) {
      normalized.cwd = normalized.workdir
    }
    if (typeof normalized.description !== "string") {
      const description = coerceToString(normalized.description)
      if (description) {
        normalized.description = description
      }
    }
    delete normalized.workingDirectory
    delete normalized.toolCallId
    delete normalized.simpleCommands
    delete normalized.hasInputRedirect
    delete normalized.hasOutputRedirect
    delete normalized.parsingResult
    delete normalized.fileOutputThresholdBytes
    delete normalized.isBackground
    delete normalized.skipApproval
    delete normalized.timeoutBehavior
    delete normalized.closeStdin
  }

  if (lower === "rm" && typeof normalized.force === "string") {
    const lowered = normalized.force.trim().toLowerCase()
    if (["true", "1", "yes"].includes(lowered)) normalized.force = true
    if (["false", "0", "no"].includes(lowered)) normalized.force = false
  }

  if (lower === "write") {
    if (normalized.content === undefined && normalized.new_string !== undefined) {
      const coerced = coerceToString(normalized.new_string)
      if (coerced !== null) normalized.content = coerced
    }
    if (normalized.content !== undefined && typeof normalized.content !== "string") {
      const coerced = coerceToString(normalized.content)
      if (coerced !== null) normalized.content = coerced
    }
  }

  if (lower === "edit") {
    if (normalized.content !== undefined && typeof normalized.content !== "string") {
      const coerced = coerceToString(normalized.content)
      if (coerced !== null) normalized.content = coerced
    }
    if (normalized.new_string === undefined && typeof normalized.content === "string") {
      normalized.new_string = normalized.content
    }
    if (typeof normalized.new_string === "string" && normalized.old_string === undefined) {
      normalized.old_string = ""
    }
  }

  if (lower === "task") {
    if (typeof normalized.description !== "string") {
      const description = coerceToString(normalized.description)
      if (description !== null) normalized.description = description
    }
    if (typeof normalized.prompt !== "string") {
      const prompt = coerceToString(normalized.prompt)
      if (prompt !== null) normalized.prompt = prompt
    }
    const subagentType = normalizeTaskSubagentType(normalized.subagent_type ?? normalized.subagentType ?? normalized.mode)
    if (subagentType) {
      normalized.subagent_type = subagentType
    }
    if (normalized.task_id === undefined && typeof normalized.agentId === "string" && normalized.agentId.trim().length > 0) {
      normalized.task_id = normalized.agentId
    }
    if (normalized.command !== undefined && typeof normalized.command !== "string") {
      const command = coerceToString(normalized.command)
      if (command !== null) normalized.command = command
    }
    delete normalized.subagentType
    delete normalized.model
    delete normalized.agentId
    delete normalized.attachments
    delete normalized.mode
    delete normalized.respondingToMessageIds
  }

  return normalized
}

function toAbsolutePath(value: unknown, baseDir: string): unknown {
  if (typeof value !== "string") {
    return value
  }

  if (value.trim().length === 0) {
    return value
  }

  return isAbsolute(value) ? value : resolve(baseDir, value)
}

function applyToolContextDefaults(toolName: string, rawArgs: JsonRecord, workspaceDirectory: string): JsonRecord {
  const args = { ...rawArgs }

  for (const key of [
    "path",
    "filePath",
    "targetPath",
    "directory",
    "dir",
    "folder",
    "targetDirectory",
    "targetFile",
    "cwd",
    "workdir",
  ]) {
    if (args[key] !== undefined) {
      args[key] = toAbsolutePath(args[key], workspaceDirectory)
    }
  }

  if ((toolName === "bash" || toolName === "shell") && typeof args.cwd !== "string") {
    args.cwd = workspaceDirectory
  }

  if ((toolName === "bash" || toolName === "shell") && typeof args.cwd === "string" && args.cwd.trim().length === 0) {
    args.cwd = workspaceDirectory
  }

  if (["grep", "glob", "list"].includes(toolName) && (typeof args.path !== "string" || args.path.trim().length === 0)) {
    args.path = workspaceDirectory
  }

  return args
}

function normalizeBashCommand(value: unknown): string | null {
  if (typeof value === "string") return value
  if (Array.isArray(value)) {
    const parts = value.map((entry) => (typeof entry === "string" ? entry : coerceToString(entry))).filter((entry): entry is string => typeof entry === "string" && entry.length > 0)
    return parts.length > 0 ? parts.join(" ") : null
  }
  if (isRecord(value)) {
    const command = typeof value.command === "string" ? value.command : null
    const args = Array.isArray(value.args)
      ? value.args.map((entry) => (typeof entry === "string" ? entry : coerceToString(entry))).filter((entry): entry is string => typeof entry === "string" && entry.length > 0)
      : []
    if (command && args.length > 0) return [command, ...args].join(" ")
    return command
  }
  return null
}

function coerceToString(value: unknown): string | null {
  if (typeof value === "string") return value
  if (value === null || value === undefined) return null
  if (typeof value === "number" || typeof value === "boolean") return String(value)
  if (Array.isArray(value)) {
    const parts = value.map((entry) => {
      if (typeof entry === "string") return entry
      if (isRecord(entry)) {
        if (typeof entry.text === "string") return entry.text
        if (typeof entry.content === "string") return entry.content
      }
      return JSON.stringify(entry)
    })
    return parts.join("")
  }
  if (isRecord(value)) {
    if (typeof value.text === "string") return value.text
    if (typeof value.content === "string") return value.content
    return JSON.stringify(value)
  }
  return null
}

function getSchemaPropertyNames(schema: unknown): string[] {
  if (!isRecord(schema) || !isRecord(schema.properties)) {
    return []
  }
  return Object.keys(schema.properties)
}

function getValueForSchemaProperty(propertyName: string, args: JsonRecord): unknown {
  const directValue = args[propertyName]
  if (isMeaningfulValue(directValue)) {
    return directValue
  }

  const emptyDirectValue = directValue

  const normalizedProperty = normalizeToken(propertyName)

  for (const [key, value] of Object.entries(args)) {
    if (isMeaningfulValue(value) && normalizeToken(key) === normalizedProperty) {
      return value
    }
  }

  for (const [, group] of ARG_KEY_GROUPS) {
    const normalizedGroup = group.map((entry) => normalizeToken(entry))
    if (!normalizedGroup.includes(normalizedProperty)) {
      continue
    }
    for (const [key, value] of Object.entries(args)) {
      if (isMeaningfulValue(value) && normalizedGroup.includes(normalizeToken(key))) {
        return value
      }
    }
  }

  return emptyDirectValue
}

function adaptArgsToSchema(toolName: string, args: JsonRecord, schema: unknown): JsonRecord {
  const normalizedArgs = normalizeSpecialToolArgs(toolName, args)
  const propertyNames = getSchemaPropertyNames(schema)

  if (propertyNames.length === 0) {
    return normalizedArgs
  }

  const adapted: JsonRecord = {}
  for (const propertyName of propertyNames) {
    const value = getValueForSchemaProperty(propertyName, normalizedArgs)
    if (value !== undefined) {
      adapted[propertyName] = value
    }
  }

  if (isRecord(schema) && schema.additionalProperties !== false) {
    for (const [key, value] of Object.entries(normalizedArgs)) {
      if (adapted[key] === undefined) {
        adapted[key] = value
      }
    }
  }

  return adapted
}

function extractToolCallFromEvent(
  event: JsonRecord,
  allowedTools: Map<string, string>,
  toolSchemaMap: Map<string, unknown>,
  workspaceDirectory: string,
): ExtractedToolCall {
  if (event.type !== "tool_call") {
    return { toolCall: null, matchedToolName: null }
  }

  if (typeof event.subtype === "string" && event.subtype !== "started") {
    return { toolCall: null, matchedToolName: null }
  }

  const rawName = inferToolName(event)
  if (rawName.length === 0) {
    return { toolCall: null, matchedToolName: null }
  }

  const matchedToolName = resolveAllowedToolName(rawName, allowedTools)
  if (!matchedToolName) {
    return { toolCall: null, matchedToolName: null }
  }

  const rawArgs = applyToolContextDefaults(matchedToolName, extractEventArgs(event), workspaceDirectory)
  const finalArgs = adaptArgsToSchema(matchedToolName, rawArgs, toolSchemaMap.get(matchedToolName))
  const callID = typeof event.call_id === "string" && event.call_id.length > 0 ? sanitizeToolCallID(event.call_id) : `tool_${Date.now()}`

  return {
    matchedToolName,
    toolCall: {
      id: callID,
      type: "function",
      function: {
        name: matchedToolName,
        arguments: JSON.stringify(finalArgs),
      },
    },
  }
}

function buildChunk(id: string, created: number, model: string, delta: JsonRecord, finishReason: string | null) {
  return {
    id,
    object: "chat.completion.chunk",
    created,
    model,
    choices: [
      {
        index: 0,
        delta,
        finish_reason: finishReason,
      },
    ],
  }
}

function buildCompletionResponse(
  model: string,
  message: { content: string | null; reasoningContent?: string; toolCall?: ToolCall },
  finishReason: string = "stop",
  usage?: unknown,
) {
  const responseMessage: JsonRecord = {
    role: "assistant",
    content: message.content,
  }

  if (message.reasoningContent && message.reasoningContent.length > 0) {
    responseMessage.reasoning_content = message.reasoningContent
  }

  if (message.toolCall) {
    responseMessage.tool_calls = [message.toolCall]
  }

  const payload: JsonRecord = {
    id: `${PROVIDER_ID}-${Date.now()}`,
    object: "chat.completion",
    created: Math.floor(Date.now() / 1000),
    model,
    choices: [
      {
        index: 0,
        message: responseMessage,
        finish_reason: finishReason,
      },
    ],
  }

  if (usage !== undefined) {
    payload.usage = usage
  }

  return payload
}

async function collectNonStreamResult(
  child: any,
  stderrPromise: Promise<string>,
  model: string,
  tools: unknown[],
  client: any,
  workspaceDirectory: string,
): Promise<Response> {
  const allowedTools = buildAllowedToolNameMap(tools)
  const toolSchemaMap = buildToolSchemaMap(tools)
  const streamState: StreamState = {
    assistantText: "",
    reasoningText: "",
    sawAssistantPartials: false,
    sawThinkingPartials: false,
  }

  let firstToolCall: ToolCall | null = null
  let usage: unknown = undefined
  const reader = child.stdout.getReader()
  const decoder = new TextDecoder()
  let buffer = ""
  let interruptedByTool = false

  const handleEvent = (event: JsonRecord) => {
    updateStreamState(streamState, event)

    if (firstToolCall === null) {
      const extracted = extractToolCallFromEvent(event, allowedTools, toolSchemaMap, workspaceDirectory)
      if (extracted.toolCall) {
        firstToolCall = extracted.toolCall
        interruptedByTool = true
        return
      }
    }

    if (event.type === "result" && event.usage !== undefined) {
      usage = event.usage
    }
  }

  outer: while (true) {
    const { value, done } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    while (true) {
      const newlineIndex = buffer.indexOf("\n")
      if (newlineIndex === -1) break
      const line = buffer.slice(0, newlineIndex)
      buffer = buffer.slice(newlineIndex + 1)

      const event = parseJsonLine(line)
      if (!event) continue
      handleEvent(event)

      if (interruptedByTool) {
        try {
          child.kill()
        } catch {
          // Ignore kill failures.
        }
        try {
          await reader.cancel()
        } catch {
          // Ignore cancel failures.
        }
        break outer
      }
    }
  }

  if (!interruptedByTool) {
    buffer += decoder.decode()
    const trailingEvent = parseJsonLine(buffer)
    if (trailingEvent) {
      handleEvent(trailingEvent)
    }
  }

  const stderrText = await stderrPromise
  const exitCode = await child.exited

  if (firstToolCall) {
    return new Response(
      JSON.stringify(
        buildCompletionResponse(
          model,
          {
            content: streamState.assistantText.length > 0 ? streamState.assistantText : null,
            reasoningContent: streamState.reasoningText || undefined,
            toolCall: firstToolCall,
          },
          "tool_calls",
          usage,
        ),
      ),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      },
    )
  }

  const stderr = stripAnsi(stderrText).trim()
  if (exitCode !== 0) {
    void log(client, "error", "cursor-agent non-stream request failed", {
      model,
      exitCode,
      stderr,
    })
    const errorText = stderr || streamState.assistantText || `cursor-agent exited with code ${String(exitCode)}`
    return new Response(JSON.stringify(buildCompletionResponse(model, { content: errorText }, "stop", usage)), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })
  }

  return new Response(
    JSON.stringify(
      buildCompletionResponse(
        model,
        {
          content: streamState.assistantText,
          reasoningContent: streamState.reasoningText || undefined,
        },
        "stop",
        usage,
      ),
    ),
    {
      status: 200,
      headers: { "Content-Type": "application/json" },
    },
  )
}

async function createStreamResponse(child: any, stderrPromise: Promise<string>, model: string, tools: unknown[], client: any, workspaceDirectory: string): Promise<Response> {
  const encoder = new TextEncoder()
  const id = `${PROVIDER_ID}-${Date.now()}`
  const created = Math.floor(Date.now() / 1000)
  const allowedTools = buildAllowedToolNameMap(tools)
  const toolSchemaMap = buildToolSchemaMap(tools)
  const state: StreamState = {
    assistantText: "",
    reasoningText: "",
    sawAssistantPartials: false,
    sawThinkingPartials: false,
  }

  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      const reader = child.stdout.getReader()
      const decoder = new TextDecoder()
      let buffer = ""
      let interruptedByTool = false

      const emit = (payload: unknown) => {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(payload)}\n\n`))
      }

      try {
        while (true) {
          const { value, done } = await reader.read()
          if (done) break
          buffer += decoder.decode(value, { stream: true })

          while (true) {
            const newlineIndex = buffer.indexOf("\n")
            if (newlineIndex === -1) break
            const line = buffer.slice(0, newlineIndex)
            buffer = buffer.slice(newlineIndex + 1)

            const event = parseJsonLine(line)
            if (!event) continue

            if (event.type === "assistant") {
              const text = extractAssistantText(event)
              if (text.length > 0) {
                const isPartial = typeof event.timestamp_ms === "number"
                let delta = ""
                if (isPartial) {
                  state.sawAssistantPartials = true
                  state.assistantText += text
                  delta = text
                } else if (!state.sawAssistantPartials) {
                  delta = text.startsWith(state.assistantText) ? text.slice(state.assistantText.length) : text
                  state.assistantText = text
                }
                if (delta.length > 0) {
                  emit(buildChunk(id, created, model, { content: delta }, null))
                }
              }
              continue
            }

            if (event.type === "thinking") {
              const text = extractThinkingText(event)
              if (text.length > 0) {
                const isPartial = typeof event.timestamp_ms === "number"
                let delta = ""
                if (isPartial) {
                  state.sawThinkingPartials = true
                  state.reasoningText += text
                  delta = text
                } else if (!state.sawThinkingPartials) {
                  delta = text.startsWith(state.reasoningText) ? text.slice(state.reasoningText.length) : text
                  state.reasoningText = text
                }
                if (delta.length > 0) {
                  emit(buildChunk(id, created, model, { reasoning_content: delta }, null))
                }
              }
              continue
            }

            const extracted = extractToolCallFromEvent(event, allowedTools, toolSchemaMap, workspaceDirectory)
            if (extracted.toolCall) {
              interruptedByTool = true
              emit(
                buildChunk(
                  id,
                  created,
                  model,
                  {
                    role: "assistant",
                    tool_calls: [
                      {
                        index: 0,
                        ...extracted.toolCall,
                      },
                    ],
                  },
                  null,
                ),
              )
              emit(buildChunk(id, created, model, {}, "tool_calls"))
              controller.enqueue(encoder.encode("data: [DONE]\n\n"))
              try {
                child.kill()
              } catch {
                // Ignore kill failures.
              }
              controller.close()
              return
            }
          }
        }

        const exitCode = await child.exited
        const stderr = stripAnsi((await stderrPromise) || "").trim()

        if (!interruptedByTool) {
          if (exitCode !== 0) {
            const errorText = stderr || `cursor-agent exited with code ${String(exitCode)}`
            emit(buildChunk(id, created, model, { content: errorText }, null))
            void log(client, "error", "cursor-agent stream request failed", {
              model,
              exitCode,
              stderr,
            })
          }

          emit(buildChunk(id, created, model, {}, "stop"))
          controller.enqueue(encoder.encode("data: [DONE]\n\n"))
          controller.close()
        }
      } catch (error) {
        void log(client, "error", "cursor-acp stream handler crashed", {
          error: String(error),
        })
        controller.error(error)
      }
    },
  })

  return new Response(stream, {
    status: 200,
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  })
}

function parseChatRequestBody(body: unknown): ParsedChatBody {
  const payload = isRecord(body) ? body : {}
  const originalModel = typeof payload.model === "string" ? payload.model : "auto"
  const messages = Array.isArray(payload.messages) ? payload.messages : []
  const tools = Array.isArray(payload.tools) ? payload.tools : []

  return {
    originalModel,
    model: normalizeRuntimeModel(originalModel),
    stream: payload.stream === true,
    prompt: buildPromptFromMessages(messages, tools),
    messages,
    tools,
  }
}

async function handleChatCompletions(request: Request, workspaceDirectory: string, client: any): Promise<Response> {
  const body = parseChatRequestBody(await request.json())
  const bunAny = globalThis as Record<string, any>
  if (!bunAny.Bun || typeof bunAny.Bun.spawn !== "function") {
    return new Response(JSON.stringify({ error: "Cursor ACP plugin requires Bun runtime." }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    })
  }

  const command = [
    "cursor-agent",
    "--print",
    "--output-format",
    "stream-json",
    "--stream-partial-output",
    "--workspace",
    workspaceDirectory,
    "--trust",
    "--model",
    body.model,
  ]

  void log(client, "debug", "Dispatching cursor-agent request", {
    model: body.model,
    stream: body.stream,
    workspaceDirectory,
    toolCount: body.tools.length,
    promptChars: body.prompt.length,
  })

  const child = bunAny.Bun.spawn({
    cmd: command,
    stdin: "pipe",
    stdout: "pipe",
    stderr: "pipe",
    env: bunAny.Bun.env,
  })

  child.stdin.write(body.prompt)
  child.stdin.end()

  const stderrPromise = new Response(child.stderr).text().catch(() => "")

  if (!body.stream) {
    return await collectNonStreamResult(child, stderrPromise, body.originalModel, body.tools, client, workspaceDirectory)
  }

  return await createStreamResponse(child, stderrPromise, body.originalModel, body.tools, client, workspaceDirectory)
}

async function handleProxyRequest(request: Request, workspaceDirectory: string, client: any): Promise<Response> {
  const url = new URL(request.url)

  if (request.method === "GET" && url.pathname === "/health") {
    return Response.json({ ok: true, workspaceDirectory, provider: PROVIDER_ID })
  }

  if (request.method === "GET" && (url.pathname === "/v1/models" || url.pathname === "/models")) {
    const models = discoverCursorModels().map((model) => ({
      id: model.id,
      object: "model",
      owned_by: PROVIDER_ID,
      created: 0,
      name: model.name,
    }))
    return Response.json({ object: "list", data: models })
  }

  if (request.method === "POST" && (url.pathname === "/v1/chat/completions" || url.pathname === "/chat/completions")) {
    return await handleChatCompletions(request, workspaceDirectory, client)
  }

  return new Response(JSON.stringify({ error: "Not Found" }), {
    status: 404,
    headers: { "Content-Type": "application/json" },
  })
}

export const CursorAcpPlugin = async (input: any) => {
  const workspaceDirectory = resolveWorkspaceDirectory(input?.worktree, input?.directory)
  const proxyBaseURLPromise = ensureProxyServer(workspaceDirectory, input?.client)

  return {
    async config(config: JsonRecord) {
      removeDisabledProvider(config)
      ensureCursorProvider(config, await proxyBaseURLPromise)
      await log(input?.client, "info", "Refreshed cursor-acp provider config", {
        modelCount: discoverCursorModels().length,
      })
    },

    auth: {
      provider: PROVIDER_ID,
      async loader() {
        return {}
      },
      methods: [
        {
          label: "Cursor OAuth",
          type: "oauth",
          async authorize() {
            return await startCursorOAuth(input?.client)
          },
        },
      ],
    },

    async "chat.params"(chatInput: JsonRecord, output: JsonRecord) {
      if (!isCursorProviderModel(chatInput.model)) {
        return
      }

      const proxyBaseURL = await proxyBaseURLPromise
      const options = isRecord(output.options) ? output.options : {}
      output.options = options
      options.baseURL = proxyBaseURL
      if (typeof options.apiKey !== "string" || options.apiKey.trim().length === 0) {
        options.apiKey = "cursor-agent"
      }
    },
  }
}
