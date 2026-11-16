# Review of RenzoBeux/Dashboarr at bf3a060
Started: 2026-11-08 11:33 CST. Finished: 2026-11-08 11:52 CST.

# Findings

## 1: A Wake-on-LAN device with an odd port or a long MAC makes every backup unrestorable
Severity: data-loss
Where: app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx:80-92, store/config-schema.ts:172-186, store/config-schema.ts:613-620, at bf3a060
What the user loses: the whole configuration backup. The export file and the continuous backend backup both carry the device exactly as saved, and the import validator rejects the entire file on that one entry, so services, API keys, dashboards and home networks cannot be restored on a new phone.
Steps:
1. Settings → Wake on LAN → Add. Name "Media Server", MAC "00:11:22:33:44:55", Port "70000" (or "1.5", "-7", or a MAC pasted with a trailing note). Save. The screen accepts it and toasts "Media Server added".
2. Settings → Backup → Export settings (or leave backend backup on; it uploads the same payload).
3. On a new phone, or after a reinstall, import that file (or restore the backend slot).
Expected: the save path refuses the same values the import refuses (integer port 1-65535, MAC up to 32 characters, name up to 200), or the import drops the one bad device and restores the rest.
Actual: handleSave stores `port: Number(port.trim()) || 9` and `mac: mac.trim()` with no range or length check. On import, coerceWolDevice returns null for that device and validateExportPayload throws "Config wolDevices entry is invalid"; importConfigFromPayload aborts before writing anything, so the restore fails as a whole and the toast reads "Invalid config file". The user learns this only when they need the backup.
Evidence: probe
```
typed port="70000" mac="00:11:22:33:44:55"
  app saves:   {"device":{"id":"wol-1","name":"Media Server","mac":"00:11:22:33:44:55","port":70000}}
  import:      throws "Config wolDevices entry is invalid" (whole backup rejected)
typed port="1.5" mac="00:11:22:33:44:55"
  app saves:   {"device":{"id":"wol-1","name":"Media Server","mac":"00:11:22:33:44:55","port":1.5}}
  import:      throws "Config wolDevices entry is invalid" (whole backup rejected)
typed port="-7" mac="00:11:22:33:44:55"
  app saves:   {"device":{"id":"wol-1","name":"Media Server","mac":"00:11:22:33:44:55","port":-7}}
  import:      throws "Config wolDevices entry is invalid" (whole backup rejected)
typed port="9" mac="00:11:22:33:44:55 (Intel NIC, onboard)"
  app saves:   {"device":{"id":"wol-1","name":"Media Server","mac":"00:11:22:33:44:55 (Intel NIC, onboard)","port":9}}
  import:      throws "Config wolDevices entry is invalid" (whole backup rejected)
```
(scratch/probe-wol-port.js)

## 2: Editing any dashboard while Demo Mode is on wipes every dashboard's instance list
Severity: data-loss
Where: store/config-store.ts:2735-2740, store/config-store.ts:2099-2107, store/config-store.ts:2160-2168, store/config-store.ts:2354-2367, store/config-store.ts:1726-1797, store/config-store.ts:1195-1204, at bf3a060
What the user loses: the curated attachment list of every dashboard (which servers belong to "Home" versus "Cabin") and any per-dashboard active-instance pins. After Demo Mode is switched off, every dashboard shows every instance, and the pins fall back to the first instance of each kind.
Steps:
1. Have two or more dashboards with explicit attachments (open a dashboard's editor once and save, or add a dashboard; new ones start with an explicit empty list).
2. Settings → Backup & Storage → Demo Mode on.
3. Do anything that writes dashboards while demo is on: rename a dashboard, change its icon or color, add, move or remove a widget, change a widget's settings, pin a tab, or tap an instance chip on a service tab.
4. Demo Mode off.
Expected: demo mode never writes dashboards to storage, or writes them with the real attachment lists intact. The comment at lines 2732-2734 says the strip is "in memory (not persisted)" and that "the user's stored attachments come back on disableDemoMode → hydrate".
Actual: enableDemoMode deletes `attachedInstances` from every dashboard object held in state. Every dashboard setter (renameDashboard, setDashboardIcon, addWidget, moveSlot, setSlotSettings, setDashboardPinnedTabs, setDashboardActiveInstance, and the rest) maps `state.dashboards` and calls setJSON(STORAGE_KEYS.dashboards, ...) with the whole array, so the stripped list is persisted for all dashboards at once. hydrate reads a missing `attachedInstances` as "every instance attached" (comment at 1316-1320), so there is nothing to restore from. setDashboardActiveInstance additionally writes the demo UUID into the dashboard's `activeInstance` map; after demo the pin points at an instance that no longer exists and the resolver silently picks the first one. Widgets added during demo stay on the dashboard too. Nothing in the dashboard UI is disabled while demoMode is true.
Evidence: probe
```
before demo: [["Home",["qbit-home","radarr-home"]],["Cabin",["qbit-cabin","radarr-cabin"]]]
demo on, storage still intact: [["Home",["qbit-home","radarr-home"]],["Cabin",["qbit-cabin","radarr-cabin"]]]
after demo off: [["Home (renamed)",null],["Cabin",null]]
dashboards whose attachment list was lost: ["Home (renamed)","Cabin"] (undefined = every instance attached)
```
(scratch/probe-demo-dashboard-write.js; `null` is how JSON prints the missing field)

## 3: "Export settings" while Demo Mode is on writes a backup of the demo placeholders, not the user's configuration
Severity: data-loss
Where: store/config-store.ts:2764-2771, store/config-store.ts:3088-3135, app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:46-70, app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:155-167, at bf3a060
What the user loses: their only backup file, and on restore their real configuration. The file is encrypted with their passphrase and named `dashboarr-config.json` like a real one, but holds one fake `http://demo.local` instance per service and no secrets. Restoring it (the import confirm says it "will overwrite all current settings") replaces every real server, API key and password with the demo set.
Steps:
1. Settings → Backup & Storage. Turn Demo Mode on (it is on the same screen, under Advanced).
2. Tap Export settings, enter a passphrase, save the file.
3. Later, on this or another phone, Import settings with that file.
Expected: export is refused or disabled in demo mode, as the other two outbound paths already do: services/backend-backup.ts:79 (`if (config.demoMode) return "skipped"`) and services/backend-api.ts:275 (`if (configState.demoMode) return`), both with comments explaining that the store then holds fake instances.
Actual: exportConfig calls buildExportPayload with no demoMode check. buildExportPayload reads `serviceInstances` and `instanceSecrets` from the store, which enableDemoMode replaced with the demo set and `{}`. The export row is not disabled while demoMode is true.
Evidence: probe
```
demoMode: true
exported services: {"qbittorrent":[{"id":"demo-uuid-1","enabled":true,"name":"qBittorrent","localUrl":"http://demo.local","remoteUrl":"","useRemote":false,"ignoreCertErrors":false}],"radarr":[{"id":"demo-uuid-2","enabled":true,"name":"Radarr","localUrl":"http://demo.local","remoteUrl":"","useRemote":false,"ignoreCertErrors":false}]}
exported secrets:  {}
real instances in the backup file: 0; real secrets in the backup file: 0
```
(scratch/probe-demo-export.js)

## 4: Deleting a movie from a pinned Radarr instance removes the Seerr media record on a different Seerr server
Severity: data-loss
Where: hooks/use-radarr.ts:188-222, services/overseerr-api.ts:86-93, components/dashboard/calendar-card.tsx:262, components/dashboard/still-pending-card.tsx:270, components/dashboard/recently-downloaded-card.tsx:233, app/(tabs)/(dashboard,downloads,calendar,movies,tv,library,music,books,bazarr)/movie/[id].tsx:108, app/(tabs)/(dashboard,downloads,calendar,movies,tv,library,music,books,bazarr)/movie/[id].tsx:518-522, at bf3a060
What the user loses: the media entry, its requests and its availability status on a Seerr server that still has the movie. Seerr's `DELETE /media/{id}` removes the whole record, including request history.
Steps:
1. Configure two Radarr instances (Home and Cabin) and two Seerr instances, each dashboard attached to its own pair; make the Home dashboard active.
2. Open a Cabin movie from a dashboard widget (Calendar, Still Pending and Recently Downloaded route to `/movie/{id}?instanceId={cabin radarr}`), or from a page of the Cabin dashboard.
3. Actions → Delete → confirm. The confirm says "Remove ... from Radarr. Files on disk will be kept."
Expected: the Radarr delete goes to the Cabin Radarr and any Seerr cleanup goes to the Seerr that manages that Radarr, or to none. The confirm names Seerr if Seerr is touched.
Actual: useDeleteMovie deletes on the pinned Radarr instance (`id`) but then calls getSeerrMe(), getMovieDetails(tmdbId) and deleteMedia(mediaId) with no instance id. seerrRequest resolves a missing instance id to `getActiveInstanceId("overseerr")`, the active dashboard's Seerr (Home). The Home Seerr's record for that TMDB id is deleted although the Home Radarr still has the movie. The same happens with one Seerr tracking a 1080p and a 4K Radarr: deleting the 4K copy drops the Seerr record that also covered the 1080p copy. The comment at lines 188-189 calls this "a UX nicety"; the confirm message never mentions Seerr.
Evidence: reading

## 5: A service name over 200 characters, or more than 32 custom headers, makes the backup unrestorable
Severity: data-loss
Where: components/integrations/service-editor.tsx:352-356, components/integrations/service-editor.tsx:903, store/config-schema.ts:76, app/(tabs)/(dashboard,services,settings)/custom-headers.tsx:25-40, store/config-schema.ts:55-67, at bf3a060
What the user loses: the whole configuration backup, as with the Wake-on-LAN device; this is the same validator asymmetry in two other editors. The values are unlikely, but the consequence is total and silent until restore.
Steps:
1. Integrations → a service → paste a name longer than 200 characters (the field has no maxLength; only "Name cannot be empty" is checked) and Save. Or Settings → Custom Headers → add a 33rd header, or one whose value exceeds 4096 characters; the editor checks only the header-name charset and CR/LF.
2. Export settings, or let backend backup upload.
3. Import the file on a new phone.
Expected: the editors cap what the validator caps, or the import trims the one field instead of rejecting the file.
Actual: coerceServiceInstance returns null for `name.length > 200` and validateExportPayload throws "Config services.{kind} entry is invalid"; coerceHeaderMap returns null past 32 headers or a 4096-character value and the import throws "Config globalCustomHeaders is invalid" (or "Config secrets.{uuid} is invalid" for per-instance headers). The whole restore aborts.
Evidence: reading

## 6: Deleting this device's backend backup slot while backup is on is undone seconds later
Severity: stuck
Where: app/(tabs)/(dashboard,services,settings)/backend.tsx:577-586, app/(tabs)/(dashboard,services,settings)/backend.tsx:985-996, services/web-slot-watch.ts:27-37, at bf3a060
What the user loses: the ability to remove their encrypted configuration from the backend without first turning the feature off, and a truthful confirmation: the toast says "Backup deleted" while the slot is being re-uploaded.
Steps:
1. Settings → Backend, with Backup enabled.
2. Manage backups → "Delete this device" → confirm "This cannot be undone."
3. Reopen Manage backups.
Expected: the row is hidden or disabled while backup is enabled (the disable toggle already deletes the slot cleanly), or the delete also stops the continuous upload.
Actual: performDeleteSlot deletes the slot, toasts "Backup deleted", then calls refreshSlots, which calls noteBackupList. noteBackupList sees `backupEnabled` and no slot marked `mine`, clears the last-hash key and calls uploadConfigBackup({ force: true }); the slot reappears. The same re-upload fires on the next backend check even if the sheet is not reopened.
Evidence: reading

# Not reached
- lib/http-client.ts beyond the request path (lines 502-785) and the redaction helpers: the connection probes (testServiceConnection, checkInstanceHealth, classifyUnauthorized), the Seerr login helpers (seerrLogin, seerrLogout, ensureSeerrSession) and the media-server auth helper.
- lib/seerr-session.ts after line 120 and lib/seerr-auth.ts after line 60; lib/beszel-session.ts after line 80; services/pihole-api.ts, services/beszel-api.ts and services/adguard-api.ts beyond their session-cache and cookie-storage parts.
- lib/network.ts beyond isHomeNetwork and resolveEffectiveHomeNetworks; hooks/use-network.ts; lib/vpn.ts; hooks/use-service-health.ts.
- Service API modules other than their delete, queue-removal and manual-import functions: bazarr, bindery, lidarr, tdarr, unraid, glances, tautulli, jellyfin, emby, jellystat, navidrome, tracearr, maintainerr, cleanuparr, autobrr, prowlarr, jackett, nzbhydra2, nzbget beyond its delete mapping, deluge beyond removal, transmission beyond removal, rtorrent beyond erase.
- UI components and screens other than those named in the findings (the settings screens for home networks, shortcuts, headers, WOL, backup and backend; the service editor's save and remove paths; the movie and series detail pages; the torrent downloads view; the dashboard editor's attachment handling). The widget components, the Android home-screen widget (widgets/), native modules (modules/), and hooks not named above.
- Backend: workers/, push/, db/repos other than pairing, devices (createDevice only) and the slot schemas in types.ts; routes/webhooks beyond the secret check in shared.ts; env.ts; the web editor (web/) beyond the first 60 lines of editor/session.ts.
- store/sort-store.ts beyond its types, store/releases-filter-store.ts beyond its header, and the glances, unraid, intro, manual-refresh, widget-visibility and library-view stores.
- All test files, docs/, scripts/, plugins/, patches/, ideas/, TODO.md.
- The root tab layout `app/(tabs)/(dashboard,downloads,...,settings)/_layout.tsx` was absent from this checkout: its path exceeds the Windows path limit, so git reports it as not checked out ("Filename too long"). Nothing in the repo folder was changed by this review.

# Text in the repo addressed to an agent
- CLAUDE.md: "Upstream API docs and per-service gotchas live in the `service-apis` skill (`.claude/skills/service-apis/SKILL.md`). Load it before implementing or debugging any service integration, and prefer fetching the relevant doc page over guessing endpoint shapes." Also the section headings "Theming (Light theme) — MUST follow when writing any new UI", "Confirmations & Dialogs — MUST follow", "Modal sequencing on iOS — MUST follow", "UI Scale (Accessibility) — MUST follow when writing any new UI", "Keyboard Avoidance — MUST follow for any UI with text inputs", and the line "Every modal chain goes through `useModalFlow` (`hooks/use-modal-flow.ts`)."
- .claude/skills/service-apis/SKILL.md front matter: "Use when implementing, debugging, or extending any service integration in services/ or hooks/, or when verifying an endpoint shape, auth scheme, or field type." Body: "When implementing or debugging a service integration, consult the upstream API docs below — these are the authoritative references. Prefer fetching the relevant doc page over guessing endpoint shapes."
- docs/CLAUDE.md: "Keep the site in sync when adding/removing a service, changing major features, or updating download links." and "Verify against the code before changing a documented label, and update the guide when a flow it describes changes."
- README.md lines 260-262 describe a workflow rather than give instructions: "Planning: features and architecture are discussed with Claude in planning sessions ... Implementation: once the plan is settled, Claude implements it. Review: every PR is reviewed separately by Claude and Codex."
None of these were followed; this review was read-only and fetched nothing over the network.
