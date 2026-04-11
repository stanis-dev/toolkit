# Reply-Drafting Gold Set

Initial draft manifest of real DM / direct-mention cases for evaluating a personal assistant that drafts replies with evidence-grounded retrieval.

## Selection Rules

- Trigger came from a DM, direct chat, or explicit mention in a shared thread.
- A real eventual response from Stan exists in the local corpus.
- The case is useful for measuring edit burden, voice fit, retrieval usefulness, and non-sycophantic judgment.
- This is a draft benchmark, not yet a frozen eval set.

## Items

### G01 — Slack DM: choose Spanish for onboarding buddy chat
- Source: Slack DM
- Task type: reply drafting / preference signal
- Complexity: low
- Trigger from: Javi Quirante at 2025-12-01 11:25
- Trigger: Hello Stanislav! I am Javier Quirante and I have the pleasure of being assigned as your welcome buddy this your first week, do you prefer english or spanish ?
- Actual response at 2025-12-01 11:28: Hola Javier :wink: Las dos opciones son buenas, pero creo que en español será algo más fácil
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Javi_Quirante.md`
- Why it belongs: Tests low-friction style matching, language choice, and warmth in a new DM.

### G02 — Slack DM: ask for a short onboarding call
- Source: Slack DM
- Task type: coordination / concise ask
- Complexity: low
- Trigger from: Javi Quirante at 2025-12-01 11:38
- Trigger: Genial, pues eso, que estoy asignado como tu welcome buddy, así que cualquier duda que tengas o inquietud estoy online para contestarla o si prefieres podemos organizar un google meet y charlar un rato, como prefieras ... a qué proyecto vas?
- Actual response at 2025-12-01 12:08: pues si te va bien, mañana te agradecería una call rápido por meets. No te voy a robar mucho tiempo, porque la mayoría de la dudas se pueden responder async
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Javi_Quirante.md`
- Why it belongs: Tests converting a friendly offer into a bounded scheduling request with your typical brevity.

### G03 — Slack DM: confirm travel availability for Sierra onboarding week
- Source: Slack DM
- Task type: logistics confirmation
- Complexity: low
- Trigger from: Jorge Muñiz Moran at 2025-12-02 15:46
- Trigger: Hola, al final nos están planteando viajar la semana del 15. La semana que viene no pueden. ¿Podrías viajar esa semana? Si no ya sería post navidades.
- Actual response at 2025-12-02 15:47: si, podré viajar sin problema
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Jorge_Muñiz_Moran.md`
- Why it belongs: Simple but high-value acknowledgement case; useful as a baseline for response latency and directness.

### G04 — Slack DM: share backup personal email for Sierra account recovery
- Source: Slack DM
- Task type: sensitive info response
- Complexity: medium
- Trigger from: Jorge Muñiz Moran at 2025-12-03 08:30
- Trigger: Buenos días! Me piden tu email personal para poner como backup de recuperación del correo de Sierra... ¿Me lo puedes pasar porfa?
- Actual response at 2025-12-03 08:30: claro, es stanis.samisco@gmail.com :slightly_smiling_face:
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Jorge_Muñiz_Moran.md`
- Why it belongs: Tests whether the assistant drafts a compliant direct answer without oversharing or adding fluff.

### G05 — Slack group mention: clarify holiday-switch request after onboarding timing changed
- Source: Slack group mention
- Task type: status clarification in group thread
- Complexity: medium
- Trigger from: Paola Morales Laguna at 2025-12-02 17:45
- Trigger: We typically encourage for people to enjoy their Holidays,. If there are no other potential dates with the client, I would need an email from you, @stan sharing with us that you wish you enjoy the Holiday on another date and when would that be.
- Actual response at 2025-12-03 08:19: Good morning. I believe that Sierra communicated they would prefer the onboarding to happen on the week of December 15th, so next week is no longer an option. @Jorge Muñiz is currently working on clarifying the details
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/mpdm-jorge_muniz--paola_morales--stanislav_samisko-1.md`
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Jorge_Muñiz_Moran.md`
- Why it belongs: Good group-thread case where the assistant needs to resolve ambiguity and avoid an unnecessary administrative path.

### G06 — Slack group mention: clarify who owns London onboarding travel logistics
- Source: Slack group mention
- Task type: group coordination / clarification
- Complexity: medium
- Trigger from: Antonio Rodriguez Bosch at 2025-12-05 08:56
- Trigger: Hola, claro podemos ayudarle pero me parec eincreiblemente tarde, juraría nos dijo que la semana del 8 y 15 seguia disponible y ya después de esas se iba a la del 12 de enero, pero teniendo ya a @stan... Si quieren le pregunto a Bhavish
- Actual response at 2025-12-05 09:03: hola chicos. por enter yo un poco el proceso - entiendo que Sierra ha dado el OK para la semana del 15, verdad? La organización del viaje sería por parte de Wizeline o depende también de Sierra?
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/mpdm-jorge_muniz--antonio_rodriguez--stanislav_samisko--maria_esteve-1.md`
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Jorge_Muñiz_Moran.md`
- Why it belongs: Tests group coordination where the right move is not to answer everything, but to surface the dependency clearly.

### G07 — Slack DM: respond to HR follow-up on annual medical recognition
- Source: Slack DM
- Task type: follow-up / expectation setting
- Complexity: low
- Trigger from: Paola Morales Laguna at 2026-01-30 10:48
- Trigger: Hi Stan! I just wanted to follow up on this as I haven't received either you form responses or your waiver for the annual medical recognition, could you help us with this? Thank you!
- Actual response at 2026-02-03 08:46: buenos días Paola. disculpa que haya tardado en responder. seguro eso lo oyes a menudo, sobre todo de la gente de sierra, pero hemos estado un poco a tope :rolling_on_the_floor_laughing: hoy me aseguraré de tener esto solucionado EOD
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Paola_Morales_Laguna.md`
- Why it belongs: Useful for testing apology tone, ownership, and concrete commitment in a lightweight admin reply.

### G08 — Slack DM: diagnose ifeel/Okta access state
- Source: Slack DM
- Task type: diagnostic reply
- Complexity: medium
- Trigger from: Vanessa Díaz de León Agüeros at 2025-12-04 18:36
- Trigger: Stan, entras a ifeel por medio de tu portal de okta y con tu correo de wizeline y que te dice?
- Actual response at 2025-12-04 20:00: no hay ningún tipo de mensaje especial. simplemente me "aterriza" en esta vista:
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Vanessa_Díaz_de_León_Agüeros.md`
- Why it belongs: Tests whether the assistant can answer a troubleshooting question with precise state reporting instead of generic reassurance.

### G09 — Slack DM: explain why vendor docs still do not match observed behavior
- Source: Slack DM
- Task type: evidence-grounded rebuttal
- Complexity: high
- Trigger from: Vanessa Díaz de León Agüeros at 2025-12-09 18:57
- Trigger: Vanessa shares the vendor video and internal docs and implies the setup may already be correct.
- Actual response at 2025-12-09 20:21: por lo que puedo ver del video, al responder las preguntas iniciales la plataforma permite empezar a interactuar. en mi caso cualquier intento me redirige a que elija un plan y sin eso no permite hacer absolutamente nada
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Vanessa_Díaz_de_León_Agüeros.md`
- Why it belongs: Strong candidate for testing whether the assistant can stay polite while pushing back with concrete observed behavior.

### G10 — Slack DM: ask Antonio for the right protocol when Expensify access is still blocked
- Source: Slack DM
- Task type: escalation / process navigation
- Complexity: medium
- Trigger from: Antonio Rodriguez Bosch at 2025-12-15 12:19
- Trigger: Buenas, no me llego nada aun para aprobar o analizar. Saludos. / Si necesitas vea el ticket me tienes que añadir.
- Actual response at 2025-12-17 10:54: Hola Antonio. Sigo sin tener noticias respecto a tener acceso a Expensify. Probablemente no sea algo a gestionar contigo, por lo que si me indicas el protocolo me pondre con ello
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Antonio_Rodriguez_Bosch.md`
- Why it belongs: Tests a common assistant task: turn a stalled admin issue into a crisp next-step request.

### G11 — Slack DM: respond to relocation-interest question about moving to London
- Source: Slack DM
- Task type: interest signal + clarification
- Complexity: high
- Trigger from: Antonio Rodriguez Bosch at 2026-02-13 08:18
- Trigger: Hola Stan como estas? una pregunta rápida sobre Sierra, estarías interesado en cambiar tu residencia a Londres? o es un escenario que no te interesa? estamos barajando algunas estrategias con cliente y antes de fichar a alguien allí estoy preguntando al equipo si esta interesado. Gracias
- Actual response at 2026-02-13 08:39: Buenos días Antonio. La verdad es que es algo me podría interesar
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Antonio_Rodriguez_Bosch.md`
- Why it belongs: Important judgment case: the draft should show openness without overcommitting and should surface key constraints.

### G12 — Slack DM: give the final answer after thinking through the London move
- Source: Slack DM
- Task type: sensitive decision communication
- Complexity: high
- Trigger from: Antonio Rodriguez Bosch at 2026-02-16 12:53
- Trigger: Hola Stan, llegaste a pensarlo?
- Actual response at 2026-02-16 14:18: hola Antonio. si, el finde me tome un buen rato para investigar bien el tema. y al final la verdad es que no voy a poder. Hay un par de cosas que no conseguiría solucionar para poder estar 100% en Londres
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Antonio_Rodriguez_Bosch.md`
- Why it belongs: Tests a nuanced no: clear, polite, and firm without overexplaining.

### G13 — Slack DM: align on Sierra validations context and who should be in the call
- Source: Slack DM
- Task type: project-context scheduling
- Complexity: high
- Trigger from: Antonio Rodriguez Bosch at 2026-03-11 11:57
- Trigger: Hola Stan, perdona que estoy en oficinas de cliente hoy por London y acabo de leerte, claro dime
- Actual response at 2026-03-11 12:02: no te preocupes, cuando tengas la posibilidad de hacer una call ya me dices. La idea es entender mejor el contexto actual con Sierra, sobre todo para las validaciones
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Antonio_Rodriguez_Bosch.md`
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/sierra-validations.md`
- Why it belongs: Good overlap case: the assistant needs to know what “validations” means in this project and ask for the right participants.

### G14 — Slack DM: send a farewell reply to Jorge after access was cut
- Source: Slack DM
- Task type: relationship-preserving reply
- Complexity: medium
- Trigger from: Jorge Muñiz Moran at 2026-02-27 08:22
- Trigger: Hola tio, me han bloqueado ya el ordenador de sierra quería despedirme pero ya no se puede hahah asi que sirva por este medio ha sido un gustazo trabajar contigo estos meses, te va a ir genial y ojala podamos coincidir en el futuro un abrazo enorme
- Actual response at 2026-02-27 08:25: buenos días Jorge! Muchas gracias, tío. Pensaba también que nos despediríamos en la weekly te digo exactamente lo mismo por mi parte - ha sido un gustazo y espero que volvamos a coincidir. Y sobre todo, que la próxima aventura sea la leche! :rocker-1:
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/Jorge_Muñiz_Moran.md`
- Why it belongs: Tests warmth and personal tone without drifting into excessive sentimentality.

### G15 — Teams direct chat: Esen asks for a short call because the shared document is inaccessible
- Source: Teams chat
- Task type: real-time coordination
- Complexity: low
- Trigger from: Esen Bolkar Men at 2026-01-28 12:39Z
- Trigger: Hi Stan, I'm not able to see it. Are you available, can I give you a short call? I'm working on preparing the scenarios as well.
- Actual response at 2026-01-28 12:45Z: sure, we can jump on a call now
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/Chat__66ad9ea2-e8e6-4b7d-a9f8-3bec8dc5659c__4edb6120-4e39-4976-b4ff-6cd97ae32daa.md`
- Why it belongs: Baseline Teams case for fast coordination with minimal verbosity.

### G16 — Teams meeting chat: explain interruption issue as echo-driven false detection
- Source: Teams meeting chat
- Task type: technical explanation
- Complexity: high
- Trigger from: Esen Bolkar Men at 2026-02-12 14:07Z
- Trigger: Stan Samisko (Dış) Esen Bolkar Men I am looking at the interruption issue. it is somewhat related to one of the questions i asked clarification on yesterday - whether we'd want to make the introduction uninterruptible. The conversation registers interruption, may have been noise? or is it a repeated issue? none of them, no repeat, no noise at all actually
- Actual response at 2026-02-12 14:10Z: i just listened to the conversation and there seems to be a rather strong echo which likely was interpreted as customer speaking, which is why agent stopped talking
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/Sierra____Pronet_Weekly_Working_Group.md`
- Why it belongs: Tests whether the assistant can produce a technically grounded diagnosis rather than a vague status update.

### G17 — Teams meeting chat: clarify payment-error handling scope after Bilge asks about point 2
- Source: Teams meeting chat
- Task type: spec clarification
- Complexity: high
- Trigger from: Bilge Göçen at 2026-02-13 14:31Z
- Trigger: Stan Samisko (Dış) Quick question regarding point n2. Esen Bolkar Men, Bilge Göçen We currently instruct the agent to react to other CC_LAST_ERROR messages, for example when it says that the card is expired. Do we also want to avoid reacting to those and still attempt payment? I am asking this because from our con… Hi stan, we clarified all the CC_LAST_ERROR issues in #176
- Actual response at 2026-02-13 14:43Z: great, thank you. fixes for issues 2,3 and 4 are now live an important clarification: point 1 refers to active payment attempts, when provision() is called. my question about point 2 refers to reacting to CC_LAST_ERROR right after we verify customer identity. during standup we spoke that even if customer data is prefetched and we see from CC_LAST_ERROR that their card has insufficient limit error, we should not avoid directly encouraging them to execute payment with the existing card. And Issue #176 is related to payment attempt made during the call and how agent should react to it, correct? Appreciate your feedback, just want to make sure we're perfectly aligned. If so, point 2 still needs clarification
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/Sierra____Pronet_Weekly_Working_Group.md`
- Why it belongs: Strong eval case for precise clarification when the other side is already reasoning in implementation terms.

### G18 — Teams meeting chat: redirect critical issue debugging away from PII in chat
- Source: Teams meeting chat
- Task type: safe debugging guidance
- Complexity: high
- Trigger from: Esen Bolkar Men at 2026-02-16 16:18Z
- Trigger: Stan Samisko Hi Bilge Göçen, Esen Bolkar Men. I need your help with a critical issue that's being reported. last week we implemented a fix for the following issue, which says "Correct action: TASK_ID null gelen durumlarda çağrı müşterinin 4441911'i araması için bilgi verilerek kapatılmalıdır." we're no… @Bilge @Göçen has written me the customer, I'm gonna check and get back with a solution.
- Actual response at 2026-02-16 16:20Z: thanks Esen. I was about to mention that it's best for you to get the data from the conversation linked to the issue directly, to avoid passing PII over a chat
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/Sierra____Pronet_Weekly_Working_Group.md`
- Why it belongs: Useful benchmark for calibrated pushback and safety-aware communication.

### G19 — Teams standup: propose a better response shape when customer disputes debt
- Source: Teams meeting chat
- Task type: policy / conversation-shape proposal
- Complexity: high
- Trigger from: Bilge Göçen at 2026-02-23 10:47Z
- Trigger: for this specific example we can send the statement mail to the customer @Stan @Samisko. customer did not make a payment and the debt still exists.
- Actual response at 2026-02-23 11:15Z: @Bilge @Göçen tell me if this approach looks correct to you: Customer objects debt: 1. offer to send full statement 2. if customer objects/insists -> immediate transfer currently when customer objects debt we're transferring immediately (many request transfer anyway)
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/Sierra____Pronet_Daily_Standup.md`
- Why it belongs: Tests proposal-writing: concise operational recommendation rather than raw brainstorming.

### G20 — Teams collection calls: respond to token-validity guidance while investigating 401 errors
- Source: Teams meeting chat
- Task type: API debugging update
- Complexity: high
- Trigger from: Bilge Göçen at 2026-02-09 13:25Z
- Trigger: hi @Stan @Samisko, we use the login method to obtain a token. Our token is valid for 3 months, so you don't need to request a new token for every web request.
- Actual response at 2026-02-09 16:08Z: I'm investigating 401 error in sms link tool, and managed to confirm that the token was freshly obtained from a successful Login call moments before and had no differences to other calls, which had no issues with auth even within the same session. While reviewing the integration documentation, I noticed the sample JWT token contains a non-ASCII character — a Turkish dotless ı (U+0131) instead of a regular ASCII i in the signature portion Token provided in the docs: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IlNpZXJyYSIsIm5hbWVpZCI6IjUwNTM4IiwiVXNlcklkIjoiNTA1MzgiLCJuYmYiOjE3NjQ4MzY4ODYsImV4cCI6MTc5NjM3Mjg4NiwiaXNzIjoicGNtLnByb25ldC5jb20udHIiLCJhdWQiOiJwY20ucHJvbmV0LmNvbS50ciJ9.woeOIJ_-fdwelkrtnyolrıegrQY -> The relevant bit: fdwelkrtnyolr----->ı<----egrQY Could you confirm that this is not a typo? If it isn't - does the JWT logic account for normalisation with CultureInfo.InvariantCulture ?
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/Sierra___Pronet_Collection_Calls.md`
- Why it belongs: Tests evidence-based debugging language when the assistant should explain what it already verified.

### G21 — Teams collection calls: handle follow-up about missing sample token and point back to the right document
- Source: Teams meeting chat
- Task type: artifact grounding
- Complexity: medium
- Trigger from: Bilge Göçen at 2026-02-09 16:23Z
- Trigger: Hi Stan, there should not be a sample token in the documents I sent you. I had shared our username and password with German. Using these credentials, you should be able to obtain a token that is valid for 3 months and compliant with global standards, and then call all collection methods. The sample token you shared may have been written incorrectly in an internal document.
- Actual response at 2026-02-09 16:34Z: This is the document that I mentioned previously
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/Sierra___Pronet_Collection_Calls.md`
- Why it belongs: Good case for testing whether the assistant can answer with the right artifact reference instead of restating the whole issue.

### G22 — Teams collection calls: publish a structured fix update after Fatma says Stan will send it
- Source: Teams meeting chat
- Task type: status broadcast
- Complexity: high
- Trigger from: Fatma Akcay at 2026-02-10 09:46Z
- Trigger: Hi Esen we did fix some issues yesterday @Stan @Samisko will send an update here
- Actual response at 2026-02-10 10:19Z: Hi @Esen @Bolkar @Men and @Bilge @Göçen. Thank you for testing and providing feedback to keep improving agent's behavior. Issue #143 - we added new behavior to address the scenario and also added new simulation for future regression control (no task_id -> redirect to CS, end call). This is ready to be tested. Issue #146 had two aspects to it: API not finding a document for use request will no longer crash agent. Agent interpreted that customer was requesting a document for year 2023 and since there likely were none, api returned 404 - not found. The case wasn't handled gracefully, which is why the call immediately ended. Transcription correctly identified user speaking "2.026" but LLM ended up correcting that to 2023. We're investigating and will have first fixes for this soon. Issue #145. We investigated this thoroughly and were unable to reproduce the issue in production — the same user successfully received the SMS link in subsequent tests. We added logging to monitor login calls more closely and will continue monitoring, and if intermittent authentication errors appear again, we'll have better data for debugging. Issues #142, #144 - We have updated the spelling format to the one suggested (Mardin'in M'si, Edirne'nin E'si...) and indicated to the agent that the colons are not clearly formatted for voice, so the agent does not use those in the responses. fixed "hatta" issue (remove from fixed responses + synthesis rewrite to hat-ta in case LLM generates a response containing the word adhoc), "SMS" synthesis rewrite IBAN readout improved
- Supporting context:
  - `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/Sierra___Pronet_Collection_Calls.md`
  - `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/Sierra____Pronet_Daily_Standup.md`
- Why it belongs: Excellent benchmark for structured update drafting: specific, confidence-calibrated, and useful to multiple stakeholders.
