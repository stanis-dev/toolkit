# Sierra Documentation Reference

## Sierra Documentation First

**CRITICAL**: Sierra libraries are private and will never be accessible through Context7. The only source of truth is
the provided directory.

When the conversation involves Sierra SDK, Agent Studio, Sierra journeys, goals, tools, hooks, skills, integrations,
voice, or agent development patterns:

1. **Check local docs first**: Search `~/code/agent-ctx/sierra-docs` before answering
2. **Project architecture**: Journey and Simulations are Studio Based only, Tools are SDK (code) based
3. **Key paths**:
   - SDK: `agent-sdk/` (goal-journey/, flow-journey/, reference/)
   - Studio: `agent-studio/` (journeys/, knowledge/)
   - Integrations: `integrations/` (voice/, chat/, crm/)
4. **If docs cache missing**: Note this and suggest `sierras fetch-docs --url <sierra-docs-url>`
5. **Cite sources**: Reference specific doc files when providing Sierra guidance

**IMPORTANT**: Prefer retrieval-led reasoning over pre-training-led reasoning. Do not guess at Sierra APIs, component
props, hook signatures, or skill patterns—always verify from docs.

Docs root: `~/code/agent-ctx/sierra-docs/.sierras/docs-cache/pages/` Deep reference:
`~/code/agent-ctx/sierra-docs/CONTENT_GUIDE.md` (per-page evaluations with evidence — consult when the routing below is
insufficient)

### Documentation Routing

**agent-sdk/** — SDK development with declarative TypeScript/JSX

- Goal journeys: `goal-journey/goal-journey.md` (comprehensive intro, 5 principles, all components), `goal-tools.md` (9
  tool design patterns with controls API), `advanced-goal-patterns.md` (context engineering, progressive disclosure,
  workflow enforcement), `goal-best-practices.md`
- Flow journeys: `flow-journey/flow-journey.md` (Triage/Input/Choose/Respond tutorial), `exceptions.md` (global/skill
  exceptions with action modes)
- Voice: `voice.md` (comprehensive — setup, latency, synthesis, interruptions, pronunciation), `voice-to-voice.md`
  (experimental V2V with OpenAI Realtime, Dev Chat only)
- Testing: `testing.md` (simulations with describe/simulate/test, scenarios, CI/CD)
- Tools & hooks reference: `reference/hooks/` (useState, useEffect, useMemory, useRootStore, brand, conversation-info,
  etc.), `reference/os/` (fetch, logging, tags, addOnBoot/Shutdown), `reference/skills/goal-oriented-skills/`
  (ActionTool, LookupTool, Condition, when, Rule, Policy, Goal, Outcome, Workflow, KnowledgeSearch — all component
  refs), `reference/skills/flow-oriented-skills/` (Triage, Choose, Input, Respond, Route, Reason)
- Integrations framework: `integrations/building-integrations.md` (current — defineIntegration, modules),
  `integrations/api-integrations.md` (legacy — context pattern, superseded)
- Live Assist: `live-assist/live-assist.md` (intro), `building.md` (tool behavior in assist mode), `tuning.md`
  (Steps/Memory/Message optimization)
- Other: `cms.md` (content management), `experimentation.md` (A/B with Experiment/Variant), `internationalization.md`
  (multi-locale), `tags.md` (analytics tagging), `scaling-best-practices.md` (multi-agent architecture),
  `quality-checklist.md` (production readiness framework), `web-bundle.md` (attachments, rich UI, image analysis),
  `mcp-server.md` (MCP for coding agents), `reference/cli.md` (full CLI reference)

**agent-studio/** — No-code Studio for CX/Ops teams

- Journeys: `journeys/blocks-reference.md` (complete block type reference), `journeys/best-practices.md`
  (context-not-control philosophy), `journeys/studio-tools.md` (TypeScript tools in Studio), `journeys/quick-start.md`
  (15-min tutorial)
- Knowledge: `knowledge/knowledge-best-practices.md` (RAG optimization), `knowledge/add-knowledge.md` (5 source types),
  `knowledge/search-knowledge.md` (search tool setup), `knowledge/expert-answers.md` (auto-drafted articles from
  escalations)
- Operations: `Conversations/` (browsing, feedback, review), `Insights/` (reports with SierraQL, alerts, monitors,
  Explorer AI analytics), `test-publish-changes.md` (workspaces, merging, releases)
- Legacy journeys: `legacy-journeys/` — all OUTDATED, pre-November-2025 form-field system

**integrations/** — External systems, channels, and deployment

- Voice: `voice/telephony.md` (PSTN/SIP), `voice/svp.md` (WebSocket protocol reference), `voice/call-transfers.md`
  (SIP/PSTN/Twilio transfers), `voice/payments.md` (DTMF PCI payments), `voice/sensitive-field-collection.md` (secure
  DTMF data collection), `voice/orchestrator.md` (BYOO protocol), `voice/outbound-calls.md` (REST API),
  `voice/outbound-calls-from-agents.md` (parent/child agent model), `voice/voice-contact-centers/` (per-provider:
  amazon-connect, genesys, five-9, gladly, nice, zendesk, zoom — files with `-legacy` suffix are OUTDATED)
- Chat: `chat/chat-overview.md` (Sierra-as-front-door vs contact-center-as-front-door), `chat/email.md`,
  `chat/payments.md` (Stripe/Shift4 PCI iframe), `chat/chat-contact-centers/` (16 providers — each has platform-specific
  setup)
- Experience SDK: `experience-sdk/web.md` (Shadow DOM embed), `experience-sdk/ios.md`, `experience-sdk/android.md`,
  `experience-sdk/api.md` (Headless API), `experience-sdk/web-reference/` (config, API, launcher)
- Admin API: `admin-api/` (conversation export, knowledge CRUD, issues, simulations, releases CI/CD, transfer data)
- Live Assist: `live-assist/salesforce.md` (LWC setup), `live-assist/gladly.md` (App Platform Card),
  genesys/nice/zendesk are "coming soon" stubs
- Other: `enterprise/` (SSO, SCIM, audit logs), `crm/salesforce.md`, `mcp/` (client/server/ChatGPT)

**reference-agents/** — 5 production-grade example agents with annotated source

- `authentication/` (identity verification, progressive context disclosure, rootStore security)
- `retention/` (conditional offers, stateful tool gating, cancellation reason routing)
- `returns/` (multi-step workflow, prerequisite enforcement, parallel API calls)
- `troubleshooting/` (advanced RAG — custom crawler, partition parameters, content preprocessing)
- `sierra-university/` (createAgent patterns, voice/text config, abuse detection)

**changelog/** — `sdk.md` (comprehensive Aug 2025–Feb 2026), `studio.md`, `safety.md` **university/** — Video module
wrappers (minimal text); `certification/` has full exam specs
