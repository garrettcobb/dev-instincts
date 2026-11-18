# Dashboarr: issue drafts, batch 2 (control round `2026-11-07-bf3a060-control`)

**Nothing is posted.** No issue, comment, label, reaction or pull request goes up until Garrett has read these drafts and said go for this batch, in writing (`testing/FILING.md` §8); Garrett's "Draft batch 2" of 2026-11-17 (about 00:35 local) is the go for drafting alone. Written 2026-11-17 by the Dev Instincts shell session, under `testing/CONTROL.md` §15 and FILING §3 to §5, from `verdicts.md`, `score.md`, `key.private.json` and the claims in `claims.md`, with each arm's own text (`arm-a-1-findings.md`, `arm-b-1-report.md`), the judge's files (`judge-1.md`, `judge-2.md`, their probes) and the reviewer's drafts of the review round (`reviews/dashboarr/2026-11-07-bf3a060-review-issues.md`) as sources, in batch 1's form (`issues-batch-1.md`, a778321). Batch 1 was posted 2026-11-16 as #524 to #529. Every `gh` call was read-only.

**Posted 2026-11-17.** Drafts 1 to 4 were posted on 2026-11-17, in their order, as #530, #531, #532 and #533, on Garrett's written go for this batch, given 2026-11-17, about 01:00 local, after reading the four drafts and the coordinator's recommendation, in Garrett's words: "Post all four" (`testing/FILING.md` §8), after FILING §3's re-check made again before the first post (`main` still at `67f9eff`, the sha below, at 2026-11-17 07:04:52 UTC, so every cited file is the same blob and each draft went up word for word, its *Version* line as written, R496; nothing opened since 2026-11-17 but our own #524 to #529), and with no label; the posted bodies, byte for byte, are in `issues-batch-2/`, one file per issue, named by its number (`530.md` to `533.md`). GitHub stamps them 2026-11-17 07:05:24 to 07:05:51 UTC, 01:05 local (UTC-6), the same local and UTC day as the go. The paragraph above, "**Nothing is posted.**" and the rest of it, is overtaken by this one and stays as written (`metrics/FILED.md`, *Dashboarr notes*).

**Target:** `RenzoBeux/Dashboarr`, `main` at `67f9eff06f574601b819f759cd26b83f029719b9` (`67f9eff`, committed 2026-11-14 14:09:52 UTC; `gh api --method GET "repos/RenzoBeux/Dashboarr/commits?sha=main&per_page=1"`, read 2026-11-17 06:40:35 UTC), the sha every run, the judge and batch 1 read against, still 11 commits after `bf3a060` (`compare/bf3a060...67f9eff`: ahead by 11, behind by 0, 54 files). `main` is the repo's only branch (`branches`, 06:40:36 UTC), so there is no dev branch to re-check (FILING §3). Not archived, issues on; 33 open items on the repo's own count, which counts pull requests: 28 open issues by `gh issue list` and 5 open pull requests. Our six, #524 to #529, are each open with no label and no comment (06:40 UTC). Nothing has been merged since batch 1's re-check of 2026-11-15, so what that re-check said of the 11 commits still holds.

**The form:** as batch 1 recorded, and the same tree today: Dashboarr has no issue template, no CONTRIBUTING and no security policy (`.github` at `67f9eff` holds `FUNDING.yml`, `dependabot.yml` and `workflows` only; `reviews/dashboarr/2026-11-07-ai-policy-check.md`), so FILING §5's form is used as it stands, and no rule on AI-assisted reports has appeared since the check.

**The order** (`testing/CONTROL.md` §15): worst first by the weight of the group's final severity (§12: data-loss 4, wrong-result 3, crash 3), and between equal weights by the group's first claim in `claims.md`'s order (XC JV PQ TH GN QX WS JW CD TJ HT QT JM LQ RW), which the judge's group numbers follow. From `verdicts.md` and `score.md`'s *Groups* list, confirmed again against `key.private.json` before writing:

| Batch | Groups in order, with their claims in `claims.md` order |
|---|---|
| 1, posted 2026-11-16 | 1 (XC, RW) #524, 2 (JV) #525, 3 (PQ) #526, 5 (GN, CD) #527, 6 (QX) #528, 9 (TJ) #529: data-loss |
| 2, this file | 10 (HT, QT), 12 (LQ): data-loss; 4 (TH): wrong-result; 11 (JM): crash |
| not filed | 7 (WS), 8 (JW): stuck, in the ledger only (FILING §4) |

| Draft | Group | Claims (arm, run, finding) | Final severity | Ledger row | Arm |
|---|---|---|---|---|---|
| 1 | 10 | HT (B, run 1, finding 2); QT (A, run 1, finding 1) | data-loss | `DA-L01` (`control:A+B`) | A+B |
| 2 | 12 | LQ (A, run 1, finding 2) | data-loss | `DA-L02` (`control:A`) | A |
| 3 | 4 | TH (A, run 1, finding 9) | wrong-result | `DA-L08` (`control:A`) | A |
| 4 | 11 | JM (A, run 1, finding 8) | crash (the judge's; the claim and the row say wrong-result) | `DA-L06` (`control:A`) | A |

Every row of this batch is an arm A row, so no `control:B` row is named by this batch's commit. These four drafts close the control's confirmed groups: after this batch every confirmed group has a draft, groups 7 and 8 stay in the ledger as `stuck`, and Garrett has held none back. No claim is a security finding and none was refuted.

**One reading, the split of `DA-L01` and `DA-L02`:** the reviewer's own drafts file of 2026-11-08 folded the two into one issue, its draft 1, with `DA-L02` as *Related*. The judge put them in two groups, 10 and 12 (judge run 1: "a different setter and storage key"; run 2 the same), and FILING §4 files one issue per judge group, so this batch drafts them as two issues, drafts 1 and 2, each naming the other in *Related* as a sibling report filed alongside it. The shell session reads that as the clearer course too: the maintainer gets one issue per persisted key (the dashboards array; the per-kind services list), each with its own steps and its own test, and the common cause is said in both.

**Where the steps start** (`RULES.md` R491): each draft's steps start from an action a user takes in the app. Drafts 1 and 2 start at the Demo Mode switch and an ordinary edit while it is on; draft 4 at Home Networks > Remove. Draft 3 starts at an import of a backup file from an early build, one that carries no notification settings, which today's export never writes: that starting file is a user's old backup, read as a stored artefact rather than a crafted input, and flagged for Garrett below.

## The re-check and the duplicate search (FILING §3), 2026-11-17

**The re-check, without a clone.** `main` is still at `67f9eff`, the sha batch 1 compared against on 2026-11-15, so batch 1's comparison covers every file both batches cite, and this re-check compared what is new to this batch. The trees at `bf3a060` and `67f9eff` were fetched again read-only (`gh api --method GET "repos/RenzoBeux/Dashboarr/git/trees/<sha>?recursive=1"`, 06:41:46 and 06:41:47 UTC, neither truncated: 1,101 and 1,107 blobs), and every file the four drafts cite was compared by its blob sha at the two. Of the 13 files cited across the four groups, 7 have the same blob at both shas: `store/config-store.ts`, the file every draft rests on, `lib/network.ts`, `app/dashboard-edit/[id].tsx`, `app/(tabs)/(dashboard,services,settings)/settings/notifications.tsx`, `settings/backup.tsx`, `services/backend-backup.ts` and `services/backend-api.ts`. Six differ, each one of batch 1's seven shifted files but one: `components/integrations/service-editor.tsx`, `lib/http-client.ts`, `lib/url-validation.ts`, `store/config-migrations.ts`, `store/config-schema.ts` and `docs/guide.html` (batch 1's: #517's rTorrent XML-RPC path and #513's VPN diagnostics, away from any cited line), and, new to this batch, `app/(tabs)/(dashboard,services,settings)/home-networks.tsx`, changed by #513 alone (`commits?path=…`: e3e3d08, 2026-11-10): an import, two class strings, one line reading the tunnel diagnostics and an 18-line diagnostics block at `:435-452`, nothing near the delete handler or the confirm. Each of the seven differing files was fetched at both shas (`contents/<path>?ref=<sha>`, raw, 06:42:46 to 06:42:57 UTC, each copy's `git hash-object` equal to its tree's blob) and the ranges this batch cites were mapped line by line from `bf3a060` to `main` and found as the same text: `service-editor.tsx:1001-1037` is `:1049-1085` on `main`; `http-client.ts:544-547` is `:557-560`; `url-validation.ts:128-135` is `:128-135`; `home-networks.tsx:284-289` is `:286-291` and `:624-627` is `:644-647`; `config-migrations.ts:335` is `:338` and `:832-860` is `:837-865`; `config-schema.ts:607` is `:613`; `guide.html:263` is `:263` (#513's lines fall below it). Files new to this batch and compared now: `lib/network.ts`, `app/dashboard-edit/[id].tsx`, `settings/notifications.tsx` (same blob each) and `home-networks.tsx` (above); the new ranges in batch 1's six shifted files were mapped now. *Unchanged* means the same blob at `bf3a060` and `main` for every cited file; *moved*, the same code at new line numbers; *changed*, the cited line itself rewritten since the read; *fixed*, the mechanism gone. The 54 files the 11 commits touch include no other file of this batch. The five open pull requests, #523 (Bindery search), #483 (library search and list view, 19 files, updated 2026-11-14), #467, #466 and #465 (AdGuard screens, drafts since 2026-10-02): #483 touches `docs/guide.html`, which draft 1 quotes, in three hunks at `:793-807` (the screens list) and `:865` (global search), not the quoted line; the other four touch no cited file (`gh pr view <n> --json files`; `pulls/483/files`).

**The duplicate search.** Phrase searches, both states, `gh search issues --repo RenzoBeux/Dashboarr "<words>" --limit 50` and `gh search prs ... --limit 50`, 27 terms, from 06:42:58 UTC; GitHub's search limit stopped the run at the 16th term ("home network") at 06:43:40, the 25th to 27th answered at 06:44:0x, and the nine stopped ran again from 06:46:05 to 06:47:10 UTC, each answered. Words-apart searches, `gh issue list` and `gh pr list --repo RenzoBeux/Dashboarr --state all --search "<words>" --limit 50`, two terms a group, 06:47:14 to 06:48:12 UTC. As a cross-check, the titles and bodies of all 522 issues and pull requests (296 issues, 226 pull requests, through #529; `gh api --method GET "repos/RenzoBeux/Dashboarr/issues?state=all&per_page=100" --paginate`, 06:44:08 UTC) were searched for the function names and the user's words below, and the 28 open issue titles were read by eye (#529 to #524 ours; #515, #514, #512, #510, #508, #507, #503, #498, #490, #489, #478, #477, #476, #462, #455, #453, #451, #445, #437, #430, #391, #37: SABnzbd, the calendar, notifications as a feature, feature and integration requests, the VPN detection of #489; none on Demo Mode, a workspace's attachments, a notification setting after an import or a removed home network). Our own #524 to #529 appear under "demo mode", "demo.local", "enableDemoMode" and "home network" and are not duplicates of these groups; #527, the file export in Demo Mode, is the nearest, a report of ours on the same Demo Mode root, and drafts 1 and 2 name it in *Related*. None of the four is reported, open or closed, and no open pull request fixes one.

- **Group 10 (draft 1).** Unchanged at every cited line: `store/config-store.ts` and `app/dashboard-edit/[id].tsx` are the same blob at both shas, and the guide's promise is `docs/guide.html:263` at both (the file's blob differs by #513's two paragraphs, below it). Searches: "demo mode": issues #527 (ours), PRs 36 (#499 to #13, each a feature adding its own demo data, batch 1's list); "demo data": issues #527, #432, #436, #434 (integration requests), PRs 19 (the same features); "attachedInstances": issues none, PRs #429, #138, #89; "attached instances", "instance list": PRs #138, #89 and #375, #93 (the feature's own pull requests); "demo mode persist", "workspace attach", "Use remote demo", "disableDemoMode", "turn off demo": none in all; "demo.local" and "enableDemoMode": #527 alone; words "demo mode attachments": none and none, "demo mode dashboard": #527 and 17 PRs (demo data for widgets). Bodies: "demo mode" 30 (#527 and 29 pull requests), `attachedInstances` 3 (#429, #138, #89), `enableDemoMode` or `demo.local` 1 (#527), Demo Mode beside persist, overwrite, wipe, lost or erase: none. None reports this. Nearest: #89 (merged 2026-05), which introduced the per-dashboard attachment lists, and #429 (merged 2026-09), which made the network resolver judge each instance by the dashboards that explicitly attach it, so a lost list changes more than the widgets' scope.
- **Group 12 (draft 2).** Moved. `store/config-store.ts`: same blob. `components/integrations/service-editor.tsx`: #517 added the XML-RPC path field above, so the four switches that call `updateInstance` are `:1049-1085` on `main` (`bf3a060`: 1001-1037), the same text. Searches: "service toggle": issues none, PRs #467 (AdGuard's blocked-services toggles); "api key lost": none; "updateInstance": issues none, PRs #377, #291, #402 (features); "instance list": PRs #375, #93; words "demo mode service switch": #527 and PRs #469, #419, #413, #370, #305 (demo data), "demo api key": #527, #436 and 12 PRs (features). Bodies: `updateInstance` 1 (#291), a demo instance beside a key: none but #527. None reports this. Nearest: #527, ours, the same root one screen over.
- **Group 4 (draft 3).** Moved. `store/config-store.ts` and `settings/notifications.tsx`: same blob. `store/config-migrations.ts`: #517 added its v64 note and bumped the version above, so the v1-to-v2 step's null is `:338` (335) and `migrateConfig` `:837-865` (832-860), the same text. `store/config-schema.ts`: #517 added five lines above, so the validator's skip of a null `notificationSettings` is `:613` (607). Searches: "notification settings": issues #395 (a web view proposal), #284 (a user changing phones), #60 (the toggle reset after app updates, closed 2026-05), PRs #425, #350, #78, #89, #72; "notificationSettings": issues #220 (Apprise request), PRs #72; "notification settings import", "import notifications": none in all; words "notification settings import": #284, #256 and PRs #253, #131, #89, #79, #72 (notification features), "notifications relaunch import": none and none. Bodies: `notificationSettings` 2 (#220, #72), "notification settings" 6, a notification beside relaunch, restart or revert 1 (#72), an import beside a notification: none. None reports this. Nearest: #60 (closed, fixed by #72): "the notification setting gets reset after app updates", the same symptom from a different cause, the notifications store reading storage before it was ready; the import path was not part of it.
- **Group 11 (draft 4).** Moved. `store/config-store.ts`, `lib/network.ts` and `app/dashboard-edit/[id].tsx`: same blob. `app/(tabs)/(dashboard,services,settings)/home-networks.tsx`: #513 added its VPN diagnostics block, so the delete handler is `:286-291` (284-289) and the confirm `:644-647` (624-627), the same text. `lib/url-validation.ts`: #517 appended below, so `workspaceForcesRemote` is `:128-135` at both. `lib/http-client.ts`: #517 added `apiBasePathFor` above, so "No URL configured" is `:557-560` (544-547). Searches: "home network": issues 13 (#489 open, the VPN detection; #526 and #524 ours; #418, #356, #394, #420, #344, #234, #251, #168, #231, #230, closed), PRs 10 (#429, #409, #264, #169, #202, #206, #183, #170, #189, #72); "WiFi": issues 13, PRs 9, the same feature's history; "always remote" and "homeNetworkIds": issues none, PRs #366, #202; "repairOrphanedHomeNetworkSelection": PRs #202; "remove home network", "No URL configured", "local URL offline": none in all; words "home network remove workspace": none and none, "home network remote local offline": #356, #344 and PRs #169, #183, #189, #72. Bodies: "home network" 15, `homeNetworkIds` 2 (#366, #202), "always remote" 1 (#366), `repairOrphaned` 1 (#202), a WiFi or SSID beside remove or delete 1 (#429, a dashboard's deletion), "No URL configured": none. None reports the delete path. The closed "offline on the home WiFi" reports, #231, #234, #251, #356, #394, are SSID reading and VPN detection, not a removed network. Nearest: #202 (merged 2026-06, on #168), which added the repair the import runs and whose description says an all-stale selection "silently meant always-remote"; #169 (merged 2026-06), the per-dashboard home networks; #366, which names the explicit empty selection as the deliberate "always remote" pin.

---

## Draft 1 (group 10)

**Title:** [Bug] Any dashboard edit while Demo Mode is on saves the demo-stripped dashboards, so every workspace's attached-instance list is gone when Demo Mode is turned off

**Version:** `main` at `67f9eff`. Read at `bf3a060`; the code below is the same at the two, `store/config-store.ts` and `app/dashboard-edit/[id].tsx` byte for byte and the guide's quoted line at the same number, and the line numbers are `main`'s.

**Summary:** `enableDemoMode` records the demo flag, builds one `http://demo.local` instance per service kind and, in memory, removes `attachedInstances` from every dashboard, with a comment that this is in memory, not persisted, and that the stored attachments come back on `disableDemoMode` (`store/config-store.ts:2716-2756`; the comment `:2732-2734`). But every dashboard setter maps `state.dashboards` and writes the whole array to storage: 21 setters do, and none checks `demoMode` (`addWidget` `:2354-2367`, `removeSlot` `:2370-2379`, `moveSlot` `:2381-2399`, `renameDashboard` `:2099-2107`, `setDashboardIcon` `:2160-2168`, `setDashboardActiveInstance` `:1726-1773` among them; the store reads `demoMode` only in the network evaluator and the switch itself, `:598`, `:662`, `:1423`, `:2717-2759`). `disableDemoMode` then hydrates from storage (`:2758-2762`), where a dashboard with no `attachedInstances` is read as auto-attach, every instance attached (`:1195-1204`; the comment `:1316-1321`), so there is nothing left to restore. A pin set while Demo Mode is on passes the write-time check because the stripped dashboard counts as auto-attach (`:1737-1745`) and points at a demo id afterwards.

**Result:** after a Demo Mode session in which any dashboard was touched, every curated workspace comes back showing every instance: the lists that said which Radarr and which qBittorrent belong to Home and which to Cabin are gone and must be rebuilt by hand in each dashboard's editor (`app/dashboard-edit/[id].tsx:570-573`, "Attached instances"), per-dashboard instance pins fall back to the first instance of each kind, and a widget added in Demo Mode stays. The guide promises the opposite: "Turn it off and everything comes back exactly as it was" (`docs/guide.html:263`).

**Where:** `store/config-store.ts:2716-2762` (`:2732-2740`), `:2354-2399`, `:2099-2107`, `:2160-2168`, `:1726-1773`, `:1195-1204`, `:1316-1321`; `app/dashboard-edit/[id].tsx:570-573`; `docs/guide.html:263`.

**Steps:**
1. Have two workspaces with explicit attachment lists: Home attached to one Radarr, Cabin to another (a dashboard's editor, Attached instances; a new dashboard starts with an explicit, empty list).
2. Settings > Backup & Storage > Advanced > Demo Mode: on.
3. On the dashboard, add a widget (or move or remove one; renaming a dashboard, changing its icon or colour, changing a widget's settings, pinning a tab or tapping an instance chip writes the same array).
4. Demo Mode: off.

**Expected:** both workspaces keep their attachment lists, as the guide says.

**Actual:** both workspaces show every instance; the attachment lists are gone and have to be rebuilt by hand; the widget added in Demo Mode is still there.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `enableDemoMode` strip, the dashboard setters and the hydrate read over an in-memory store. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe-demo-dashboard-write.js`, plain Node, standard library only; a rename while Demo Mode is on):
```
before demo: [["Home",["qbit-home","radarr-home"]],["Cabin",["qbit-cabin","radarr-cabin"]]]
demo on, storage still intact: [["Home",["qbit-home","radarr-home"]],["Cabin",["qbit-cabin","radarr-cabin"]]]
after demo off: [["Home (renamed)",null],["Cabin",null]]
dashboards whose attachment list was lost: ["Home (renamed)","Cabin"] (undefined = every instance attached)
```
(`null` is how JSON prints the missing field. A second program, with one `addWidget` instead of the rename, shows the same two dashboards at `null`.)

**Related:** the same cause reaches the per-kind service lists through the service editor's switches, a sibling report filed alongside this one. #527 is our report of the file export while Demo Mode is on, the same root one row over on the same screen: the live store holds the demo set, and only the two upload paths check for it. #89 introduced the per-dashboard attachment lists; since #429 the network resolver judges each instance by the dashboards that explicitly attach it, so a lost list also changes which home networks an instance is judged against.

**Possible fix:** keep the real dashboards aside while Demo Mode is on (snapshot on enable, restore on disable, and let the setters write the in-memory copy only), or route the setters' dashboard writes through one helper that skips the storage write while `demoMode` is true, as the backend backup and the backend sync already skip. A store test: enable Demo Mode, call `addWidget` and `renameDashboard`, disable it, and assert every dashboard's `attachedInstances` equals what was stored before.

*Outside the issue:* Arm: A+B. Claims HT (arm B run 1, finding 2) and QT (arm A run 1, finding 1), both final data-loss. Both arms have claims here, so the clearer steps were taken: QT's (arm A run 1), four concrete steps through one door, a widget added, whose *Expected* and *Actual* match the probes; HT's list of every door that writes the array is folded into step 3, and HT's note on the pin into *Summary*. The probe output is arm B's `probe-demo-dashboard-write.js` as its report prints it (`arm-b-1-probes/`), the one output that shows the dashboards alone; arm A's probe output interleaves this group with groups 5 and 12, and judge run 2's `p2_demo_persist.js` (`judge-2-probes/`) shows the same two dashboards at `null` after one `addWidget`, which the note under the output says. Judge run 2 counted 23 writes of the dashboards key; the shell session's count at the re-check is 21 setters, the import's own write and one comment making the judge's 23 matches of the call; *Related*'s #89 and #429 are the shell session's reading at the search. Ledger row `DA-L01` (`control:A+B`). This group and group 12 were one issue in the reviewer's 2026-11-08 draft 1; drafted as two here (the reading above).

---

## Draft 2 (group 12)

**Title:** [Bug] Flipping any switch on a service while Demo Mode is on replaces the real server of that kind with the demo one, and its API key is left under an id nothing reads

**Version:** `main` at `67f9eff`. Read at `bf3a060`; the code below is the same at the two, `components/integrations/service-editor.tsx` at new line numbers on `main`, and the line numbers are `main`'s.

**Summary:** `enableDemoMode` puts one generated `http://demo.local` instance per kind into the in-memory instance lists and empties the secrets map (`store/config-store.ts:2718-2728`, `:2749-2751`). The service editor's switches, "Always use Remote URL", "Allow invalid certificates", "Remote URL needs a VPN" and qBittorrent's "Tag added torrents", call `updateInstance` on every tap (`components/integrations/service-editor.tsx:1049-1085`), and `updateInstance` writes that kind's whole list to storage with no `demoMode` check (`store/config-store.ts:1636-1649`); `removeInstance` writes the filtered, now empty, list the same way (`:1557-1561`). `disableDemoMode` hydrates from storage (`:2758-2762`), and hydrate loads secrets by the ids in the stored list (`:1094-1101`), so the real instance's key stays in the keychain under an id no instance has any more.

**Result:** after Demo Mode is turned off, the only Radarr is "Radarr" at `http://demo.local` with no API key; the real connection, its name, local and remote URLs and options, must be entered again and the key pasted again. The old key is unreachable from the app, though still stored. One tap on one switch is enough; the editor gives no sign that it is editing a demo instance.

**Where:** `store/config-store.ts:2716-2756` (`:2718-2728`, `:2749-2751`), `:1636-1649`, `:1557-1561`, `:2758-2762`, `:1094-1101`; `components/integrations/service-editor.tsx:1049-1085`.

**Steps:**
1. Have a real Radarr configured, with an API key.
2. Settings > Backup & Storage > Advanced > Demo Mode: on.
3. Settings > Services > Radarr: on the instance shown, flip "Always use Remote URL" (or any other switch), then flip it back.
4. Demo Mode: off.

**Expected:** the real Radarr is back, with its URL and its key.

**Actual:** the only Radarr is "Radarr" at `http://demo.local`, with no key; the real one has to be re-entered.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `enableDemoMode` swap, `updateInstance` and the hydrate read over an in-memory store. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`p2_demo_persist.js`, plain Node, standard library only; the last block is this report, the two before it the sibling's):
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

**Related:** the dashboards array is written the same way by every dashboard edit while Demo Mode is on, a sibling report filed alongside this one. #527 is our report of the file export while Demo Mode is on, the same root: the live store holds the demo set, and only the backend backup and the backend sync check for it.

**Possible fix:** the same guard as for the dashboards: snapshot the real instance lists on enable and restore them on disable, or skip the storage write in `updateInstance` and `removeInstance` while `demoMode` is true; and on `disableDemoMode`, or at hydrate, a secret whose id matches no instance could be reported rather than left behind. A store test: enable Demo Mode, call `updateInstance` on the demo instance, disable it, and assert the stored list for that kind equals the one stored before, with its secret still loaded.

*Outside the issue:* Arm: A. Claim LQ (arm A run 1, finding 2; final data-loss), the group's only claim; its steps, with "flip it back" added so the step is plainly an ordinary tap, not a chosen setting. The probe output is judge run 2's `p2_demo_persist.js` as `judge-2.md` keeps it (`judge-2-probes/`), whole, since its last block is this group and the two before it the sibling's; arm A's own probe output (the reviewer's `probe_demo_mode_persist.js`, printed under the claim) shows the same `uuid-1` at `http://demo.local` after Demo Mode is off, interleaved with groups 5 and 10. The remark on the orphaned secret's reporting in *Possible fix* is the shell session's. Ledger row `DA-L02` (`control:A`). Drafted apart from group 10 (the reading above).

---

## Draft 3 (group 4)

**Title:** [Bug] Importing a backup that carries no notification settings shows the defaults until the next launch, then the phone's earlier settings come back

**Version:** `main` at `67f9eff`. Read at `bf3a060`; the code below is the same at the two, `store/config-migrations.ts` and `store/config-schema.ts` at new line numbers on `main`, and the line numbers are `main`'s.

**Summary:** the import computes the notification settings it will install as the backup's, merged over the defaults, or the defaults when the backup has none, but writes the storage key only when the backup has them (`store/config-store.ts:2987-2992`); the bulk `set()` at the end installs the computed value in memory either way (`:3040`, `:3067`), and the next launch reads the key (`:1415-1421`). Today's export always writes the field (`:3123`), so the gap needs a backup from before the field existed: the v1-to-v2 migration sets a missing `notificationSettings` to `null` (`store/config-migrations.ts:338`; `migrateConfig` `:837-865`), the validator skips a null one (`store/config-schema.ts:613`), and the file reaches `:2987` with no settings. A hand-edited file or a backend slot payload without the field would do the same.

**Result:** right after the import, Settings > Notifications shows "Enable notifications" on and every category at its default, whatever the phone had; after the next launch the toggles are back to what the phone had before the import. Nothing is lost, but for one session the screen and the stored values disagree, and an import whose confirm says it will overwrite all current settings leaves this one as it was.

**Where:** `store/config-store.ts:2987-2992`, `:3040`, `:3067`, `:3123`, `:1415-1421`; `store/config-migrations.ts:338`, `:837-865`; `store/config-schema.ts:613`; `app/(tabs)/(dashboard,services,settings)/settings/notifications.tsx:35-38`.

**Steps:**
1. Settings > Notifications: turn "Enable notifications" off.
2. Settings > Backup & Storage > Import settings, with a backup made by an early build, one from before notification settings were exported (a v1 file).
3. Settings > Notifications: the switch shows on. Relaunch the app and look again.

**Expected:** the same values before and after the relaunch, the imported ones or the defaults.

**Actual:** on after the import, off after the relaunch.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the import's notification branch and the hydrate read over an in-memory store. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`p4_notif_import.js`, plain Node, standard library only):
```
after import, in memory: {"enabled":true} | storage key: {"enabled":false}
after relaunch (hydrate): {"enabled":false}
```

**Related:** #60 (closed, fixed by #72) was the same symptom, the notification switch reset after an app update, from a different cause, the notifications store reading storage before it was ready; the import path was not part of that fix. #528 is our report on the order of writes in the same import function.

**Possible fix:** write the key whenever the import runs, with the value the in-memory `set()` installs, so storage and memory agree; or, if a backup without the field should leave the phone's settings alone, keep the stored value in memory too instead of the defaults. A test: with `enabled: false` stored, import a payload without `notificationSettings`, hydrate, and assert the stored value equals the one the store shows.

*Outside the issue:* Arm: A. Claim TH (arm A run 1, finding 9; final wrong-result), the group's only claim; its steps, with the starting file named as what it is. The claim's evidence is reading; judge run 2 ran a program on this group's code, `p4_notif_import.js` (`judge-2-probes/`), so the issue carries the program clause and quotes the judge's output as `judge-2.md` keeps it. Judge run 2's note on how such a file arises (the v1-to-v2 migration's `null`, the validator's skip, a hand-edited file or a backend slot payload) is in *Summary*. The reviewer's own drafts file of 2026-11-08 listed `DA-L08` under *Not filing*, "small, and FILING §4 would allow it, but not worth a maintainer's attention on its own; hold for a later batch"; the control's rule (§15: every confirmed group gets a draft, in order) governs here, and the draft says plainly that nothing is lost. **Flagged for Garrett:** the smallest of the four, and the starting file is a backup from an early build, which today's export cannot produce. Ledger row `DA-L08` (`control:A`).

---

## Draft 4 (group 11)

**Title:** [Bug] Removing a home network leaves the workspaces that selected it pinned to "always remote", and adding the same WiFi back does not undo it; their local-only services show offline at home

**Version:** `main` at `67f9eff`. Read at `bf3a060`; the code below is the same at the two, `home-networks.tsx` and `lib/http-client.ts` at new line numbers on `main`, and the line numbers are `main`'s.

**Summary:** a workspace's home-network selection is a list of network ids on the dashboard. `removeHomeNetwork` filters the global list and writes it (`store/config-store.ts:1945-1953`, through `homeNetworksPatch` `:579-619`) and touches no dashboard's `homeNetworkIds`; hydrate keeps the stale ids (`:1260-1271`); `addHomeNetwork` mints a new id (`:1918-1927`, `:806-808`), so adding the same SSID back does not match the old one. A non-empty selection with no live id counts as "forces remote" (`lib/url-validation.ts:128-135`; `lib/network.ts:77-88` resolves it to no network), auto-switch on or off, and `getActiveUrl` then returns the remote URL, an empty string for an instance with only a local URL (`:2636-2637`), which every request refuses with "No URL configured" (`lib/http-client.ts:557-560`). The import path repairs exactly this state: `repairOrphanedHomeNetworkSelection` (`:700-712`, called at `:2926-2931`), whose comment (`:690-699`) says an all-stale selection resolves to "always remote", "silently breaking local URLs with no way for the user to recover"; the delete path does not run it. The Home Networks screen's confirm says only "Stop treating "<name>" as a home network?" and its handler calls `removeHomeNetwork` alone (`app/(tabs)/(dashboard,services,settings)/home-networks.tsx:644-647`, `:286-291`).

**Result:** on the home WiFi, every service in such a workspace is reached through its Remote URL, and a service with only a Local URL fails every request and shows offline, for good, until the user finds the workspace editor's Home networks section and chooses All (`app/dashboard-edit/[id].tsx:717-735`, `:405-407`). Nothing on the Home Networks screen says a workspace depended on the removed network.

**Where:** `store/config-store.ts:1945-1953`, `:579-619`, `:1918-1927`, `:806-808`, `:1260-1271`, `:2636-2637`, `:690-712`, `:2926-2931`; `lib/url-validation.ts:128-135`; `lib/network.ts:77-88`; `lib/http-client.ts:557-560`; `app/(tabs)/(dashboard,services,settings)/home-networks.tsx:286-291`, `:644-647`; `app/dashboard-edit/[id].tsx:405-407`, `:717-735`.

**Steps:**
1. Settings > Network > Home Networks: one network, "Casa". In a workspace's editor, Home networks > Custom, select Casa.
2. Home Networks: remove Casa (the confirm asks only whether to stop treating it as a home network). Add Casa again, the same SSID.
3. Open that workspace on the Casa WiFi.

**Expected:** the workspace is at home on Casa again; or, as after an import, it falls back to all home networks.

**Actual:** the workspace keeps the dead id, resolves to no home network and uses Remote URLs; a service with only a Local URL fails with "No URL configured" and shows offline.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `addHomeNetwork`, `removeHomeNetwork`, `resolveEffectiveHomeNetworks`, `workspaceForcesRemote` and `repairOrphanedHomeNetworkSelection` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe_home_network_delete.js`, plain Node, standard library only):
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

**Related:** #202 (merged 2026-06, on #168) added the repair the import runs, its description saying an all-stale selection "silently meant always-remote"; the delete path has no such step. #169 added the per-dashboard home networks; #366 names the explicit empty selection as the deliberate "always remote" pin, which is why a pruned list that empties should become "use all networks" rather than `[]`.

**Possible fix:** in `removeHomeNetwork`, prune the id from every dashboard's `homeNetworkIds` and, where that empties a list the user had filled, drop the key so the workspace uses all networks, as the import's repair does; or run `repairOrphanedHomeNetworkSelection` after the delete; and name the workspaces that select the network in the confirm. A store test: select a network in a workspace, remove it, and assert `workspaceForcesRemote` is false for that workspace.

*Outside the issue:* Arm: A. Claim JM (arm A run 1, finding 8), the group's only claim; its steps, with the editor's Custom choice named in step 1 and the confirm's words in step 2. The claim's severity is wrong-result; the judge's final verdict is crash, both runs ("a failed request where the app should work": every request from a local-only instance in that workspace throws "No URL configured"), and the judge's final severity rules this batch's order (`testing/CONTROL.md` §15), where it places group 11 last, after the wrong-result group 4; the ledger row `DA-L06` keeps its own severity, wrong-result, from the review round, and is not rewritten. The draft's *Result* says what happens in plain words, failed requests and an offline service, and does not call it a crash of the app. The probe output is arm A's (the reviewer's `probe_home_network_delete.js`, as the claim prints it); judge run 2's `p3_home_networks.js` (`judge-2-probes/`) shows the same four states. *Related*'s #202, #169 and #366 are the shell session's reading at the search. **Flagged for Garrett:** the severity reading. Ledger row `DA-L06` (`control:A`).

---

## Not in this batch

- **Not filed (FILING §4):** group 7 (WS), the backend backup slot that comes back after its delete, and group 8 (JW), the poster cache that grows in one storage row, both `stuck` by the judge's final verdicts, stay in the ledger (`DA-L12`, `DA-L07`).
- **Dropped by the re-check or the search:** none. No group is fixed on `main`, none is filed upstream, and no open pull request touches a cited line (#483 touches `docs/guide.html` away from the quoted line).
- **After this batch no confirmed group remains undrafted:** the 12 judge groups are 10 drafted (6 posted in batch 1, 4 here) and 2 `stuck`, in the ledger only. Garrett has held none back so far.

## Flagged for Garrett

Each draft Garrett should read before a go, and why:
- **Draft 4 (group 11, JM, `DA-L06`):** the severity. The claim and the ledger row say wrong-result; the judge's final verdict, which orders the batch, says crash in the sense of a failed request, not a crash of the app; the draft's *Result* says the plain outcome and the *Arm* line names both.
- **Drafts 1 and 2 (groups 10 and 12, `DA-L01` and `DA-L02`):** the split. The reviewer's 2026-11-08 draft folded them into one issue; the judge's two groups and FILING §4's one issue per group make them two here, each naming the other as a sibling filed alongside it. If Garrett prefers one issue, draft 2's *Summary* and steps fold into draft 1 as its *Related* without loss.
- **Draft 1 (group 10):** a judgement of the shell session: arm A's steps through one door, with arm B's list of every door folded into step 3; the probe quoted is arm B's rename, not arm A's widget, since it shows the dashboards alone.
- **Draft 3 (group 4, TH, `DA-L08`):** the smallest of the four, which the reviewer's own drafts file would have held; the starting file is a backup from an early build, which today's export cannot produce, read here as a user's stored artefact rather than a crafted input. Garrett may hold it if a maintainer's attention is better spent on the three above.
- **Drafts 1, 2 and 4** rest on probes (both arms and the judge for group 10; arm A and the judge for groups 12 and 11); draft 3 on the judge's program alone, its claim being reading. Drafts 1 and 2 name #527, our own posted issue, in *Related* as a report of ours on the same Demo Mode root; draft 3 names #528 the same way.
