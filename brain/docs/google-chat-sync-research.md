# Google Chat sync options

**Decision (2026-09-15):** Stan chose browser scraping to avoid Cloud/OAuth setup.
The implementation uses the signed-in Sierra Chat tab through Playwriter and reads
the structured responses used by the browser. The API research below is retained
as background, not the selected implementation.

Researched 2026-09-15 against Google's documentation. Targets supplied by Stan:

- `voicebot - openpay`
- `voicebot - Cobranza`

## Conclusion

**Browser scraping is not the only supported option. Try the Google Chat REST API with user OAuth first.** Google documents listing messages in a space the authenticated caller belongs to, using the read-only `chat.messages.readonly` scope. This route does not require adding a bot to the two spaces. App authentication is a separate route requiring administrator approval for message listing. [Message list reference](https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages/list)

**Account-specific access is unverified.** This research did not authenticate, read either space, create a Cloud project, change credentials, or test an organization's policy. Confirm the actual account, membership, space IDs, oldest available messages, and OAuth access before selecting the implementation.

## Access and one-time setup

1. Use the Google account that is already a member of both spaces. Google's message-list guide lists a Google Workspace Business or Enterprise account as a prerequisite; a consumer Gmail account is outside that documented prerequisite, so do not promise equivalent support. [List messages guide](https://developers.google.com/workspace/chat/list-messages)
2. Use a Google Cloud project with Chat API enabled and its Chat app name, icon, and description configured; configure the OAuth consent screen and create a desktop OAuth client. The app acts with the user's permissions; domain-wide delegation is an optional administrator mechanism, not a prerequisite for this approach. [API setup prerequisites](https://developers.google.com/workspace/chat/list-messages), [User authentication](https://developers.google.com/workspace/chat/authenticate-authorize-chat-user)
3. Request `https://www.googleapis.com/auth/chat.spaces.readonly` to discover spaces and `https://www.googleapis.com/auth/chat.messages.readonly` to read messages and reactions. Google categorizes the former as sensitive and the latter as restricted. These scopes are not grants limited to two named spaces; the implementation must enforce the two-space allowlist. [Scope definitions](https://developers.google.com/workspace/chat/authenticate-authorize)
4. Authenticate through the system browser with the desktop authorization-code flow and PKCE, then retain the refresh token securely between runs. For Brain, the macOS Keychain is the proposed storage. Browser sign-in here is an OAuth setup step, not browser scraping. [Desktop OAuth](https://developers.google.com/identity/protocols/oauth2/native-app)
5. Address publishing status before relying on unattended sync: external apps left in Testing normally receive refresh tokens that expire after seven days. Tokens can also be revoked or invalidated later, so surface a reconnect state. [OAuth token lifecycle](https://developers.google.com/identity/protocols/oauth2)

Personal-use apps with fewer than 100 users can use Google's verification exemption; internal apps also have an exemption when the project belongs to the organization and the audience is Internal. A public app verification project is therefore not automatically necessary for Brain. [Verification exemptions](https://support.google.com/cloud/answer/13464323)

Workspace administrators can still block internal or external OAuth clients and restrict service access. Google's current overview also documents an admin Trusted status exception to the normal testing token/user limits. **A successful browser login does not demonstrate permission to authorize Brain's OAuth client.** [OAuth states and administrator controls](https://developers.google.com/identity/protocols/oauth2/production-readiness/overview), [API access controls](https://support.google.com/a/answer/7281227)

An externally owned space is not documented as categorically unsupported by the `messages.list` member-access contract. That makes a user-authenticated read worth trying; it is not proof these particular cross-organization spaces will work. Avoid applying Takeout/Vault ownership restrictions to this API without testing.

## Proposed API sync

- **Discover once:** paginate `GET /v1/spaces`, optionally filtering `spaceType = "SPACE"`; match the supplied display names and retain canonical `spaces/...` IDs. The list supports type filtering, not display-name filtering. Ambiguous names need resolution before hardcoding IDs. [Space list reference](https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces/list)
- **Backfill:** paginate each `GET /v1/spaces/{id}/messages`, up to 1,000 messages per page, until `nextPageToken` is absent. Store by canonical message ID. The list supports `createTime` and `thread.name` filters and chronological ordering. System membership announcements are excluded; `showDeleted=true` exposes deletion metadata without deleted text. [Message list reference](https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages/list)
- **Preserve structure:** retain message ID, sender ID, text/formatted text, creation/edit/deletion times, thread ID, `threadReply`, attachment metadata, and emoji summaries. Group the Markdown export by thread. A message resource has current content and last-edit time, not a full edit history. [Message resource](https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages)
- **Incremental updates:** poll space events for message creation/update/deletion and reaction creation/deletion; paginate, process batch events, and checkpoint only after successful local persistence. Events cover the preceding 28 days and return the latest resource state. If Brain has been offline longer, reconcile by re-listing available history. Creation-time-only polling misses changes to old messages. [Space events reference](https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.spaceEvents/list)
- **Reaction identities:** if required, paginate the per-message reactions endpoint; the existing `chat.messages.readonly` scope suffices. [Reaction list reference](https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages.reactions/list)
- **Readable people names:** user-authenticated Chat responses populate `User.name` and `User.type`, not display names/emails. Keep the stable ID and use a verified small local mapping or separately authorized People/Directory lookups. Cross-domain name resolution must be tested, not assumed. [User resource](https://developers.google.com/workspace/chat/api/reference/rest/v1/User)
- **History limits:** inspect `spaceHistoryState`. History-off messages expire after 24 hours; history-on retention depends on organizational retention rules. Neither API reads nor browser scrolling can restore unavailable content. [Space history state](https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces)

For two spaces and a desktop app, periodic polling is the proposed first implementation. A hosted event subscription is unnecessary for the first version.

### Brain integration points

The accompanying local code review identified these proposed touchpoints: `ChatSync.swift` for the channel and exporter runner; `ChatAutoRefresh.swift` for scheduling; `Config.swift` for paths; `MacOSTab.swift` for sync controls; a new `scripts/google_chat_export.py` exporter; and a Google Chat renderer in `process_exports.py`. These are implementation suggestions only; no app implementation was changed in this research task.

## Alternatives

| Option | Fit for Brain |
| --- | --- |
| Browser automation of the signed-in Chat UI | Fallback if permitted API setup is impractical. Must separately prove history coverage, reply expansion, stable message IDs, and repeatable extraction. This is an engineering recommendation, not a live browser finding. |
| Incoming webhook | Wrong direction: sends notifications into a space and cannot receive user messages or retrieve history. [Webhook guide](https://developers.google.com/workspace/chat/quickstart/webhooks) |
| Google Takeout | One-off export, not ongoing sync. Google excludes group messages/spaces created by work or school users from personal Chat history export; organizational exports exclude spaces created outside the domain. [Chat exports](https://support.google.com/chat/answer/10126829) |
| Google Vault | Admin/legal discovery tooling requiring account setup; exports history-on data, excludes messages in externally owned spaces. Poor fit for a personal ongoing channel exporter. [Vault Chat search](https://knowledge.workspace.google.com/vault/search/use-vault-to-search-google-chat) |
| Gmail API | Does not provide Google Chat message search even though the Gmail UI embeds Chat. [Chat search help](https://support.google.com/chat/answer/7655805) |

## Decision tree

1. Confirm the signed-in account and the two space identities.
2. If an authorized desktop OAuth client is already available, run a read-only space/message probe and compare one root message, one reply, and older history with the UI.
3. Otherwise establish whether creating/using a suitable Cloud project and OAuth client is practical for that account. Missing setup alone does not prove the API cannot work.
4. If the probe succeeds, implement API polling with hardcoded verified space IDs and JSON/Markdown outputs consistent with Brain's other channels.
5. If access is denied, distinguish account/client setup, missing membership, and organization policy. Resolve legitimate setup issues; do not reinterpret a policy block as permission to bypass it.
6. If a permitted browser export is the workable route, validate the UI extraction first and then integrate it. Report actual history/reply limitations instead of claiming a complete export.
