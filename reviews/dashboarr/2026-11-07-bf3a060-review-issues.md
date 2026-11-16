# Dashboarr: issue drafts, round 2026-11-07-bf3a060-review

Drafts for RenzoBeux/Dashboarr, `main` at `bf3a060a35170ba789f73195e3defaa0703e93e9` (bf3a060), in `testing/FILING.md` §5's form. **Nothing is filed.** No issue, comment, label or reaction goes up until Garrett has read these and said go for the batch, in writing (§8). The repo has no issue template (`reviews/dashboarr/2026-11-07-ai-policy-check.md`), so each draft is §5's form alone. Four drafts; the batch cap is six. Ledger rows: `2026-11-07-bf3a060-review/ledger-rows.jsonl`. Probes: `2026-11-07-bf3a060-review/probes/`.

Before posting, §3's re-check must be made again on the day: the cited lines re-read on the current `main`, and open and closed issues and pull requests searched once more. The searches made 2026-11-08 02:17 UTC (read-only `gh api search/issues` for "demo mode", "demo", "wake on lan import", "import invalid config", "wolDevices", "export settings demo", "AsyncStorage", "poster cache", "CursorWindow", "attachedInstances", "workspace attach", and the 22 open issue titles by eye) found no issue or pull request on any of the four. #168 is the only import-related issue (cross-device import, BSSID pins) and is closed; it is not these.

---

## Draft 1 (DA-L01, with DA-L02 as Related)

**Title:** [Bug] Changing a dashboard or a service while Demo Mode is on overwrites the real configuration, which does not come back when Demo Mode is turned off

**Version:** `main` at `bf3a060a35170ba789f73195e3defaa0703e93e9` (the default branch).

**Summary:** `enableDemoMode` (`store/config-store.ts:2716-2756`) replaces the service instances and strips every dashboard's `attachedInstances` in memory only, with the comment "not persisted", and `disableDemoMode` (`:2758-2762`) reads the real configuration back from storage. But every store setter persists the whole slice it touches without checking `demoMode`: `addWidget`, `removeSlot`, `moveSlot` and `setDashboardActiveInstance` write `state.dashboards` (`:2364`, `:2376`, `:2396`, `:1773`), and `updateInstance` writes the per-kind instance list (`:1649`), which the service editor's switches call on every tap (`components/integrations/service-editor.tsx:1006-1037`). So one widget added, or one "Use remote" toggle flipped, while Demo Mode is on writes the demo state over the real one, and turning Demo Mode off hydrates the demo state as if it were the user's.

**Result:** after a Demo Mode session in which a dashboard was touched, every curated workspace comes back as auto-attach (all instances on every workspace); after a service switch was touched, the real server of that kind is replaced by a "demo.local" instance and its API key is left under an id nothing reads any more. The guide says "Turn it off and everything comes back exactly as it was" (`docs/guide.html:263`).

**Where:** `store/config-store.ts:2735-2740`, `:2364`, `:2376`, `:2396`, `:1773`, `:1649`, `:1561`, `:2758-2762`; `components/integrations/service-editor.tsx:1006-1037`; `store/config-store.ts:1096-1101` (secrets are loaded by instance id on hydrate).

**Steps:**
1. Have two workspaces with explicit attachments (for example Home attached to one Radarr, Cabin to another) and a real Radarr instance configured.
2. Settings > Backup & Storage > Advanced > Demo Mode: on.
3. On the dashboard, add any widget (or reorder one). Then open Settings > Services > Radarr and flip "Use remote" on the (demo) instance.
4. Demo Mode: off.

**Expected:** both workspaces keep their attachments; the Radarr instance is the real one, with its URL and API key.

**Actual:** both workspaces are auto-attach (every instance shows on both); the only Radarr is "Radarr" at `http://demo.local` with no API key, and the real one is gone.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `enableDemoMode`, `addWidget`, `updateInstance`, `disableDemoMode` and hydrate logic over an in-memory store. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe_demo_mode_persist.js`, Node 24, standard library only):
```
1. Real configuration after launch:
  dashboard dash-home: attachedInstances=["radarr-home"] widgets=1
  dashboard dash-cabin: attachedInstances=["radarr-cabin"] widgets=0
  radarr instance: id=radarr-home name="Radarr Home" localUrl=http://10.0.0.5:7878 useRemote=false

2. Settings > Backup & Storage > Advanced > Demo Mode: on
   In memory while Demo Mode is on:
  dashboard dash-home: attachedInstances=undefined widgets=1
  dashboard dash-cabin: attachedInstances=undefined widgets=0
  radarr instance: id=uuid-1 name="Radarr" localUrl=http://demo.local useRemote=false

3. While in Demo Mode: add a widget to the active dashboard, and flip 'Use remote' on the (demo) Radarr
   persisted app.dashboards: [{"id":"dash-home","name":"Home","widgets":[{"id":"slot-1","widgetId":"calendar"},{"id":"uuid-2","widgetId":"downloads"}]},{"id":"dash-cabin","name":"Cabin","widgets":[]}]
   persisted services.radarr: [{"id":"uuid-1","enabled":true,"name":"Radarr","localUrl":"http://demo.local","remoteUrl":"","useRemote":true,"ignoreCertErrors":false}]

4. Demo Mode: off (disableDemoMode -> hydrate)
   Real configuration after Demo Mode is turned off:
  dashboard dash-home: attachedInstances=undefined widgets=2
  dashboard dash-cabin: attachedInstances=undefined widgets=0
  radarr instance: id=uuid-1 name="Radarr" localUrl=http://demo.local useRemote=true

Expected: Home attached ['radarr-home'], Cabin attached ['radarr-cabin'], radarr instance id 'radarr-home' at http://10.0.0.5:7878
Actual:   Home attached undefined, Cabin attached undefined, radarr instance id 'uuid-1' at http://demo.local
RESULT: real workspace attachments and the real Radarr connection were overwritten by Demo Mode edits
```

**Related:** the same cause reaches `removeInstance` (`:1561` writes an empty list, so hydrate seeds a fresh disabled instance in place of the real one) and `setDashboardActiveInstance` (`:1773` pins a demo UUID that is stale once Demo Mode is off, so the kind falls back to its first attached instance instead of the one the user had chosen).

**Possible fix:** either keep the real slices aside while Demo Mode is on (snapshot on enable, restore on disable, and have the setters write to the in-memory copy only), or make `setJSON` of the services and dashboards keys a no-op while `demoMode` is true, as `services/backend-backup.ts:79` and `services/backend-api.ts:275` already do for the uploads. A store test: enable demo, call `addWidget` and `updateInstance`, disable demo, and assert the dashboards' `attachedInstances` and the instance list equal what was persisted before.

---

## Draft 2 (DA-L03)

**Title:** [Bug] "Export settings" while Demo Mode is on writes a backup of the demo data, without the real servers, keys or workspace attachments

**Version:** `main` at `bf3a060a35170ba789f73195e3defaa0703e93e9` (the default branch).

**Summary:** `exportConfig` (`store/config-store.ts:2764-2801`) encrypts `buildExportPayload()` (`:3088-3113`), which reads the live store. While Demo Mode is on the live store holds the demo instances, an empty `instanceSecrets` map and dashboards with their `attachedInstances` removed (`:2718-2728`, `:2735-2740`, `:2749-2751`). The continuous backend backup checks for this and skips (`services/backend-backup.ts:79`, and the guide: "Demo Mode never uploads"); the file export has no such check, and its row sits on the same screen as the Demo Mode switch (`app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:131-137`, `:153-165`).

**Result:** the user keeps a passphrase-protected backup that looks right and contains one "demo.local" instance per service, no API keys and no workspace attachments. Restoring it later replaces their configuration with that.

**Where:** `store/config-store.ts:2764-2801`, `:3088-3113`, `:2716-2756`; `services/backend-backup.ts:79`; `app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:131-165`.

**Steps:**
1. Configure at least one real service with an API key.
2. Settings > Backup & Storage > Advanced > Demo Mode: on.
3. On the same screen, tap "Export settings", authenticate, choose a passphrase, save the file.
4. Later (Demo Mode off, or on another phone), "Import settings" with that file.

**Expected:** the export refuses while Demo Mode is on, or exports the real configuration, as the backend upload does.

**Actual:** the export succeeds; the file holds the demo instances and no secrets; the import replaces the real configuration with them.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `enableDemoMode` and `buildExportPayload` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (step 2b of `probe_demo_mode_persist.js`):
```
2b. While in Demo Mode: Settings > Backup & Storage > Export settings (same screen as the Demo Mode toggle)
   exported services.radarr: [{"id":"uuid-1","enabled":true,"name":"Radarr","localUrl":"http://demo.local","remoteUrl":"","useRemote":false,"ignoreCertErrors":false}]
   exported secrets: {}
   exported dashboards attachedInstances: [null,null]
```

**Possible fix:** in `exportConfig`, return early with a toast while `demoMode` is true (the check `services/backend-backup.ts:79` makes), or disable the Export row while the switch is on. A test: enable demo mode, call `exportConfig`, and assert nothing is written (or that the payload equals the persisted configuration).

---

## Draft 3 (DA-L04, with DA-L05 as Related)

**Title:** [Bug] A Wake-on-LAN device saved with a port such as 70000 makes every later config backup impossible to restore ("Config wolDevices entry is invalid")

**Version:** `main` at `bf3a060a35170ba789f73195e3defaa0703e93e9` (the default branch).

**Summary:** The Wake-on-LAN editor saves a device after checking only that name and MAC are non-empty; the port becomes `Number(port.trim()) || 9` (`app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx:80-92`), so 70000, 9.5 or -7 are stored and shown with a success toast. The export writes the payload as it is (`store/config-store.ts:2764-2781`; `buildExportPayload` at `:3088-3113` runs no validation), and so does the backend backup upload (`services/backend-backup.ts:40-51`). Only the import validates: `coerceWolDevice` (`store/config-schema.ts:172-189`) requires an integer port 1 to 65535, a MAC of at most 32 characters, a broadcast address of at most 45 and a name of at most 200, and one failing device throws for the whole file (`:613-622`). The same validator runs in the backend's web editor when it opens a slot (`backend/dashboarr-backend/web/src/editor/session.ts:77`).

**Result:** every backup made after that device was saved, file or backend slot, fails to restore with "Config wolDevices entry is invalid" (`backup.tsx:117` shows the message); nothing from it is restored, and the user has no hint which device or field is at fault. The same gap exists for a service name longer than 200 characters (no `maxLength` in `components/integrations/service-editor.tsx`; coercer `:76`) and for a custom header value over 4096 characters or a name over 200 (`custom-headers.tsx:28-41` checks only the name's characters and CR/LF; `coerceHeaderMap` at `:62-67`).

**Where:** `app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx:80-92`; `store/config-schema.ts:172-189`, `:613-622`; `store/config-store.ts:2764-2781`, `:3088-3113`; `services/backend-backup.ts:40-51`.

**Steps:**
1. Settings > Network > Wake on LAN: add a device with name "NAS", MAC `AA:BB:CC:DD:EE:FF`, port `70000`. It saves ("NAS added").
2. Settings > Backup & Storage > Export settings; save the file.
3. On the same or another phone, Import settings with that file.

**Expected:** the editor refuses the port, or the import restores everything else and skips or clamps the device.

**Actual:** the import fails with "Config wolDevices entry is invalid" and restores nothing.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the editor's save, `coerceWolDevice` and the import loop. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe_wol_import.js`):
```
port typed as 70000
  editor: success: NAS added; stored device = {"id":"wol-1","name":"NAS","mac":"AA:BB:CC:DD:EE:FF","port":70000}
  later restore of the export: import REJECTED: Config wolDevices entry is invalid
port typed as 9.5
  editor: success: NAS added; stored device = {"id":"wol-1","name":"NAS","mac":"AA:BB:CC:DD:EE:FF","port":9.5}
  later restore of the export: import REJECTED: Config wolDevices entry is invalid
port typed as -7
  editor: success: NAS added; stored device = {"id":"wol-1","name":"NAS","mac":"AA:BB:CC:DD:EE:FF","port":-7}
  later restore of the export: import REJECTED: Config wolDevices entry is invalid
broadcast address 46 chars
  editor: success: NAS added; stored device = {"id":"wol-1","name":"NAS","mac":"AA:BB:CC:DD:EE:FF","broadcastAddress":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
  later restore of the export: import REJECTED: Config wolDevices entry is invalid
valid device (control)
  editor: success: NAS added; stored device = {"id":"wol-1","name":"NAS","mac":"AA:BB:CC:DD:EE:FF","broadcastAddress":"10.0.0.255","port":9}
  later restore of the export: import accepted

Expected: a device the editor saved with a success toast restores with the rest of the config
Actual:   4 of 4 editor-accepted devices make the whole import throw
```

**Related:** a service URL stored without a scheme (older installs; `getActiveUrl` normalizes it on read, `store/config-store.ts:2615-2623`, and nothing rewrites it in storage) is exported as stored and rejected by `isHttpUrlOrEmpty` (`store/config-schema.ts:41-50`, `:77-78`): `new URL("192.168.1.10:7878").protocol` is `"192.168.1.10:"`. That backup fails with "Config services.<kind> entry is invalid" (reading only, no probe).

**Possible fix:** validate the payload at export time (run `validateExportPayload(buildExportPayload())` before encrypting, and name the field in the error), give the editors the coercer's limits (integer port 1 to 65535; the length caps), and normalize stored URLs once on hydrate. A test: save a device with port 70000 through the editor's path, export, import, and assert the import succeeds or the editor refused.

---

## Draft 4 (DA-L06)

**Title:** [Bug] Removing a home network leaves workspaces that had selected it pinned to "always remote", and adding the same WiFi back does not undo it

**Version:** `main` at `bf3a060a35170ba789f73195e3defaa0703e93e9` (the default branch).

**Summary:** A workspace's home-network selection is a list of network ids (`dashboard.homeNetworkIds`). `removeHomeNetwork` (`store/config-store.ts:1945-1953`) only filters the global list; the ids in every dashboard stay. A list whose ids are all gone resolves to no home network (`lib/network.ts:77-88`), which `workspaceForcesRemote` (`lib/url-validation.ts:128-135`) and `getActiveUrl` step 2 (`store/config-store.ts:2636-2637`) treat as "always remote", global auto-switch on or off. `addHomeNetwork` (`:1918-1927`) mints a new id, so re-adding the same SSID does not reconnect the selection. The import path has a repair for exactly this state, `repairOrphanedHomeNetworkSelection` (`:700-712`), whose own comment calls it "silently breaking local URLs with no way for the user to recover"; the delete path does not run it.

**Result:** after removing and re-adding a home network, every service in such a workspace is reached through its Remote URL on the home WiFi; a service with only a Local URL gets `""` from `getActiveUrl` and fails with "No URL configured" (`lib/http-client.ts:544-546`), showing as offline. The delete confirm says only "Stop treating X as a home network?" (`home-networks.tsx:624-627`). Recovery is possible but hidden: open the workspace editor and choose the networks again.

**Where:** `store/config-store.ts:1945-1953`, `:1918-1927`, `:700-712`, `:2636-2637`; `lib/network.ts:77-88`; `lib/url-validation.ts:128-135`; `lib/http-client.ts:544-546`.

**Steps:**
1. Settings > Network > Home Networks: one network, "Casa". In a workspace's editor, select Casa as its home network (so `homeNetworkIds` is `[Casa's id]`).
2. Home Networks: remove Casa. Add Casa again (same SSID).
3. Open that workspace on the Casa WiFi.

**Expected:** the workspace is at home on Casa again, or at least falls back to all home networks, as it would after an import.

**Actual:** the workspace keeps the dead id, resolves to no home network and uses Remote URLs; services with only a Local URL show offline.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `addHomeNetwork`, `removeHomeNetwork`, `resolveEffectiveHomeNetworks`, `workspaceForcesRemote` and `repairOrphanedHomeNetworkSelection` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe_home_network_delete.js`):
```
1. Before: Casa saved, Home workspace selects Casa
  saved networks: ["net-1:Casa"]
  workspace "Home" homeNetworkIds=["net-1"] -> effective home networks ["Casa"], forcesRemote=false
2. After removing Casa
  saved networks: []
  workspace "Home" homeNetworkIds=["net-1"] -> effective home networks [], forcesRemote=true
3. After adding Casa back
  saved networks: ["net-2:Casa"]
  workspace "Home" homeNetworkIds=["net-1"] -> effective home networks [], forcesRemote=true
4. Same dashboards through repairOrphanedHomeNetworkSelection (import only): homeNetworkIds=undefined, forcesRemote=false

Expected: after re-adding Casa the Home workspace is at home on Casa again (or at least uses all networks)
Actual:   Home workspace keeps the dead id ["net-1"], effective home networks [], forcesRemote=true: every service in it uses its Remote URL on the home WiFi, for good
```

**Possible fix:** in `removeHomeNetwork`, prune the id from every dashboard's `homeNetworkIds`, and when a list becomes empty by pruning (not by the user's choice) drop the key so the workspace uses all networks, as `repairOrphanedHomeNetworkSelection` does on import; or warn in the delete confirm which workspaces select this network. A store test: select a network in a workspace, remove it, assert `workspaceForcesRemote` is false.

---

## Not filing

- **DA-L05** (schemeless stored service URL rejected on import): filed inside Draft 3's *Related* rather than on its own, since the cause is the same (export is never validated or normalized; import is strict). If Garrett prefers one issue per path, it splits out cleanly; evidence is reading only.
- **DA-L07** (unbounded poster cache in one AsyncStorage row; storage writes never awaited or checked): `crash`, reading only. The size at which Android's 2 MB cursor window or the 6 MB store limit is reached was not measured (about 7,000 distinct downloads for the first), so it stays in the ledger until a measured case exists.
- **DA-L08** (import with a backup that has no `notificationSettings` leaves the previous device's settings in storage; they come back on relaunch): `wrong-result`, reading only, settings toggles only; small, and FILING §4 would allow it, but it is not worth a maintainer's attention on its own. Hold for a later batch or fold into a fix of the import path.
- **DA-L09** (import wipes secrets and rewrites service lists before the fallible steps): `data-loss` by class, but no failing step was demonstrated; reading only. Hold.
- **Security paths** (Plex/Jellyfin/Emby/Seerr/Pi-hole/Beszel sign-in, HTTP Basic and Digest, the device-unlock gate, backend pairing, bearer and web login): read for security only, nothing found that would be a defect; details in the round report, for Garrett, never a draft.
