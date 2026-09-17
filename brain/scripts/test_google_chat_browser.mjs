import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeTopic, parseTopics, nextCursor, createTopicReader, authenticateFromBrowser, SPACES } from './google_chat_browser.mjs';

function message(id, text = 'Hola', time = '1789000000000000') {
  const m = [];
  m[0] = [null, id]; m[1] = [['u1'], 'Stan', null, 'stan@example.com'];
  m[2] = time; m[3] = time; m[9] = text;
  return m;
}

function topic(messages = [message('root')], replies = 0) {
  const t = [];
  t[0] = [null, 'root', [['space1']]]; t[1] = '1789000000000000';
  t[6] = messages; t[10] = [];
  t[10][12] = [String(replies)];
  return t;
}

test('keeps replies, edits, names, links and reactions without browser credentials', () => {
  const root = message('root'), reply = message('reply', 'Gracias', '1789000001000000');
  reply[3] = '1789000002000000';
  reply[20] = [[['🙌'], 2, false, '1789000002000000']];
  const link = [1, 0, 4]; link[6] = [];
  link[6][6] = [null, null, 'https://example.com/doc'];
  link[6][13] = [null, null, 'https://chat.google.com/api/get_redirect_url?token=secret'];
  const file = [13]; file[9] = ['secret-download-token', null, 'image.png', 'image/png'];
  root[10] = [link, file];
  const result = normalizeTopic(topic([root, reply], 1), 'space1');
  assert.equal(result.messages[1].sender.name, 'Stan');
  assert.equal(result.messages[1].update_time_usec, '1789000002000000');
  assert.deepEqual(result.messages[1].reactions, [{ emoji: '🙌', count: 2 }]);
  assert.deepEqual(result.messages[0].links, ['https://example.com/doc']);
  assert.deepEqual(result.messages[0].attachments, [{ name: 'image.png', mime_type: 'image/png' }]);
  assert.ok(!JSON.stringify(result).includes('secret'));
});

test('preserves deletion markers without inventing a sender or text', () => {
  const m = message('root');
  m[1] = null; m[9] = null; m[3] = null;
  m[7] = '1789000002000000'; m[30] = [true];
  const deletedTopic = topic([m]); deletedTopic[1] = '0'; deletedTopic[14] = m[2];
  const result = normalizeTopic(deletedTopic, 'space1').messages[0];
  assert.equal(result.deleted, true);
  assert.equal(result.text, '');
  assert.equal(result.sender.id, null);
  assert.equal(nextCursor([deletedTopic], null), Number(m[2]));
});

test('rejects incomplete replies, duplicate messages, wrong spaces and unknown schemas', () => {
  assert.throws(() => normalizeTopic(topic([message('root')], 2), 'space1'), /Incomplete/);
  assert.throws(() => normalizeTopic(topic([message('root'), message('root')], 1), 'space1'), /Incomplete/);
  assert.throws(() => normalizeTopic(topic(), 'other'), /unexpected space/);
  const malformed = message('root'); malformed[1] = null;
  assert.throws(() => normalizeTopic(topic([malformed]), 'space1'), /format changed/);
});

test('accepts only the observed response envelope, including a real empty page', () => {
  assert.deepEqual(parseTopics(")]}'\n" + JSON.stringify([['dfe.t.lt', [topic()]]])), JSON.parse(JSON.stringify([topic()])));
  assert.deepEqual(parseTopics(JSON.stringify([['dfe.t.lt', null]])), []);
  assert.throws(() => parseTopics('<html>Sign in</html>'), /unreadable/);
  assert.throws(() => parseTopics('[[]]'), /format changed/);
});

test('pagination must advance backwards with precise microsecond timestamps', () => {
  const older = topic(); older[1] = '1788000000000000';
  assert.equal(nextCursor([topic(), older], null), 1788000000000000);
  assert.throws(() => nextCursor([topic()], 1789000000000000), /stopped advancing/);
});

function authentication(generation = 1) {
  const body = [];
  body[7] = [[SPACES[0].id]];
  body[99] = [generation];
  return { url: 'https://chat.google.com/u/2/api/list_topics?c=1', body,
    headers: { cookie: `test-session-${generation}`, 'x-framework-xsrf-token': `test-xsrf-${generation}`,
      'x-goog-chat-space-id': `space/${SPACES[0].id}` } };
}

function emptyPage() {
  return new Response(JSON.stringify([['dfe.t.lt', null]]), { headers: { 'content-type': 'application/json' } });
}

test('direct reads share one authentication capture across both spaces and pages', async () => {
  let captures = 0;
  const calls = [];
  const reader = createTopicReader({ authenticate: async () => { captures++; return authentication(); },
    request: async (url, options) => { calls.push({ url, options }); return emptyPage(); } });
  await reader.read(SPACES[0].id);
  await reader.read(SPACES[1].id, 1789000000000000);
  assert.equal(captures, 1);
  const second = calls[1].options;
  assert.equal(second.redirect, 'manual');
  assert.equal(second.headers.cookie, 'test-session-1');
  assert.equal(second.headers['x-goog-chat-space-id'], `space/${SPACES[1].id}`);
  const body = JSON.parse(second.body);
  assert.deepEqual(body[7], [[SPACES[1].id]]);
  assert.deepEqual(body[3], [1789000000000000]);
  reader.close();
});

test('expired auth refreshes once, preserving the space and page cursor', async () => {
  let captures = 0;
  const calls = [];
  const reader = createTopicReader({ authenticate: async () => authentication(++captures),
    request: async (url, options) => {
      calls.push(options);
      return calls.length === 1 ? new Response('', { status: 401 }) : emptyPage();
    } });
  await reader.read(SPACES[1].id, 1789000000000000);
  assert.equal(captures, 2);
  assert.equal(calls[1].headers.cookie, 'test-session-2');
  const body = JSON.parse(calls[1].body);
  assert.deepEqual(body[99], [2]);
  assert.deepEqual(body[3], [1789000000000000]);
  assert.deepEqual(body[7], [[SPACES[1].id]]);
});

test('persistent rejection stops after one refresh for the entire run', async () => {
  let captures = 0, requests = 0;
  const reader = createTopicReader({ authenticate: async () => authentication(++captures),
    request: async () => {
      requests++;
      return requests === 2 ? emptyPage() : new Response('', { status: 403 });
    } });
  await reader.read(SPACES[0].id);
  await assert.rejects(reader.read(SPACES[1].id), /authentication was rejected/);
  assert.equal(captures, 2);
  assert.equal(requests, 3);
});

test('login redirects and HTML responses refresh auth without following redirects', async () => {
  for (const response of [new Response('', { status: 302, headers: { location: 'https://accounts.google.com/' } }),
    new Response('<html>Sign in</html>', { headers: { 'content-type': 'text/html' } })]) {
    let captures = 0, requests = 0;
    const reader = createTopicReader({ authenticate: async () => authentication(++captures),
      request: async (url, options) => {
        assert.equal(options.redirect, 'manual');
        return ++requests === 1 ? response : emptyPage();
      } });
    await reader.read(SPACES[0].id);
    assert.equal(captures, 2);
  }
});

test('rate limits, schema changes and network errors do not trigger an auth loop', async () => {
  for (const failure of ['rate-limit', 'schema', 'network']) {
    let captures = 0, requests = 0;
    const reader = createTopicReader({ authenticate: async () => authentication(++captures),
      request: async () => {
        requests++;
        if (failure === 'network') throw new Error('Network error with sensitive request details');
        if (failure === 'schema') return new Response('[[]]');
        return new Response('', { status: 429 });
      } });
    await assert.rejects(reader.read(SPACES[0].id), error => !error.message.includes('sensitive'));
    assert.equal(captures, 1);
    assert.equal(requests, 1);
  }
});

test('credentials cannot be sent to an unexpected host, endpoint or space', async () => {
  for (const url of ['https://example.com/u/2/api/list_topics', 'https://chat.google.com/u/2/api/send_message']) {
    let requests = 0;
    const reader = createTopicReader({ authenticate: async () => ({ ...authentication(), url }),
      request: async () => { requests++; return emptyPage(); } });
    await assert.rejects(reader.read(SPACES[0].id), /Unexpected Google Chat read endpoint/);
    await assert.rejects(reader.read('other-space'), /Unexpected Google Chat space/);
    assert.equal(requests, 0);
  }
});

test('separate syncs reuse cached authentication after the prior reader closes', async () => {
  const cache = { value: null };
  let captures = 0;
  const options = { cache, authenticate: async () => authentication(++captures), request: async () => emptyPage() };
  const first = createTopicReader(options);
  await first.read(SPACES[0].id);
  first.close();
  const second = createTopicReader(options);
  await second.read(SPACES[1].id);
  second.close();
  assert.equal(captures, 1);
  // A new helper process has an empty cache.
  const restarted = createTopicReader({ ...options, cache: { value: null } });
  await restarted.read(SPACES[0].id);
  assert.equal(captures, 2);
});

test('rejected cached auth is refreshed and the replacement survives the sync', async () => {
  const cache = { value: authentication(1) };
  let captures = 0;
  const reader = createTopicReader({ cache,
    authenticate: async () => { captures++; return authentication(2); },
    request: async (url, options) => options.headers.cookie === 'test-session-1'
      ? new Response('', { status: 401 }) : emptyPage() });
  await reader.read(SPACES[1].id);
  reader.close();
  assert.equal(captures, 1);
  assert.equal(cache.value.headers.cookie, 'test-session-2');
});

test('authentication that still fails after refreshing is evicted from the shared cache', async () => {
  const cache = { value: authentication() };
  let captures = 0;
  const reader = createTopicReader({ cache,
    authenticate: async () => { captures++; return authentication(2); },
    request: async () => new Response('', { status: 403 }) });
  await assert.rejects(reader.read(SPACES[0].id), /authentication was rejected/);
  assert.equal(captures, 1);
  assert.equal(cache.value, null);
});

test('temporary HTTP failures preserve cached authentication for the next sync', async () => {
  const auth = authentication();
  const cache = { value: auth };
  const authenticate = async () => { throw new Error('Should not refresh'); };
  const failed = createTopicReader({ cache, authenticate, request: async () => new Response('', { status: 429 }) });
  await assert.rejects(failed.read(SPACES[0].id), /HTTP 429/);
  failed.close();
  assert.equal(cache.value, auth);
  const next = createTopicReader({ cache, authenticate, request: async () => emptyPage() });
  await next.read(SPACES[1].id);
});

test('authentication recovers when Chat is closed but the browser is still signed in', async () => {
  let closed = false, visited = null;
  const request = {
    url: () => 'https://chat.google.com/u/2/api/list_topics?c=1',
    postData: () => JSON.stringify(authentication().body),
    allHeaders: async () => authentication().headers,
  };
  const page = {
    waitForRequest: async predicate => { assert.ok(predicate(request)); return request; },
    goto: async url => { visited = url; },
    getByRole: (role, options) => {
      assert.equal(options.name, 'Google Account: stan.samisco@ext.sierra.ai');
      return { first: () => ({ waitFor: async () => {} }) };
    },
    close: async () => { closed = true; },
  };
  const result = await authenticateFromBrowser({ pages: () => [], newPage: async () => page });
  assert.equal(visited, `https://chat.google.com/u/2/app/chat/${SPACES[0].id}`);
  assert.equal(closed, true);
  assert.equal(result.headers.cookie, 'test-session-1');
});

test('closed-tab recovery refuses another account and closes the temporary tab', async () => {
  let closed = false, headersRead = false;
  const request = {
    url: () => 'https://chat.google.com/u/2/api/list_topics?c=1',
    postData: () => JSON.stringify(authentication().body),
    allHeaders: async () => { headersRead = true; return authentication().headers; },
  };
  const page = {
    waitForRequest: async () => request,
    goto: async () => {},
    getByRole: () => ({ first: () => ({ waitFor: async () => { throw new Error('Account mismatch'); } }) }),
    close: async () => { closed = true; },
  };
  await assert.rejects(authenticateFromBrowser({ pages: () => [], newPage: async () => page }), /Sign into Google Chat as stan.samisco@ext.sierra.ai/);
  assert.equal(headersRead, false);
  assert.equal(closed, true);
});
