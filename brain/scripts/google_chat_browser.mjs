// Google Chat's browser protocol, observed on 2026-09-15. No OAuth or saved credentials.
import fs from 'node:fs/promises';

export const ACCOUNT = 'stan.samisco@ext.sierra.ai';
export const SPACES = [
  { id: 'AAQAkdY0pQg', name: 'Voicebot - Openpay' },
  { id: 'AAQAZ0v2SzU', name: 'VoiceBot- Cobranza' },
];

// Playwriter's relay retains imported modules across short-lived CLI sessions.
// Keep auth in that process only; a relay restart or exporter update clears it.
const sharedAuthentication = { value: null };

export function parseTopics(text) {
  let envelope;
  try { envelope = JSON.parse(text.replace(/^\)\]\}'\s*/, '')); }
  catch { throw new Error('Google Chat returned an unreadable response; previous exports were kept.'); }
  const payload = envelope?.find?.(row => row?.[0] === 'dfe.t.lt');
  if (!payload || (payload[1] != null && !Array.isArray(payload[1]))) {
    throw new Error('Google Chat message format changed; previous exports were kept.');
  }
  return payload[1] ?? [];
}

function timestamp(value, field = 'timestamp') {
  if (!/^\d{15,17}$/.test(String(value))) throw new Error(`Invalid Google Chat ${field}: ${String(value)}.`);
  return String(value);
}

function topicSortTime(topic) {
  // Deleted roots retain their creation time but have a zero last-activity time.
  return timestamp(topic[1] === '0' && topic[6]?.[0]?.[30]?.[0] === true ? topic[14] : topic[1]);
}

function annotations(items) {
  const links = [], attachments = [];
  for (const item of items ?? []) {
    // Only canonical link targets; omit signed redirects, thumbnails and auth data.
    const url = item?.[6]?.[6]?.[2] ?? item?.[29]?.[0]?.[2];
    if (typeof url === 'string' && /^https?:\/\//.test(url)) links.push(url);
    if ([2, 3, 4].includes(item?.[0])) {
      const file = item[3];
      if (Array.isArray(file) && typeof file[1] === 'string') {
        attachments.push({ name: file[1], ...(url ? { url } : {}) });
      }
    }
    if (item?.[0] === 13 && typeof item[9]?.[2] === 'string') {
      // Uploaded files expose a signed download token at [9][0]; keep metadata only.
      attachments.push({ name: item[9][2], mime_type: item[9][3] });
    }
  }
  return { links: [...new Set(links)], attachments: [...new Map(attachments.map(a => [a.name, a])).values()] };
}

export function normalizeTopic(topic, spaceID) {
  const id = topic?.[0]?.[1];
  if (typeof id !== 'string' || topic?.[0]?.[2]?.[0]?.[0] !== spaceID || !Array.isArray(topic[6])) {
    throw new Error('Google Chat returned an unexpected space or thread format.');
  }
  const expectedReplies = Number(topic?.[10]?.[12]?.[0]);
  if (!Number.isSafeInteger(expectedReplies) || expectedReplies < 0) {
    throw new Error('Google Chat did not provide a verifiable reply count.');
  }
  const messages = topic[6].map(m => {
    const messageID = m?.[0]?.[1];
    const deleted = m?.[30]?.[0] === true && /^\d{15,17}$/.test(String(m?.[7]));
    if (typeof messageID !== 'string' || (!deleted && !Array.isArray(m[1])) || (m[9] != null && typeof m[9] !== 'string')) {
      throw new Error(`Google Chat message format changed in thread ${id}.`);
    }
    return {
      id: messageID, thread_id: id,
      sender: { id: m[1]?.[0]?.[0] ?? null, name: m[1]?.[1] || 'Unknown', email: m[1]?.[3] || '' },
      create_time_usec: timestamp(m[2], `creation time in ${id}`), update_time_usec: timestamp(m[3] ?? m[2], `update time in ${id}`),
      deleted, ...(deleted ? { delete_time_usec: timestamp(m[7]) } : {}),
      text: m[9] ?? '', ...annotations(m[10]),
      reactions: (m[20] ?? []).map(r => ({ emoji: r[0]?.[0] || '[custom emoji]', count: r[1] })),
    };
  });
  const unique = new Map(messages.map(m => [m.id, m]));
  if (!unique.has(id) || unique.size !== expectedReplies + 1) {
    throw new Error(`Incomplete Google Chat thread ${id}: received ${unique.size} messages, expected ${expectedReplies + 1}. Previous exports were kept.`);
  }
  return { id, sort_time_usec: topicSortTime(topic), reply_count: expectedReplies,
    messages: [...unique.values()].sort((a, b) => a.create_time_usec.localeCompare(b.create_time_usec)) };
}

export function nextCursor(topics, previous) {
  const cursor = topics.map(t => BigInt(topicSortTime(t))).reduce((a, b) => a < b ? a : b);
  if (previous != null && cursor >= BigInt(previous)) throw new Error('Google Chat pagination stopped advancing.');
  if (!Number.isSafeInteger(Number(cursor))) throw new Error('Google Chat pagination timestamp exceeds safe precision.');
  return Number(cursor);
}

export async function authenticateFromBrowser(context) {
  let source;
  for (const candidate of context.pages()) {
    if (new URL(candidate.url()).hostname !== 'chat.google.com') continue;
    if (await candidate.getByRole('button', { name: `Google Account: ${ACCOUNT}`, exact: true }).count()) {
      source = candidate;
      break;
    }
  }
  // Sierra is account 2 in Stan's browser. Prefer a verified open tab's account
  // index, but recover a closed tab using that known URL and verify identity below.
  const prefix = source ? new URL(source.url()).pathname.match(/^\/u\/\d+\//)?.[0] : '/u/2/';
  if (!prefix) throw new Error('Google Chat account URL was not recognized.');
  const base = `https://chat.google.com${prefix}`;
  const page = await context.newPage();
  try {
    const space = SPACES[0];
    const observed = page.waitForRequest(r => {
      if (new URL(r.url()).pathname !== `${prefix}api/list_topics`) return false;
      try { return JSON.parse(r.postData())?.[7]?.[0]?.[0] === space.id; } catch { return false; }
    }, { timeout: 30000 });
    observed.catch(() => {});
    await page.goto(`${base}app/chat/${space.id}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    try {
      await page.getByRole('button', { name: `Google Account: ${ACCOUNT}`, exact: true }).first().waitFor({ timeout: 15000 });
    } catch {
      throw new Error(`Sign into Google Chat as ${ACCOUNT} in the connected browser, then retry Sync.`);
    }
    const request = await observed;
    const originalHeaders = await request.allHeaders();
    const headers = Object.fromEntries(Object.entries(originalHeaders).filter(([key]) =>
      ['cookie', 'content-type', 'x-framework-xsrf-token', 'x-goog-chat-space-id', 'origin', 'referer'].includes(key)));
    if (!headers.cookie || !headers['x-framework-xsrf-token']) {
      throw new Error('Google Chat browser authorization was not available.');
    }
    return { url: request.url(), headers, body: JSON.parse(request.postData()) };
  } finally {
    // History requests start only after this temporary tab has closed.
    await page.close().catch(() => {});
  }
}

export function createTopicReader({ authenticate, request = globalThis.fetch, cache = { value: null } }) {
  let auth = cache.value;
  let refreshed = false;
  return {
    async read(spaceID, cursor = null) {
      if (!SPACES.some(space => space.id === spaceID)) throw new Error('Unexpected Google Chat space.');
      if (!auth) {
        auth = await authenticate();
        cache.value = auth;
      }
      for (;;) {
        const url = new URL(auth.url);
        if (url.origin !== 'https://chat.google.com' || !/^\/u\/\d+\/api\/list_topics$/.test(url.pathname)) {
          throw new Error('Unexpected Google Chat read endpoint.');
        }
        const body = structuredClone(auth.body);
        const headers = { ...auth.headers };
        const originalSpace = body[7]?.[0]?.[0];
        if (!SPACES.some(space => space.id === originalSpace)) throw new Error('Unexpected Google Chat authentication space.');
        if (headers['x-goog-chat-space-id']) {
          headers['x-goog-chat-space-id'] = headers['x-goog-chat-space-id'].replace(originalSpace, spaceID);
        }
        body[7] = [[spaceID]];
        body[3] = cursor == null ? null : [cursor];
        body[8] = null; body[9] = null;
        body[6] = 1000;
        let response;
        try {
          // Node HTTP, not page.evaluate; credentials stay in relay memory.
          response = await request(url.href, {
            method: 'POST', headers, body: JSON.stringify(body), redirect: 'manual',
            signal: AbortSignal.timeout(30000),
          });
        } catch {
          throw new Error('Google Chat direct request failed or timed out; previous exports were kept.');
        }
        const needsAuth = [401, 403].includes(response.status)
          || (response.status >= 300 && response.status < 400)
          || (response.headers.get('content-type') ?? '').includes('text/html');
        if (needsAuth) {
          await response.body?.cancel();
          cache.value = null;
          auth = null;
          if (refreshed) throw new Error('Google Chat authentication was rejected. Sign back into Sierra Chat and retry Sync.');
          refreshed = true;
          auth = await authenticate();
          cache.value = auth;
          continue;
        }
        if (response.status !== 200) {
          await response.body?.cancel();
          throw new Error(`Google Chat read failed (HTTP ${response.status}); previous exports were kept.`);
        }
        return parseTopics(await response.text());
      }
    },
    close() { auth = null; },
  };
}

export async function capture({ context, outputPath }) {
  let authenticationCaptures = 0;
  const reader = createTopicReader({
    cache: sharedAuthentication,
    authenticate: async () => {
      const auth = await authenticateFromBrowser(context);
      authenticationCaptures++;
      return auth;
    },
  });
  const spaces = [];
  try {
    for (const space of SPACES) {
      const threads = new Map();
      let completed = false;
      let pages = 0;
      let cursor = null;
      for (; pages < 500; pages++) {
        const topics = await reader.read(space.id, cursor);
        if (!topics.length) { completed = true; break; }
        for (const topic of topics) {
          const normalized = normalizeTopic(topic, space.id);
          if (!threads.has(normalized.id)) threads.set(normalized.id, normalized);
        }
        cursor = nextCursor(topics, cursor);
        await new Promise(resolve => setTimeout(resolve, 250));
      }
      if (!completed) throw new Error('Google Chat history reached the page limit; previous exports were kept.');
      spaces.push({ space, history_complete: true, pages: pages + 1, threads: [...threads.values()] });
      console.log(`${space.name}: ${threads.size} threads read`);
    }
    await fs.writeFile(outputPath, JSON.stringify({ account: ACCOUNT, captured_at: new Date().toISOString(),
      authentication_captures: authenticationCaptures, spaces }), { mode: 0o600 });
  } finally {
    reader.close();
  }
}
