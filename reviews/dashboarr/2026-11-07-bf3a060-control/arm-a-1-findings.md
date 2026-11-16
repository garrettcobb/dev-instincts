# Review of RenzoBeux/Dashboarr at bf3a060

# Findings

## 1: Adding, moving or removing a dashboard widget while Demo Mode is on erases every workspace's instance attachments when Demo Mode is turned off
Severity: data-loss
Where: store/config-store.ts:2735, store/config-store.ts:2364, store/config-store.ts:2376, store/config-store.ts:2396, store/config-store.ts:1773, store/config-store.ts:2758, at bf3a060
What the user loses: the curated attachment list of every workspace (which Radarr, which qBittorrent belongs to Home and which to Cabin). Turning Demo Mode on deletes `attachedInstances` from every dashboard in memory only; any widget edit then persists that whole dashboards array; turning Demo Mode off reads it back, so every workspace is auto-attach from then on, with every instance on every dashboard. The guide promises "Turn it off and everything comes back exactly as it was" (docs/guide.html:263).
Steps:
1. Have two workspaces with explicit attachments (Home attached to one Radarr, Cabin to another).
2. Settings > Backup & Storage > Advanced > Demo Mode: on.
3. On the dashboard, add any widget (or move or remove one).
4. Demo Mode: off.
Expected: both workspaces keep their attachments.
Actual: both workspaces show every instance; the attachment lists are gone and must be rebuilt by hand.
Evidence: probe
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

2b. While in Demo Mode: Settings > Backup & Storage > Export settings (same screen as the Demo Mode toggle)
   exported services.radarr: [{"id":"uuid-1","enabled":true,"name":"Radarr","localUrl":"http://demo.local","remoteUrl":"","useRemote":false,"ignoreCertErrors":false}]
   exported secrets: {}
   exported dashboards attachedInstances: [null,null]

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

## 2: Flipping a switch on a service while Demo Mode is on replaces the real server of that kind with the demo one, and its API key is never read again
Severity: data-loss
Where: store/config-store.ts:2718, store/config-store.ts:2749, store/config-store.ts:1649, store/config-store.ts:1561, components/integrations/service-editor.tsx:1006, store/config-store.ts:1096, at bf3a060
What the user loses: the saved connection for that service kind (name, local and remote URL, options) and, in effect, its API key: Demo Mode puts one generated "demo.local" instance per kind in memory; the service editor's switches ("Use remote", "Allow invalid certificates", "Remote URL needs a VPN", "Tag added torrents") call the instance updater on each tap, which writes the whole per-kind list to storage; removing the demo instance writes an empty list. When Demo Mode is turned off, that list is what comes back, and secrets are loaded by instance id, so the real key stays in the keychain under an id nothing uses.
Steps:
1. Have a real Radarr configured with an API key.
2. Settings > Backup & Storage > Advanced > Demo Mode: on.
3. Settings > Services > Radarr: flip "Use remote" (or any switch) on the instance shown.
4. Demo Mode: off.
Expected: the real Radarr, with its URL and key, is back.
Actual: the only Radarr is "Radarr" at http://demo.local with no API key; the real connection must be re-entered.
Evidence: probe
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

2b. While in Demo Mode: Settings > Backup & Storage > Export settings (same screen as the Demo Mode toggle)
   exported services.radarr: [{"id":"uuid-1","enabled":true,"name":"Radarr","localUrl":"http://demo.local","remoteUrl":"","useRemote":false,"ignoreCertErrors":false}]
   exported secrets: {}
   exported dashboards attachedInstances: [null,null]

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

## 3: "Export settings" while Demo Mode is on produces a backup of the demo data, with no real servers, keys or workspace attachments
Severity: data-loss
Where: store/config-store.ts:2764, store/config-store.ts:3088, services/backend-backup.ts:79, app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:131, at bf3a060
What the user loses: a usable backup. The file export encrypts whatever the live store holds; in Demo Mode that is one "demo.local" instance per service, an empty secrets map and dashboards without attachments. The continuous backend upload checks Demo Mode and skips ("Demo Mode never uploads", docs/guide.html:1143); the file export, one row above the Demo Mode switch on the same screen, does not. Restoring that file later replaces the real configuration with the demo one.
Steps:
1. Configure at least one real service with an API key.
2. Settings > Backup & Storage > Advanced > Demo Mode: on.
3. On the same screen tap "Export settings", authenticate, pick a passphrase, save the file.
4. Later, with Demo Mode off or on another phone, "Import settings" with that file.
Expected: the export refuses while Demo Mode is on, or exports the real configuration.
Actual: the export succeeds; the file holds demo instances and no secrets; importing it wipes the real configuration.
Evidence: probe
```
2b. While in Demo Mode: Settings > Backup & Storage > Export settings (same screen as the Demo Mode toggle)
   exported services.radarr: [{"id":"uuid-1","enabled":true,"name":"Radarr","localUrl":"http://demo.local","remoteUrl":"","useRemote":false,"ignoreCertErrors":false}]
   exported secrets: {}
   exported dashboards attachedInstances: [null,null]
```

## 4: A Wake-on-LAN device saved with a port such as 70000 makes every later backup impossible to restore
Severity: data-loss
Where: app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx:80, store/config-schema.ts:172, store/config-schema.ts:613, store/config-store.ts:2764, services/backend-backup.ts:40, components/integrations/service-editor.tsx:352, app/(tabs)/(dashboard,services,settings)/custom-headers.tsx:28, at bf3a060
What the user loses: every backup made after that device was saved, file or backend slot. The editor checks only that name and MAC are non-empty and turns the port field into `Number(x) || 9`, so 70000, 9.5 or -7 are saved with a success toast; the export and the backend upload write the payload unvalidated; the import's validator requires an integer port 1 to 65535 (and caps MAC at 32, broadcast address at 45, name at 200 characters) and one failing device throws for the whole file. The same gap exists for a service name over 200 characters (no limit in the editor) and a custom header value over 4096 characters.
Steps:
1. Settings > Network > Wake on LAN: add "NAS", MAC AA:BB:CC:DD:EE:FF, port 70000. It saves.
2. Settings > Backup & Storage > Export settings; save the file.
3. Import settings with that file (same or another phone).
Expected: the editor refuses the port, or the import restores everything else.
Actual: the import fails with "Config wolDevices entry is invalid" and restores nothing; no hint which device or field is at fault.
Evidence: probe
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

## 5: A service URL saved without a scheme on an older build is exported as-is and rejected on import, so that backup cannot be restored
Severity: data-loss
Where: store/config-store.ts:2615, store/config-store.ts:3112, store/config-schema.ts:41, store/config-schema.ts:77, store/config-store.ts:824, at bf3a060
What the user loses: the whole backup. The app tolerates a stored URL such as `192.168.1.10:7878` by prefixing `http://` every time it reads it (its own comment says historical values lack the scheme) and never rewrites the stored value; the export carries it as stored; the import's URL check parses it with `new URL`, whose protocol comes out as `192.168.1.10:`, and rejects the instance, which fails the whole file with "Config services.radarr entry is invalid". Day to day the app works, so the user learns of it only when restoring.
Steps:
1. On an install whose Radarr URL was saved before the editor normalized schemes (stored as `192.168.1.10:7878`; the app connects fine).
2. Settings > Backup & Storage > Export settings.
3. Import that file.
Expected: the import accepts the URL the app itself uses, or the export writes it normalized.
Actual: "Config services.radarr entry is invalid"; nothing is restored.
Evidence: reading

## 6: A failure in the second half of an import leaves the phone with its old secrets deleted, the new service lists already in storage and the old configuration still on screen
Severity: data-loss
Where: store/config-store.ts:2868, store/config-store.ts:2883, store/config-store.ts:2891, store/config-store.ts:2972, store/config-store.ts:3029, store/config-store.ts:3040, at bf3a060
What the user loses: the API keys of the current instances, deleted from the keychain before the steps that can still fail (keychain writes of the imported secrets, the backend pairing write, the Seerr session drains). If one of those throws, the user sees "Invalid config file", the running app still shows the old instances (now without keys, so every request fails), and the next launch loads the half-written new configuration.
Steps:
1. Import a backup on a device where a keychain write or the backend pairing write fails after the current secrets were wiped (a keychain error, or the app killed during the import).
2. Dismiss the "Invalid config file" message; use the app; relaunch.
Expected: a failed import changes nothing, or the failure is reported as partial with what to redo.
Actual: before relaunch the old instances have no keys; after relaunch the imported service lists are there with whichever secrets had been written.
Evidence: reading

## 7: The Downloads widget's poster cache grows forever in one storage row, and storage writes are never checked, so a long-lived install can stop loading its settings on Android
Severity: crash
Where: hooks/use-torrent-poster-map.ts:22, hooks/use-torrent-poster-map.ts:89, hooks/use-torrent-poster-map.ts:113, store/storage.ts:7, store/storage.ts:21, store/storage.ts:70, at bf3a060
What the user loses: the app's start. The hash-to-poster cache adds every download id seen in the queue or the latest 50 history rows and never evicts, persisting the whole map as one value (about 300 bytes per entry). On Android a single value past the 2 MB cursor window makes the read of all keys at start fail, which is how every setting is loaded; and because every write is fire-and-forget with no error handling, a store that has hit its size limit makes later saves fail silently.
Steps:
1. Keep the Downloads widget on a dashboard on Android, with Radarr or Sonarr grabbing many releases over a long period (on the order of seven thousand distinct downloads).
2. Relaunch the app.
Expected: the cache is capped or evicted; a failed storage write is reported.
Actual: by the code, the start-up read throws once the row is too large, and failed writes are dropped without a message. The size was not measured in a running app.
Evidence: reading

## 8: Removing a home network leaves workspaces that had selected it pinned to "always remote", and adding the same WiFi back does not undo it
Severity: wrong-result
Where: store/config-store.ts:1945, store/config-store.ts:1918, store/config-store.ts:700, store/config-store.ts:2636, lib/network.ts:77, lib/url-validation.ts:128, lib/http-client.ts:544, at bf3a060
What the user loses: local access from workspaces that had picked that network. The delete filters the global list only; the ids inside each dashboard stay; a selection whose ids are all gone resolves to no home network, which the URL resolver treats as "always remote" even with auto-switch off; re-adding the network mints a new id. The import path has a repair for exactly this state (its comment calls it "silently breaking local URLs with no way for the user to recover"); the delete path does not run it. Services with only a Local URL get an empty URL and show offline ("No URL configured").
Steps:
1. One home network "Casa"; in a workspace's editor, select Casa as its home network.
2. Settings > Network > Home Networks: remove Casa; add Casa again.
3. Open that workspace on the Casa WiFi.
Expected: the workspace is at home on Casa again, or falls back to all home networks as it would after an import.
Actual: the workspace keeps the dead id, resolves to no home network and uses Remote URLs; services with only a Local URL show offline, until the user finds the workspace's network picker.
Evidence: probe
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

## 9: Importing a backup that has no notification settings shows defaults until the next launch, then the previous device's settings come back
Severity: wrong-result
Where: store/config-store.ts:2987, store/config-store.ts:3067, store/config-store.ts:1415, at bf3a060
What the user loses: certainty about which notification toggles are in force. The import writes the notification-settings key only when the backup carries one, but always sets the in-memory settings (to defaults when the backup has none); the next launch reads the untouched key, so the toggles revert to whatever was on the phone before the import.
Steps:
1. Turn notifications off on the phone.
2. Import a backup made by an app version that did not export notification settings.
3. Check Settings > Notifications (shows on, the default); relaunch; check again.
Expected: the same values before and after relaunch.
Actual: on after the import, off after the relaunch.
Evidence: reading

# Not reached
- Service sign-in and sessions (Plex, Jellyfin, Emby, Seerr, Pi-hole, Beszel), HTTP Basic and Digest, the device-unlock gate, backend pairing, bearer and web login: read for security only; nothing found that would be a defect; not drafted by rule.
- Not read at all: the notification watchers (hooks/use-notification-watchers.tsx), the backend's pollers and webhook routes beyond the config and backup routes, the web editor's reducer, Plex/Jellyfin/Emby/Navidrome/Tautulli/Glances/unRAID/Tdarr/AdGuard/Maintainerr/Autobrr/Cleanuparr/NZBHydra2/Jackett/Prowlarr screens and services, the usenet add paths, the Bazarr tab beyond its mutation parameter builders, the calendar, and every test file.
- Read and found consistent: the torrent delete paths of qBittorrent, Deluge, Transmission and rtorrent; the arr library deletes and their exclusion flags; the queue-remove option mapping; the season file delete; the Bindery file delete; the manual import payloads and import mode; the detail-screen instance pinning from the dashboard Downloads and usenet widgets; the Seerr approve/decline/delete mutations; the config migrations v12 to v22; the import's validator field coverage against the config types; the backend backup slot writes and revisions.
