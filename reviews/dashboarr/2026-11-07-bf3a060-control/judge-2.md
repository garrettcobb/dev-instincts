# Verdicts

| Claim | Verdict | Group | Severity | Evidence |
|---|---|---|---|---|
| XC | confirmed | 1 | data-loss | wake-on-lan.tsx:80-92 checks only that name and MAC are non-empty and stores the port as Number(port.trim()) falling back to 9, so 70000, 9.5 or -7 are saved. config-store.ts:3088-3124 and backend-backup.ts:40-46 put wolDevices in the payload as stored. config-schema.ts:172-186 rejects a port that is not an integer in 1..65535 or a MAC over 32 chars; config-schema.ts:613-620 throws "Config wolDevices entry is invalid" for the whole file; config-store.ts:2857 validates before any write, so nothing is restored. Probe p1 reproduces it. |
| JV | confirmed | 2 | data-loss | use-radarr.ts:208 deletes on the pinned Radarr id, then use-radarr.ts:214-218 call getSeerrMe(), getMovieDetails(tmdbId) and deleteMedia(mediaId) with no instance id. overseerr-api.ts:88 and :160 resolve a missing id to getActiveInstanceId("overseerr"), the active dashboard's Seerr. The confirm text at movie/[id].tsx:518-522 names only Radarr. With the claim's exact setup the Home widgets list only Home Radarr items (calendar-card.tsx:12 useWorkspaceScopedInstances), so the mismatch needs a dashboard whose attached set includes the other Radarr, a pinned instance chip, or one Seerr tracking two Radarrs. |
| PQ | confirmed | 3 | data-loss | service-editor.tsx:352-356 checks only that the trimmed name is non-empty; the Name input at :898-903 has no maxLength and text-input.tsx:117 spreads props with no default cap. service-editor.tsx:380-390 and custom-headers.tsx:28-38 check header-name charset and CR/LF but never value length. config-schema.ts:76 rejects name over 200; config-schema.ts:62-64 rejects a header value over 4096; config-schema.ts:519 and :542 throw for the whole file. The 33-header step cannot happen: header-list-editor.tsx:21,60,120 cap rows at 32, and config-schema.ts:67 only rejects the 33rd. |
| TH | confirmed | 4 | wrong-result | config-store.ts:2987-2992 computes defaults when the payload has no notificationSettings but writes the storage key only when the payload has one; config-store.ts:3067 always sets the in-memory value. config-store.ts:1415-1421 reads the untouched key on the next launch. Probe p4 shows on after import, off after relaunch. |
| GN | confirmed | 5 | data-loss | config-store.ts:2764-2781 exportConfig has no demoMode check and calls buildExportPayload, which at :3088-3113 reads serviceInstances and instanceSecrets from the store; enableDemoMode at :2749-2751 replaced those with one demo.local instance per kind and an empty secrets map. backup.tsx:131-137 disables the row only while an export is in progress. backend-backup.ts:79 and backend-api.ts:275 are the two paths that do skip demo mode. |
| QX | confirmed | 6 | data-loss | config-store.ts:2868-2873 awaits deleteSecret for every current instance before :2883 persists the imported service lists and before the fallible awaits at :2891-2899 (setSecret), :2972-2982 (backend pair, which writes the keychain at backend-store.ts:149-156) and :3029-3036 (Seerr drains); the in-memory set() is only at :3040. backup.tsx:117 reports any throw as "Invalid config file". Smaller than claimed before relaunch: state.instanceSecrets still holds the old keys and http-client.ts:536 reads from it, so requests keep working until the next launch loads the half-written storage. |
| WS | confirmed | 7 | stuck | backend.tsx:577-586 performDeleteSlot deletes the slot, toasts "Backup deleted" and calls refreshSlots; backend.tsx:405-412 refreshSlots lists backups and calls noteBackupList; web-slot-watch.ts:31-36 sees backupEnabled with no slot marked mine, clears the last-hash key and calls uploadConfigBackup with force. backend.tsx:60-62 labels the own slot "This device" and :1002 says "This cannot be undone". web-slot-watch.ts:44-56 repeats the same list on the next check. |
| JW | confirmed | 8 | crash | use-torrent-poster-map.ts:64-111 only ever adds to the map and never deletes; :39-44 persists the whole map under one key on every growth (:113). storage.ts:70-74 and :21-24 call AsyncStorage.setItem without await or catch; storage.ts:7-13 reads every key with getAllKeys plus multiGet at start, and _layout.tsx:431 calls hydrate() with no catch. The Android per-row cursor limit that turns this into a failed start is platform behavior, not in the repo; the growth and the unchecked writes are in the code. |
| CD | confirmed | 5 | data-loss | Same code as GN: config-store.ts:2764-2771 exports whatever the store holds; :2735-2740 strips attachedInstances and :2749-2750 swaps in demo instances and empty secrets while demo mode is on; backup.tsx:131-137 and :154-165 put the export row and the Demo Mode switch on the same screen with no guard; backend-backup.ts:79 skips demo mode for the upload path only. |
| TJ | confirmed | 9 | data-loss | config-store.ts:2615-2623 says stored values can lack a scheme and prefixes http:// on every read without rewriting storage; hydrate at :959-963 accepts any string URL and never normalizes (normalizeServiceUrl is only used at :2622-2623). buildExportPayload at :3112 writes serviceInstances as stored. config-schema.ts:41-49 parses with new URL and requires http: or https:; probe p1 shows "192.168.1.10:7878" and "nas.local:7878" fail, and :519 throws for the whole file. Git history: scheme prefixing in the editor arrived in commit 061f468, so earlier saves were raw. |
| HT | confirmed | 10 | data-loss | config-store.ts:2735-2740 deletes attachedInstances from every dashboard in memory. renameDashboard :2099-2107, setDashboardIcon :2160-2168, addWidget :2354-2366, removeSlot :2370-2379, moveSlot :2381-2399 and setDashboardActiveInstance :1763-1773 each map the whole state.dashboards and setJSON it; 23 such writes exist and none checks demoMode. hydrate at :1195-1204 copies attachedInstances only when it is an array, so :1316-1320 treats the loss as auto-attach. :1737-1745 accepts the demo UUID as a pin because attachedInstances is undefined. Probe p2 reproduces it. |
| QT | confirmed | 10 | data-loss | Same cause and place as HT: config-store.ts:2735-2740 strips in memory; addWidget :2358-2365, removeSlot :2372-2377 and moveSlot :2384-2397 persist the whole dashboards array; disableDemoMode :2758-2761 re-hydrates from that row. Probe p2 shows both dashboards at null after one addWidget. |
| JM | confirmed | 11 | crash | config-store.ts:1945-1953 removeHomeNetwork filters the global list through homeNetworksPatch :579-619, which never touches dashboards; :1918-1927 addHomeNetwork mints a new id. url-validation.ts:128-135 returns forcesRemote for a non-empty id list with no live match, and config-store.ts:2636-2637 then returns the remote URL, so a local-only instance yields an empty string and http-client.ts:544-546 throws "No URL configured". repairOrphanedHomeNetworkSelection :700-712 is called only from the import at :2926; hydrate :1260-1270 keeps the stale ids. Probe p3 reproduces it. Severity chosen as crash because the visible effect is failed requests on the home WiFi. |
| LQ | confirmed | 12 | data-loss | config-store.ts:2718-2728 builds one demo instance per kind with a fresh UUID and :2749 installs it as serviceInstances. updateInstance :1640-1649 writes setJSON for that kind from the demo list with no demoMode check; service-editor.tsx:1003-1015 calls updateInstance on each switch; removeInstance :1561 writes the filtered list. disableDemoMode :2758-2761 hydrates from storage, and :1096-1100 loads secrets by instance id, so the real key stays under the orphaned id. Probe p2 reproduces it. |
| RW | confirmed | 1 | data-loss | Same as XC: wake-on-lan.tsx:80-92 stores the port as Number(port.trim()) falling back to 9 and the MAC as mac.trim() with no range or length check; config-schema.ts:172-186 returns null for port outside 1..65535, a non-integer port or a MAC over 32 chars; config-schema.ts:613-620 throws for the file; config-store.ts:2857 throws before any write; backend-backup.ts:40-46 uploads the same payload. Probe p1 reproduces all four typed values in the claim. |

# Notes

General decisions:
- Nothing in repo or in claims.md told me to do anything; the claims' "Steps" are descriptions, not instructions, and I followed none as commands.
- I ran no code from repo. Four probes under scratch copy single functions and name their source lines. Outputs are below.
- `git status` in repo shows one `_layout.tsx` under a very long route-group path as deleted; that is a Windows path-length checkout artifact, unrelated to the claims, and I changed nothing.
- Grouping: XC and RW share the Wake-on-LAN editor versus validator gap (group 1). PQ is the same kind of gap in two other editors; I kept it a separate group because the cause sits in different files, and I note XC's last sentence overlaps it. HT and QT are one group (demo mode strips attachments in memory and the dashboard setters persist the whole array). LQ is a separate group because the place is the per-kind services key and updateInstance, not the dashboards key. GN and CD are one group.
- Severity for the unrestorable-backup claims (XC, RW, PQ, TJ): data-loss, because the saved backup is unusable and a user restoring on a new phone recovers nothing. Nothing on the originating phone is lost by these defects alone.

XC and RW:
- Editor: wake-on-lan.tsx:80-92. The port input (:158-164) is a plain TextInput with number-pad keyboard and no maxLength; the MAC input (:144-150) has no length cap.
- Export: config-store.ts:3098 and :3124 pass wolDevices unchanged; backend-backup.ts:40-46 uses the same builder.
- Import: config-store.ts:2856-2857 runs migrateConfig then validateExportPayload before the first write at :2868. migrateConfig (config-migrations.ts:832-860) only runs migrations for payloads older than the current version and never touches WOL ports.
- Probe p1 output (section "XC/RW"): ports 70000, 9.5 and -7 and a 38-character MAC each save and each make the validator throw "Config wolDevices entry is invalid"; "abc" becomes 9 and passes; a clean device passes.

JV:
- Code path as the claim says. The code comment at use-radarr.ts:188-189 states that the cleanup targets the active Seerr.
- Decision on the steps: with each dashboard attached to its own Radarr and Seerr, the Home dashboard's Calendar, Still Pending and Recently Downloaded widgets only list Home Radarr items, because they take instances from useWorkspaceScopedInstances (calendar-card.tsx:12, use-workspace-instances.ts:64-79), and opening the Cabin dashboard makes Cabin's Seerr the active one. The defect is reached when the active dashboard attaches both Radarrs but pins Home's Seerr, when the movie page is opened with a Cabin instanceId while Home is active, or with one Seerr tracking a 1080p and a 4K Radarr. I counted it confirmed by those paths.

PQ:
- Name: no cap at service-editor.tsx:898-903 or in performSave :352-356; text-input.tsx passes props through (:117) with no default maxLength; the validator rejects at config-schema.ts:76 and throws at :519.
- Header value: neither service-editor.tsx:380-390 nor custom-headers.tsx:28-38 checks value length; header-list-editor.tsx:106-112 has no maxLength; the validator rejects at config-schema.ts:62 and throws at :542 (global) or :531 (per-instance, through coerceServiceSecrets at :165-166).
- Header count: refuted for this step. header-list-editor.tsx:21,60,120 stop at 32 rows and rowsToRecord (:23-31) can only shrink the count, and config-schema.ts:67 rejects only the 33rd entry, so the editor and the validator agree.
- Probe p1 output (section "PQ"): name 200 accepted, 201 rejected; 32 headers accepted, 33 rejected; value 4096 accepted, 4097 rejected.

TH:
- buildExportPayload always writes notificationSettings (:3123), so the gap needs a backup from before that field existed, a hand-edited file, or a backend web-slot payload without it; migrateConfig's v1 to v2 step sets it to null (config-migrations.ts:335), and validateExportPayload :607 skips null, so such a file reaches :2987 with no settings.
- Probe p4 output:
```
after import, in memory: {"enabled":true} | storage key: {"enabled":false}
after relaunch (hydrate): {"enabled":false}
```

GN and CD:
- exportConfig (config-store.ts:2764-2800) has no demoMode branch. buildExportPayload (:3088-3131) reads the live store. enableDemoMode (:2716-2756) replaces serviceInstances and instanceSecrets and strips attachedInstances in memory. The export row (backup.tsx:131-137) is only disabled while exportStage is set. The import confirm (backup.tsx:193) says it overwrites all settings, so restoring the file replaces the real configuration.

QX:
- Order inside importConfigFromPayload: validate (:2857), delete every current secret (:2868-2873), persist imported service lists (:2883), write imported secrets (:2891-2899), persist settings and dashboards (:2911-2964), backend pair (:2972-2982, keychain writes only, backend-store.ts:149-156), Seerr drains (:3029-3036), then set() (:3040-3068).
- Correction to the claim: before relaunch the old instances still have their keys in memory (state.instanceSecrets is untouched until :3040, and http-client.ts:536 reads from it), so requests do not fail until the next launch. After relaunch, hydrate reads the imported lists with whichever secrets had been written and the old secrets gone.
- Trigger paths: a thrown setSecret or pair keychain write, or the app being killed between the awaits.

WS:
- The own slot appears in the manage list labelled "This device" (backend.tsx:60-62) and its delete calls performDeleteSlot, which calls refreshSlots (:582), which calls noteBackupList (:409), which forces an upload when backupEnabled and no slot is mine (web-slot-watch.ts:31-36). performDisableBackup (:448-463) is the path that removes the slot without a re-upload.

JW:
- Code facts confirmed: no eviction in use-torrent-poster-map.ts; one storage row at :39-44; setJSON and setString in storage.ts never await or catch; initStorage reads every row at :7-13; hydrate() is called without a catch at _layout.tsx:431, so a throwing initStorage leaves the hydrated flag false and the store on defaults.
- Decision: the claim's failure threshold (a single row past the Android cursor window) is platform behavior that reading this repo cannot settle, and the claim itself says it was not measured. I counted the claim confirmed on the code defect it describes and assigned crash as the consequence the code allows, with that assumption stated.

TJ:
- Evidence that scheme-less values can exist: the code's own comment at config-store.ts:2615-2618, and the repo history (git log -S normalizeServiceUrl) shows the prefixing arrived in commit 061f468 "auto-prefix http:// to service URLs if protocol is missing"; earlier editors saved what was typed. hydrate never rewrites URLs; only an editor Save (service-editor.tsx:358-361) normalizes, and only for the instance being edited.
- Probe p1 output (section "TJ"): "192.168.1.10:7878", "nas.local:7878" and "localhost:7878" all return false from isHttpUrlOrEmpty; the prefixed form returns true.

HT and QT:
- Probe p2 output:
```
before demo:
  storage dashboards: [["Home",["radarr-home"]],["Cabin",["radarr-cabin"]]] | storage services.radarr: ["radarr-home@http://10.0.0.5:7878 useRemote=false"]
demo on, nothing edited:
  storage dashboards: [["Home",["radarr-home"]],["Cabin",["radarr-cabin"]]] | storage services.radarr: ["radarr-home@http://10.0.0.5:7878 useRemote=false"]
HT: renameDashboard('cabin','Cabin 2') while demo on:
  storage dashboards: [["Home",null],["Cabin 2",null]] | storage services.radarr: ["radarr-home@http://10.0.0.5:7878 useRemote=false"]
QT: addWidget('downloads') while demo on:
  storage dashboards: [["Home",null],["Cabin 2",null]] | storage services.radarr: ["radarr-home@http://10.0.0.5:7878 useRemote=false"]
LQ: updateInstance('radarr','uuid-1',{useRemote:true}) while demo on:
  storage dashboards: [["Home",null],["Cabin 2",null]] | storage services.radarr: ["uuid-1@http://demo.local useRemote=true"]
```
- null in that output is the hydrate result for a missing attachedInstances, which config-store.ts:1316-1320 treats as every instance attached.

JM:
- Probe p3 output:
```
1 before: networks=["net-1:Casa"] dash.homeNetworkIds=["net-1"] forcesRemote=false -> local/remote by auto-switch
2 removed Casa: networks=[] dash.homeNetworkIds=["net-1"] forcesRemote=true -> getActiveUrl returns remote ('' when only a Local URL is set -> 'No URL configured')
3 re-added Casa: networks=["net-2:Casa"] dash.homeNetworkIds=["net-1"] forcesRemote=true -> getActiveUrl returns remote ('' when only a Local URL is set -> 'No URL configured')
4 after import-only repair: networks=["net-2:Casa"] dash.homeNetworkIds=undefined forcesRemote=false -> local/remote by auto-switch
```
- Severity decision: the claim says wrong-result; I chose crash because for a local-only instance the resolver returns an empty string and serviceRequest throws "No URL configured" (http-client.ts:544-546), a failed request where the app should work. With a Remote URL configured the app works through it.

LQ:
- The same probe p2 (last block above) shows the services.radarr row replaced by the demo instance after one updateInstance. On disableDemoMode, hydrate (:959-963) reads that row, and the real API key stays in the keychain under "radarr-home", an id no instance uses (:1096-1100).

Programs run (all under scratch, standard library only, no network, no subprocess, no writes):
- p1_validator.js: copies of isHttpUrlOrEmpty, coerceHeaderMap, the leading checks of coerceServiceInstance, coerceWolDevice, the wolDevices loop of validateExportPayload, and the handleSave device construction from wake-on-lan.tsx.
- p2_demo_persist.js: copies of the enableDemoMode strip, addWidget, renameDashboard, updateInstance and the hydrate attachedInstances read, with a plain-object stand-in for setJSON and getJSON.
- p3_home_networks.js: copies of workspaceForcesRemote and repairOrphanedHomeNetworkSelection, with the removeHomeNetwork filter and a fresh id on re-add.
- p4_notif_import.js: copies of the import notification branch and the hydrate notification read, with a plain-object storage stand-in.
