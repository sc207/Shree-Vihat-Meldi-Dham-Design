## 0B. v11 — Control Centre and WhatsApp queue recovery (15 Nov 2026; overrides 0A where they differ)

Status: **design and prototype only.** No application code, database, feature flag, GitHub, staging, production or WhatsApp setting has been changed. Every item below needs separate, explicit approval before implementation.

### 0B.1 Owner decisions applied
1. **WhatsApp capacity never closes Seva registration.** Registration acceptance and WhatsApp delivery are independent. This replaces 0A.2 rows 2 and 3 where they tied the daily registration limit to WhatsApp ("દૈનિક મર્યાદા = WhatsApp મર્યાદા"). The daily registration limit is now set by the Super Admin on its own; the message policy only changes how many registrations can be confirmed the same day.
2. **One Control Centre (નિયંત્રણ કેન્દ્ર), every ON/OFF switched there with a toggle** (owner, 15 Nov: "on off ek j jagya e thi toggle thi thai javu joie"). Groups: Website · Seva registration · WhatsApp · Modules · System status. Each switch shows its real current state.

**Code note** — (read-only check of `feature/admin-idcard-mangalarohan`, 15 Nov): `server/wa-budget.js` / `wa-budget-sql.js` contain a `registration_holds` hold with reason `wa_budget` that would close registration when the WhatsApp budget is full. It is **not wired** into the public form today (`holdSql` is not called by the server). Implementation must keep it unwired or remove it, and add a test that a full WhatsApp budget leaves registration open.

### 0B.2 Control Centre — rules
- Route `#/control` (menu: કામ → નિયંત્રણ કેન્દ્ર, second item; phone: "વધુ" first item; the dashboard queue chip opens the WhatsApp queue).
- **Every ON/OFF is a toggle in this one screen.** No switch lives anywhere else; other screens (e.g. "નોંધણી નિયંત્રણ") only link here for switches and keep numbers such as the daily limit.
- Each row: name, one-line meaning, current state pill (read from the server, never assumed), level pill, and the toggle. Tapping the name opens details: who may change it, what changing it does, why it is locked (if it is), last changes from the audit log.
- Tapping a toggle never switches at once. It opens a confirmation: "<name>: ચાલુ → બંધ?", what will happen, reason (required, saved in the audit log), plus what the level requires. The server re-checks permission and the current version; if someone else changed it meanwhile, nothing changes and the new state is shown.
- A toggle that cannot be changed is shown greyed with a lock and the reason (for example "Cloud API સેટ નથી (સર્વર મર્યાદા)", "પહેલાં વેબસાઇટ જાહેર કરો", "પહેલાં ભક્ત યાદી ચાલુ કરો"). Tapping it opens the details, not the confirmation.

Four levels, always labelled:

| Level | Who | Confirmation |
|---|---|---|
| તરત (operational) | Super Admin, Admin | reason; critical ones also a typed word ("હા"; Emergency Stop "રોકો") |
| માલિક સ્તર (owner level) | Super Admin only | reason + Super Admin authenticator code (6 digits) + typed "હા" for critical ones |
| મોડ્યુલ (module) | Super Admin only | reason + authenticator code; only within the server upper limit |
| ફક્ત સ્થિતિ (read-only) | — | none; display (some open a screen, e.g. the queue) |

Rows (sample states in the prototype; the server shows real values):
- **Website:** website public (owner level, critical; locked while emergency private is on) · emergency private (owner level, critical; forces private) · ceremony page (owner level; turning it on does not make the site public) · inauguration record (read-only) · section show/hide for ઇતિહાસ, દર્શન, ગેલેરી, નવું મંદિર, સેવા નોંધણી, WhatsApp સમુદાય, સંપર્ક (owner level; new).
- **Seva registration:** effective state (read-only, with the blocking reason) · website registration (owner level, critical; locked until the site is public and the consent text is approved) · panel intake (operational, critical) · each festival day 2–8 Feb (operational) · daily limit (read-only here, link) · "WhatsApp capacity full → registration stays open" (read-only, owner decision) · consent version (read-only).
- **WhatsApp:** sending on/off (operational; locked during Emergency Stop) · Emergency Stop (operational, critical, red toggle) · live sending vs test mode (owner level, critical; locked until the Cloud API is configured) · queue, Meta tier, templates (read-only, links).
- **Modules:** SEVA_V2 (critical), TEAMS, DEVOTEES, PADHRAMNI and INVITATIONS (locked while DEVOTEES is off), WHATSAPP_MGMT, CEREMONY_REHEARSAL (locked: server limit off). ADMIN_PANEL is shown on and locked: the panel cannot switch itself off.
- **System:** database, `/healthz`, two-step verification, last backup (read-only).

**Implementation consequence (needs separate approval; nothing changed):** today the website, registration and ceremony switches live on `/website-control` and the modules are Render environment variables. To make them toggles here, they move into database-backed settings that the panel reads and writes, with these safety rules:
- Render environment values stay as the **upper limit**: a module the server has off cannot be switched on from the panel (shown locked). `WEBSITE_EMERGENCY_PRIVATE` in Render stays as the last-resort override above every toggle.
- The website reads the setting with a short cache and fails closed (private) if it cannot read it.
- `/website-control` becomes a fallback or is retired (owner's choice when implementing).
- Every change is versioned and audited (who, when, from → to, reason).

### 0B.3 WhatsApp queue and recovery (WhatsApp → "કતાર અને ફરી પ્રયાસ")
Flow: registration saved → eligibility and consent (no WhatsApp consent → no message is created; refusal/STOP → blocked; test mode and number not on the allow-list → blocked) → queued (one event = one message, unique key such as `out:reg:<id>:received`; waits with a visible reason if the approved template is missing) → capacity check (none → "ક્ષમતાની રાહ"; paused or Emergency Stop → nothing is sent) → capacity returns (priority registration → team → others) → send (atomic claim, one worker) → result (sent → delivered → read; temporary error → retry by rule; permanent error → failed; no answer → "result unknown", never retried automatically) → expiry (stale messages are not sent).
States shown: રાહમાં, ક્ષમતાની રાહ, કતારમાં, ફરી પ્રયાસ નક્કી, મોકલાયો, પહોંચ્યો, નિષ્ફળ, રોકાયેલો, સમય પૂરો, પરિણામ અજાણ્યું; plus "no consent: no message" count.
Three different things are shown separately and never mixed:
1. **Meta messaging limit** — unique users reached with messages outside a customer-service window in a moving 24 h, set for the whole business portfolio (tiers 250 · 2,000 · 10,000 · 100,000 · unlimited; this account TIER_250). No fixed midnight reset; the panel shows only an estimate ("when the oldest counted message passes 24 h") and says it is an estimate.
2. **The panel's internal budget** — 200 attempts and 200 unique recipients per rolling 24 h, 50 held for registration and team messages (current code defaults, editable later).
3. **Customer-service window** — 24 h after the devotee's last message to the temple, free-form replies are possible; outside it only approved templates. Registration messages are templates, so the window is not a "reset".
Retry rules: 130429 and 131000/131016 → automatic retry with back-off (1, 5, 15, 60 min; max 6); 131049 → once after 24 h, then failed; 131048 → pause the whole queue and alert, no automatic retry; 131026 → failed, manual only after the number is corrected; 131050 / STOP → blocked and recorded as a refusal; 132000/132001 → wait until the template is fixed; timeout / unknown → never automatic (matches the existing code rule).
Duplicate prevention: unique key per event, the same key on every retry, atomic claim from `pending`, an attempted message never returns to the queue (existing triggers).
Emergency Stop: stops every WhatsApp send (registration, team, invitations, retries) at once; registration stays open; nothing is lost; resuming needs a reason and confirmation; both are audited.
Admin visibility: Dashboard hero chip "WhatsApp કતાર · N રાહમાં", Control Centre tile, queue tab counters and filters, message detail with the full timeline and only the actions that are safe for that state.
Never: bypass consent, template approval, Meta rate limits or quality rules; send free-form messages outside the customer-service window; auto-retry an unknown result.

### 0B.4 Other requirements — where they stand (design)
| Requirement | Code today (read-only check) | Prototype v11 | Next |
|---|---|---|---|
| Seva and Team separate | Public form (SEVA_V2): dates, time, photo, consent, optional WhatsApp consent; **no Seva choice**. Admin assigns Seva (`registration_sevas`) and Team (`seva_assignments`) separately. No auto-assignment in code. | Planner "આપમેળે ભરો" is now shown as **off, approval pending** | Keep manual until the owner approves auto-assignment |
| Attendance 2–8 Feb by day, team, member | Present / absent with reason; "not recorded" is never absent; append-only `seva_attendance_history` | Present/absent/pending, QR, team table, A4 sheet | Add a "correction history" sheet per member |
| WhatsApp safety | Test mode + allow-list, live switch Super Admin only, consent and template checks | Shown in Control Centre | Decide App + API coexistence (0B.5) |
| Padhramni (one host) | Staff entry, Maps link, Calendar, status history; no duration; no separate digital approval | Full workflow | Add Maps and "add to calendar" buttons on the detail |
| Reports and audit | Audit log exists | Audit filters by area | Add categories: Seva, Team, WhatsApp send, ID card handover, attendance correction |
| WhatsApp Community and groups | Not built | Not yet | Full design after confirmation (0B.5) |
| Invitation patrika, village cards | Manual campaigns and hand-over records; nothing is sent | 6-step flow, village cards | Contacts → approval → send → tracking review |
| QR attendance identity | Card QR = SEVA number | QR scan screen | Bind scan to the registration and record who scanned |
| ID card collection | 8 states in code | 8 states, collection details, reprint | Hand-over record with person and time |
| Roles | Five roles in `server/admin/roles.js` | Settings → roles | A role × permission matrix screen |

### 0B.5 Open owner decisions
~~1. Where website public/private is switched~~ — **decided 15 Nov:** every ON/OFF is a toggle in the Control Centre (0B.2).
1. Section show/hide: are the seven sections above the right list, and should a hidden page show "વિગત ટૂંક સમયમાં" (prototype) or disappear?
2. After the move: keep `/website-control` as a fallback, or retire it?
3. Message expiry: after how long is an unsent "નોંધણી મળી" no longer sent (proposal: 72 hours, or as soon as a newer message about the same registration supersedes it)?
4. Retry limits and back-off: approve the table in 0B.3.
5. Existing WhatsApp Business App: move the number to the API with coexistence, or use a separate number for the API?
6. Public success page wording when WhatsApp is delayed (proposal: "નોંધણી મળી ગઈ છે. WhatsApp પુષ્ટિ થોડા સમયમાં મળશે.") — needs the trust's approval.
7. Who may use Emergency Stop: Super Admin and Admin (as `wa.mode` today) or Super Admin only?
8. WhatsApp Community: add the full design now (see recommended flow in the hand-off note)?

### 0B.6 WhatsApp Community and groups — recommended flow (not built; needs approval)
- Groups and the Community are created and owned on the temple's own WhatsApp by a person. The panel never creates groups or adds anyone. (The Cloud API Groups feature is limited to small groups and special account status, so it is not used for festival groups.)
- **Group directory** in the panel: group name, purpose (Community announcements · Seva · Team), invite link (stored encrypted, shown masked, replaceable after a reset), group lead and deputy (taken from team leaders), status (active · closed).
- A volunteer becomes **eligible** for a group only after the registration is accepted and a team is assigned (Seva and Team stay admin decisions).
- The link reaches the volunteer either by an approved WhatsApp template that carries the link (needs template approval and the volunteer's WhatsApp consent) or personally from the team lead.
- Statuses: લિંક મોકલવાની બાકી → લિંક મોકલી (who, when, how) → જોડાયા (recorded by the lead or an admin, with date) · જોડાયા નથી · બહાર નીકળ્યા. The panel never says "added automatically"; "joined" is only what a person confirmed.
- Link reset: if a link leaks, the group admin resets it in WhatsApp; the panel stores the new link and marks earlier shares "જૂની લિંક".
- Privacy: members of a group see each other's numbers — the consent wording must say so; a team coordinator sees only the groups of the teams linked to the account.
- The public website button "WhatsApp સમુદાયમાં જોડાઓ" stays the general Community link (owner-approved), separate from Seva and team groups.
- Our flow today: nothing in code; only the public website button exists in the design.
