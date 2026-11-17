# Dashboarr: issue drafts, batch 1 (control round `2026-11-07-bf3a060-control`)

**Nothing is posted.** No issue, comment, label, reaction or pull request goes up until Garrett has read these drafts and said go for this batch, in writing (`testing/FILING.md` §8); Garrett's "Draft the batch" of 2026-11-15 is the go for drafting alone. Written 2026-11-15 by the Dev Instincts shell session, under `testing/CONTROL.md` §15 and FILING §3 to §5, from `verdicts.md`, `score.md`, `key.private.json` and the claims in `claims.md`, with each arm's own text (`arm-a-1-findings.md`, `arm-b-1-report.md`), the judge's files (`judge-1.md`, `judge-2.md`, their probes) and the reviewer's drafts of the review round (`reviews/dashboarr/2026-11-07-bf3a060-review-issues.md`) as sources. Every `gh` call was read-only.

**Posted 2026-11-16.** Drafts 1 to 6 were posted on 2026-11-16, in their order, as #524, #525, #526, #527, #528 and #529, on Garrett's written go for this batch, given 2026-11-15, about 23:05 local, after reading the six drafts, in Garrett's words: "Post all six" (`testing/FILING.md` §8), after FILING §3's re-check made again before the first post (`main` still at `67f9eff`, the sha below, at 2026-11-17 00:24:59 UTC, so every cited file is the same blob and each draft went up word for word, its *Version* line as written, R496; nothing opened since 2026-11-16), and with no label; the posted bodies, byte for byte, are in `issues-batch-1/`, one file per issue, named by its number (`524.md` to `529.md`). GitHub stamps them 2026-11-17 00:27:54 to 00:29:08 UTC, the evening of 2026-11-16 local (UTC-6). The paragraph above, "**Nothing is posted.**" and the rest of it, is overtaken by this one and stays as written (`metrics/FILED.md`, *Dashboarr notes*).

**Target:** `RenzoBeux/Dashboarr`, `main` at `67f9eff06f574601b819f759cd26b83f029719b9` (`67f9eff`, committed 2026-11-14 14:09:52 UTC, the release of v1.23.0; `gh api --method GET "repos/RenzoBeux/Dashboarr/commits?sha=main&per_page=1" --jq '.[0].sha'`, read 2026-11-16 04:24:39 UTC and again at 04:34:42 UTC, after the re-check, unchanged), 11 commits after `bf3a060`, the sha every run and the judge read (`compare/bf3a060...67f9eff`: ahead by 11, behind by 0). `main` is the repo's only branch (`branches`), so there is no dev branch to re-check (FILING §3). Not archived, issues on, 28 open items on the repo's count, 23 issues and 5 pull requests by `search/issues`. The 11 commits, each a merged pull request: #495 (Maintainerr collections), #513 (VPN tunnel diagnostics on iOS), #516 (Lidarr cover routes), #517 (a configurable XML-RPC path for rTorrent instances, closing #504), #509 and #519 (iOS Face ID text and permissions), #505 (unRAID capacity units), #520 (the downloads speed line), #521 (Seerr request paging), and the two release commits. What each does to a group is said under it.

**The form:** Dashboarr has no issue template on `main` (the community profile's `issue_template` is null; `.github` holds `FUNDING.yml`, `dependabot.yml` and `workflows` only, as at `bf3a060`), no CONTRIBUTING and no security policy (`reviews/dashboarr/2026-11-07-ai-policy-check.md`; the community profile's `contributing` and `code_of_conduct` are null on `main` too), so FILING §5's form is used as it stands, and no rule on AI-assisted reports has appeared since the check.

**The order** (`testing/CONTROL.md` §15): worst first by the weight of the group's final severity (§12: data-loss 4, wrong-result 3, crash 3), and between equal weights by the group's first claim in `claims.md`'s order (XC JV PQ TH GN QX WS JW CD TJ HT QT JM LQ RW), which the judge's group numbers follow; six to a batch. From `verdicts.md` and `score.md`'s *Groups* list:

| Batch | Groups in order, with their claims in `claims.md` order |
|---|---|
| 1 | 1 (XC, RW), 2 (JV), 3 (PQ), 5 (GN, CD), 6 (QX), 9 (TJ): data-loss |
| 2 | 10 (HT, QT), 12 (LQ): data-loss; 4 (TH): wrong-result; 11 (JM): crash |
| not filed | 7 (WS), 8 (JW): stuck, in the ledger only (FILING §4) |

Arm lines: group 1 A+B, group 2 B, group 3 B, group 5 A+B, group 6 A, group 9 A. Ledger rows: group 1 `DA-L04`, group 5 `DA-L03`, group 6 `DA-L09`, group 9 `DA-L05` (arm A's, `control:A` or `control:A+B`); groups 2 and 3 are the `control:B` rows `DA-L10` and `DA-L11`, filed while the block is open as monize's batch 2 filed MZ-L13 (#2073). No claim is a security finding, none was refuted, and Garrett has held none back.

**Where the steps start** (`RULES.md` R491): each draft's steps start from an action a user takes in the app, on a screen, with a button or by an import. Four start at an editor's Save or at the Export and Import rows (drafts 1, 3, 4 and 6), one at a dashboard widget's Delete (draft 2), one at an import that fails partway (draft 5, which needs a fault: a keychain write that fails, or the app killed while the import runs). None rests on a crafted input. Draft 6's starting state, a service URL stored without a scheme, is created by no door on today's build: it is legacy data from an install that saved the URL before #73, read by the shell session as a user's stored configuration rather than a crafted input, and flagged for Garrett below.

## The re-check and the duplicate search (FILING §3), 2026-11-15

**The re-check, without a clone.** The trees at `bf3a060` and `67f9eff` were fetched read-only (`gh api --method GET "repos/RenzoBeux/Dashboarr/git/trees/<sha>?recursive=1"`, 04:25:23 UTC, neither truncated: 1,101 and 1,107 blobs), and every file the drafts cite was compared by its blob sha at the two. Of the 24 files cited across the six groups, 17 have the same blob at both shas and 7 differ: `store/config-schema.ts`, `components/integrations/service-editor.tsx`, `lib/http-client.ts`, `lib/url-validation.ts`, `services/backend-api.ts`, `store/config-migrations.ts` and `docs/guide.html`. Each of those seven was fetched at both shas (`gh api --method GET "repos/RenzoBeux/Dashboarr/contents/<path>?ref=<sha>" -H "Accept: application/vnd.github.raw"`, 04:26:01 to 04:26:09 UTC, each copy's `git hash-object` equal to its tree's blob) and the two copies compared line by line: every change is #517's rTorrent XML-RPC path (a new optional field in the validator, the editor, the request path and the backend sync; a v64 migration that only stamps the version; a guide row) or #513's VPN diagnostics (two guide paragraphs), none at a cited line, and each cited range was found again on `main` as the same text at new line numbers. *Unchanged* means the same blob at `bf3a060` and `main`; *moved*, the same code at new line numbers; *changed*, the cited line itself rewritten since the read; *fixed*, the mechanism gone. No `main` commit since `bf3a060` touches any group's mechanism: all six are **moved** (each cites at least one of the seven shifted files), none is changed, none is fixed, and none is filed upstream, so all six are drafted and none is held back. The drafts name `67f9eff` with `main`'s line numbers, read at `bf3a060`. Of the 54 files the 11 commits touch, one is a batch 2 file, `home-networks.tsx` (group 11); none is a batch 1 file but the seven above. The five open pull requests, #523 (Bindery search), #483 (library search and list view), #467, #466 and #465 (AdGuard screens, drafts since 2026-10-02), touch none of the cited files (`gh pr view <n> --json files`).

**The duplicate search.** Phrase searches, both states, `gh search issues --repo RenzoBeux/Dashboarr "<words>" --limit 50` and `gh search prs ... --limit 50`, 27 terms, from 04:27:30 UTC; GitHub's search limit stopped the run after the 15th term ("header value") at 04:27:54, and the remaining 12 terms ran again from 04:29:42 to 04:30:00 UTC, each answered. Words-apart searches, `gh issue list` and `gh pr list --repo RenzoBeux/Dashboarr --state all --search "<words>" --limit 50`, two terms a group, 04:30:46 to 04:30:59 UTC. As a cross-check, the titles and bodies of all 516 issues and pull requests (290 issues, 226 pull requests, through #523; `gh api --method GET "repos/RenzoBeux/Dashboarr/issues?state=all&per_page=100" --paginate`, 04:26:16 UTC) were searched for the function names and the user's words below, and the 23 open issue titles were read by eye (#515, #514, #512, #510, #508, #507, #503, #498, #490, #489, #478, #477, #476, #462, #455, #453, #451, #448, #445, #437, #430, #391, #37: SABnzbd, the calendar, notifications, feature and integration requests, the VPN detection of #489; none on a backup, an export, Demo Mode, a Seerr delete or a stored URL). None of the six is reported, open or closed, and no open pull request fixes one. The reviewer's searches of 2026-11-08 (its drafts file) found the same for the four groups it drafted.

- **Group 1 (draft 1).** Moved. `store/config-schema.ts`: #517 added one import above and five lines at `:149-153`, so `coerceWolDevice` is `:178-192` (`bf3a060`: 172-186) and the `wolDevices` loop with its throw `:619-626` (613-620), the same text. The editor `wake-on-lan.tsx`, `store/config-store.ts` (the export at `:2764-2771`, `buildExportPayload` at `:3088-3135`, the import's validate-before-write at `:2856-2857`), `services/backend-backup.ts` and `settings/backup.tsx`: unchanged. Searches: "wake on lan": issues none, PRs #409, #438 (navigation, the shortcuts widget), words "wake on lan backup" none and none; "wolDevices": issues #344 (the shortcuts widget request, which names the field in passing), PRs none, words "wolDevices invalid" none and none; "invalid config", "backup restore", "coerceWolDevice", "validateExportPayload", "restore backup", "cannot restore": none in all; "import settings": issues #168 (import between phones, closed), PRs none; "export settings": issues #180 (an error message after an export to another app, fixed by #187), #84 (the keyboard over the export screen), PRs none; "import fails": issues none, PRs #261 (grab history). Bodies: `wolDevices` 1 (#344), `coerceWolDevice` and `validateExportPayload` none, "Invalid config" and "entry is invalid" none, a backup beside a restore 13 (#424 and #425, the backend backup feature; the rest release notes and dependency bumps). None reports this. Nearest: #425 (merged), which made the backend slot carry the same payload as the export file.
- **Group 2 (draft 2).** Moved. `hooks/use-radarr.ts`, `services/overseerr-api.ts`, the movie page and the three dashboard widgets, and `hooks/use-workspace-instances.ts`: unchanged. `lib/http-client.ts`: #517 added `apiBasePathFor` above `serviceRequest`, so its active-instance fallback is `:542-543` (528-529), the same text. #521 changed `hooks/use-overseerr.ts` (request paging), not the delete path. Searches: "delete movie": issues #318, #83, #130 (a mix-up in a widget, a crash on delete in May, a wrong year), PRs #72 (a batch of May fixes); "seerr delete": issues none, PRs #259 (Seerr's delete-request and remove-media actions); "overseerr delete", "media record", "deleteMedia": none in all; words "seerr delete movie": 1 and 2 (#257, #259, #281), "deleteMedia instance": none and none. Bodies: `deleteMedia`, `getActiveInstanceId` and `useDeleteMovie` none; a Seerr beside a delete 5 (#281, #259, #257, #201, #186), each the Seerr tab's own actions. None reports this. Nearest: #332, after which the hook skips the cleanup for a Seerr signed in as a plain member; the instance it picks was not changed.
- **Group 3 (draft 3).** Moved. `components/integrations/service-editor.tsx`: #517 added the XML-RPC path field and its checks, so the name check in `performSave` is `:365-369` (352-356), the header checks `:398-408` (380-390) and the Name input `:923-929` (898-904), the same text. `store/config-schema.ts` as group 1's: `coerceHeaderMap` `:58-70` (57-69), its name and value limits `:63-65` (62-64), its count `:68` (67); `coerceServiceInstance`'s name limit `:77` (76); the throws `:525` (519), `:543` (537) and `:548` (542). `custom-headers.tsx`, `components/ui/header-list-editor.tsx` and `components/ui/text-input.tsx`: unchanged. Searches: "service name": none in all, words "service name 200": 4 and 5 (common words; none on a name's length); "custom headers": issues #26 (the request for the feature), #239 (a proxy's auth), PRs #409, #444, #176, #138; "header value": none, words "header value 4096": none and none. Bodies: a name over 200 characters or `maxLength` none, "custom header" 4 (#444, #409, #176, #26). None reports this. Nearest: #26 (closed), the feature's request.
- **Group 5 (draft 4).** Moved. `store/config-store.ts` (`exportConfig` `:2764-2771`, `buildExportPayload` `:3088-3135`, `enableDemoMode` `:2716-2756`), `services/backend-backup.ts` (`:79`) and `settings/backup.tsx` (`:131-137`, `:154-165`, `:193`): unchanged. `services/backend-api.ts`: #517 added three lines at `:314-316`, below the demo check, which is `:275` at both. `docs/guide.html`: #513 added three lines above, so "Demo Mode never uploads" is `:1146` (1143); the promise at `:263` is at both. Searches: "demo mode": issues none, PRs 36 (#499, #495, #491, #496, #474, #419, #410, #443, #469, #411, #424, #368, #369, #444, #353, #349, #392, #413, #363, #324, #377, #301, #305, #312, #367, #376, #260, #261, #232, #190, #166, #162, #160, #92, #143, #13), each a feature adding its own demo data; words "demo mode export": none and 5, "export settings demo": none and 1 (#424). Bodies: "demo mode" 34, the same features; an export beside Demo Mode none but #424's description of the backend backup's demo guard. None reports this. Nearest: #424 and #425 (merged), whose backend backup skips Demo Mode where the file export does not.
- **Group 6 (draft 5).** Moved. `store/config-store.ts` (`importConfigFromPayload` `:2852-3077`), `store/backend-store.ts` (`pair` `:149-156`), `store/storage.ts` (`:46-52`) and `settings/backup.tsx` (`:117`): unchanged. `lib/http-client.ts`: the request path's read of the store's secrets is `:550` (536), the same text. Searches: "api key lost", "import secrets": none in all; "keychain": issues none, PRs #187 (a keychain race on export, fixed); words "import secrets deleted", "import failed keychain": none and none. Bodies: a secret or key beside lost, wiped or deleted 1 (#274, a build file), `SecureStore` beside an import none. None reports this. Nearest: #187 (merged), which moved a keychain write out of a race in the export; the import's order is as read.
- **Group 9 (draft 6).** Moved. `store/config-store.ts` (`getActiveUrl` `:2615-2623`, `isServiceInstance` `:824-834`, hydrate's list read `:959-963`, the export's `:3112`): unchanged. `store/config-schema.ts`: `isHttpUrlOrEmpty` `:42-51` (41-50), its two calls `:78-79` (77-78), the throw `:525` (519). `lib/url-validation.ts`: #517 appended its XML-RPC helpers at `:192-226`, so `normalizeServiceUrl` is `:54-59` at both. `components/integrations/service-editor.tsx`: the Save's normalizing `:371-374` (358-361). Searches: "url scheme": issues none, PRs #276 (magnet links); "http prefix": issues none, PRs #73 (the editor's `http://` prefix); "without scheme": none; "normalizeServiceUrl": issues none, PRs #221, #73; words "url scheme import": 1 and 1, "http prefix export": none and 1. Bodies: `normalizeServiceUrl` 2 (#221, #73), `isHttpUrlOrEmpty` none, a missing scheme or prefix 1 (#73). None reports this. Nearest: #73 (merged 2026-05), which added the prefix in the editor for new saves, and #106 (closed), the disconnected-services report the read-time normalizing cites in its comment.

---

## Draft 1 (group 1)

**Title:** [Bug] A Wake-on-LAN device saved with a port such as 70000 makes every later backup impossible to restore

**Version:** `main` at `67f9eff`. Read at `bf3a060`; the code below is the same at the two, `store/config-schema.ts` at new line numbers on `main`, and the line numbers are `main`'s.

**Summary:** The Wake-on-LAN editor saves a device after checking only that the name and the MAC are not empty, and turns the port field into `Number(port.trim()) || 9` (`app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx:80-92`), so 70000, 1.5 or -7, or a MAC with a note pasted after it, is stored with a success toast. The export file and the backend backup carry the device as stored (`store/config-store.ts:2764-2771` and `buildExportPayload` at `:3088-3135`; `services/backend-backup.ts:40-46`). Only the import validates: `coerceWolDevice` requires an integer port from 1 to 65535, a MAC of at most 32 characters, a name of at most 200 and a broadcast address of at most 45 (`store/config-schema.ts:178-192`), the first device it refuses throws for the whole file (`:619-626`), and the import validates before it writes anything (`store/config-store.ts:2856-2857`).

**Result:** every backup made after that device was saved, the export file and the backend slot alike, fails to restore with "Config wolDevices entry is invalid", shown under "Invalid config file" (`app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:117`), and nothing from it is restored: services, API keys, dashboards and home networks are all missing on the new phone. The message names no device and no field, and the user learns of it only when the backup is needed.

**Where:** `app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx:80-92`; `store/config-schema.ts:178-192`, `:619-626`; `store/config-store.ts:2764-2771`, `:2856-2857`, `:3088-3135`; `services/backend-backup.ts:40-46`.

**Steps:**
1. Settings > Wake on LAN > Add: name "Media Server", MAC `00:11:22:33:44:55`, port `70000` (or `1.5`, or `-7`, or a MAC with a note pasted after it). Save. The screen accepts it and toasts "Media Server added".
2. Settings > Backup & Storage > Export settings, and save the file; or leave the backend backup on, which uploads the same payload.
3. On a new phone, or after a reinstall, Import settings with that file, or restore the backend slot.

**Expected:** the editor refuses the values the import refuses, or the import drops the one bad device and restores the rest.

**Actual:** "Invalid config file": the whole import is refused and nothing is restored.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the editor's `handleSave`, `coerceWolDevice` and the import's `wolDevices` loop. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe-wol-port.js`, plain Node, standard library only):
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

**Related:** the service editor and the Custom Headers screen have the same gap for a name over 200 characters and a header value over 4096, reported separately. #517 shows the other way to close it: for the new XML-RPC path field, the import drops a malformed value and falls back to the default instead of refusing the instance (`store/config-schema.ts:149-153`).

**Possible fix:** give the editor the validator's limits (an integer port from 1 to 65535, a MAC of at most 32 characters, a name of at most 200, a broadcast address of at most 45), and in the import skip or clamp a bad device, with its name in the message, instead of throwing for the file, as `coerceServiceInstance` drops a malformed `rpcPath`. A test: a device saved through the editor's path with port 70000, exported and imported, restores with the rest of the configuration, or the editor refused it.

*Outside the issue:* Arm: A+B. Claims XC (arm A run 1, finding 4) and RW (arm B run 1, finding 1), both final data-loss. Both arms have claims here, so the clearer steps were taken: RW's (arm B run 1), which name both doors, the export file and the backend slot, and the import's message; XC's folded in the service-name and header gaps, which are group 3's (draft 3). The probe output is arm B's `probe-wol-port.js` as its report prints it (`arm-b-1-probes/`); arm A's probe and the judge's two programs reproduced the same four values. *Related*'s #517 precedent and the message's wording under "Invalid config file" are the shell session's reading at the re-check, in no claim. Ledger row `DA-L04` (`control:A+B`).

---

## Draft 2 (group 2)

**Title:** [Bug] Deleting a movie from a second Radarr also deletes its record on the dashboard's active Seerr, which may be another Seerr or still cover another Radarr's copy

**Version:** `main` at `67f9eff`. Read at `bf3a060`; the code below is the same at the two, `lib/http-client.ts` at new line numbers on `main`, and the line numbers are `main`'s.

**Summary:** `useDeleteMovie` deletes the movie on the Radarr instance the page was opened with, then tidies Seerr so the movie can be requested again: `getSeerrMe()`, `getMovieDetails(tmdbId)` and `deleteMedia(mediaId)`, each called with no instance id (`hooks/use-radarr.ts:185-187`, `:208-218`). A Seerr request with no instance id goes to the active dashboard's Seerr (`services/overseerr-api.ts:86-93`, `:158-160`; `lib/http-client.ts:542-543` the same), though both functions take an `instanceId` (`services/overseerr-api.ts:650-656`, `:670-675`). The movie page takes its Radarr from the route (`app/(tabs)/(dashboard,downloads,calendar,movies,tv,library,music,books,bazarr)/movie/[id].tsx:108`), and the Calendar, Still Pending and Recently Downloaded widgets route to it with each item's own Radarr id (`components/dashboard/calendar-card.tsx:262`, `still-pending-card.tsx:270`, `recently-downloaded-card.tsx:233`), so a movie from a second Radarr is deleted there while the Seerr cleanup goes wherever the dashboard points. The confirm names only Radarr (`movie/[id].tsx:518-522`); the comment at `use-radarr.ts:188-189` calls the cleanup "a UX nicety".

**Result:** Seerr's `DELETE /media/{id}` removes the whole media record, its requests and its availability included, on a Seerr that was never named and still has the movie through its own Radarr. With one Seerr tracking a 1080p and a 4K Radarr, deleting the 4K copy drops the record that also covered the 1080p copy. Nothing on screen says Seerr was touched.

**Where:** `hooks/use-radarr.ts:185-222` (`:185-187`, `:188-189`, `:208-218`); `services/overseerr-api.ts:86-93`, `:158-160`, `:650-656`, `:670-675`; `lib/http-client.ts:542-543`; `app/(tabs)/(dashboard,downloads,calendar,movies,tv,library,music,books,bazarr)/movie/[id].tsx:108`, `:518-522`; `components/dashboard/calendar-card.tsx:262`, `components/dashboard/still-pending-card.tsx:270`, `components/dashboard/recently-downloaded-card.tsx:233`.

**Steps:**
1. Configure two Radarr instances, Home and Cabin, and two Seerr instances, Home Seerr managing Home Radarr and Cabin Seerr managing Cabin Radarr. Use a dashboard that shows every instance (one with no attachment list does), with Home Seerr as its active Seerr: the first one, or the one chosen with the instance chip.
2. In that dashboard's Calendar, Still Pending or Recently Downloaded widget, open a movie that belongs to Cabin Radarr.
3. Actions > Delete > Delete. The confirm says "Remove "<title>" from Radarr. Files on disk will be kept."
4. Open Home Seerr and look up the movie.

**Expected:** the movie is removed from Cabin Radarr; any Seerr cleanup goes to Cabin Seerr, the one that manages that Radarr, or to none; and the confirm says so if Seerr is touched.

**Actual:** Cabin Radarr loses the movie, and Home Seerr loses its media record for that title, requests and availability included, though Home Radarr still has the movie.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** #332 made the hook skip the cleanup for a Seerr signed in as a plain member, who could not delete media; the instance it picks was not changed. The series delete and the Seerr tab's own Remove action were not read for this report.

**Possible fix:** pass the Seerr that manages the deleted movie's Radarr to `getMovieDetails` and `deleteMedia`, the one attached beside it on the dashboard, and skip the cleanup when the dashboard holds more than one Seerr with no way to tell which; or name Seerr in the confirm ("also remove from Seerr <name>") and let the user opt out. A test: with two Radarr and two Seerr instances on one dashboard, deleting a Cabin movie opened from a widget sends `DELETE /media` to Cabin Seerr or to none, never to Home Seerr.

*Outside the issue:* Arm: B. Claim JV (arm B run 1, finding 4; final data-loss), the group's only claim; its evidence is reading, and no probe ran on this group's code in any run, so the issue carries no program clause and no probe output. The claim's steps had each dashboard attached to its own Radarr and Seerr pair; judge run 2 read that with that setup the Home dashboard's widgets list Home Radarr's items only (`useWorkspaceScopedInstances`, `calendar-card.tsx:12`, `hooks/use-workspace-instances.ts:64-79`), and that the defect is reached when the active dashboard attaches both Radarrs but one Seerr is active, when the movie page is opened with the other Radarr's id while the first dashboard is active, or with one Seerr tracking a 1080p and a 4K Radarr. So the steps use a dashboard that shows every instance, the shell session's reading of the judge's notes, and the 1080p and 4K case is in *Result*. Judge run 1 noted it did not verify Seerr's server-side meaning of `DELETE /media/{id}`; the misrouted call is in the code. **Flagged for Garrett:** reading with no probe, and the steps' door is the shell session's. Ledger row `DA-L10` (`control:B`).

---

## Draft 3 (group 3)

**Title:** [Bug] A service name longer than 200 characters, or a custom header value longer than 4096, is saved but makes every later backup impossible to restore

**Version:** `main` at `67f9eff`. Read at `bf3a060`; the code below is the same at the two, `components/integrations/service-editor.tsx` and `store/config-schema.ts` at new line numbers on `main`, and the line numbers are `main`'s.

**Summary:** The service editor refuses only an empty name (`components/integrations/service-editor.tsx:365-369`), and its Name field has no length limit (`:923-929`); its header check, and the Custom Headers screen's, look at the header name's characters and at line breaks in the value only (`:398-408`; `app/(tabs)/(dashboard,services,settings)/custom-headers.tsx:28-38`), with a comment that says the check mirrors the schema validator (`service-editor.tsx:395-396`). The import's `coerceServiceInstance` returns null for a name over 200 characters (`store/config-schema.ts:77`), and `coerceHeaderMap` for a header name over 200 or a value over 4096 (`:63-65`); one null throws for the whole file, "Config services.<kind> entry is invalid" (`:525`), "Config secrets.<uuid> is invalid" (`:543`) or "Config globalCustomHeaders is invalid" (`:548`). The export file and the backend backup write the payload unvalidated. The number of headers is capped at 32 by the editor and the validator alike (`components/ui/header-list-editor.tsx:21`, `:60`, `:120`; `store/config-schema.ts:68`), so that limit agrees.

**Result:** the whole backup fails to restore, as with the Wake-on-LAN device: services, API keys, dashboards and home networks are all missing on the new phone. The values are unlikely, but the loss is total and silent until the restore.

**Where:** `components/integrations/service-editor.tsx:365-369`, `:395-408`, `:923-929`; `app/(tabs)/(dashboard,services,settings)/custom-headers.tsx:28-38`; `store/config-schema.ts:58-70` (`:63-65`), `:77`, `:525`, `:543`, `:548`; `components/ui/header-list-editor.tsx:21`, `:60`, `:120`.

**Steps:**
1. Settings > Integrations > a service: paste a name longer than 200 characters into Name (a pasted line of notes will do) and Save; the editor checks only that it is not empty. Or Settings > Custom Headers: add a header whose value is longer than 4096 characters, a long token, and Save; the screen checks the header's name and line breaks only.
2. Settings > Backup & Storage > Export settings, or let the backend backup upload.
3. Import the file on a new phone.

**Expected:** the editors refuse what the import refuses, or the import trims or drops the one field and restores the rest.

**Actual:** "Invalid config file": the whole import is refused and nothing is restored.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `coerceServiceInstance` name check and the `coerceHeaderMap` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`validators.js`, plain Node, standard library only; the validator's side):
```
--- service name > 200 (coerceServiceInstance line 76)
201 chars rejected: true
--- header maps
33 headers: REJECTED
value 4097: REJECTED
key 201: REJECTED
```
(The 33rd header cannot be added in the app, whose header editor stops at 32 rows; the name and the value limits are the ones the editors leave out.)

**Related:** the Wake-on-LAN editor has the same gap for a device's port, MAC and name, reported separately. #517's new XML-RPC path field shows the other way to close it: the import drops a malformed value and falls back instead of refusing the instance (`store/config-schema.ts:149-153`).

**Possible fix:** a `maxLength` of 200 on the Name field and the header-name field and of 4096 on the header-value field, or the three limits added to the editors' checks beside the name regex they already mirror; and in the import, drop the one field or header with a warning instead of throwing for the file. A test: a 201-character name saved through the editor's path, exported and imported, restores, or the editor refused it; the same for a 4097-character header value.

*Outside the issue:* Arm: B. Claim PQ (arm B run 1, finding 5; final data-loss), the group's only claim; its steps, but for its 33rd-header step, which both judges refuted (the header editor caps its rows at 32), so the steps use the name and the header value, and the header name over 200, judge run 1's reading, is in *Summary*. The probe output is the judge's (run 1, `judge-1-probes/validators.js`), on the validator's side; that the editors set no cap is reading, by arm B and both judges; the comment on mirroring the validator and *Related*'s #517 precedent are the shell session's reading at the re-check. Ledger row `DA-L11` (`control:B`), whose title keeps the claim's 32-header wording.

---

## Draft 4 (group 5)

**Title:** [Bug] "Export settings" while Demo Mode is on writes a backup of the demo data, not the user's configuration

**Version:** `main` at `67f9eff`. Read at `bf3a060`; every file below is the same at the two but `docs/guide.html`, where the quoted line moved; the line numbers are `main`'s.

**Summary:** `exportConfig` encrypts `buildExportPayload()` (`store/config-store.ts:2764-2771`, `:3088-3135`), which reads the live store. `enableDemoMode` replaces the service instances with one `http://demo.local` instance per kind, empties the secrets map and strips every dashboard's attachment list, in memory (`:2716-2756`). The two other paths that send the configuration out check Demo Mode and skip: the backend backup (`services/backend-backup.ts:79`; the guide says "Demo Mode never uploads", `docs/guide.html:1146`) and the backend sync (`services/backend-api.ts:275`). The file export does not, and its row sits one group above the Demo Mode switch on the same screen, disabled only while an export is running (`app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:131-137`, `:154-165`).

**Result:** a passphrase-protected file named like a real backup that holds one fake instance per service, no API key or password and no workspace attachment. Importing it, which "will overwrite all current settings" (`settings/backup.tsx:193`), replaces every real server, key and attachment with the demo set.

**Where:** `store/config-store.ts:2764-2771`, `:3088-3135`, `:2716-2756`; `services/backend-backup.ts:79`; `services/backend-api.ts:275`; `app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:131-137`, `:154-165`, `:193`.

**Steps:**
1. Settings > Backup & Storage: under Advanced, turn Demo Mode on.
2. On the same screen tap Export settings, authenticate, enter a passphrase and save the file.
3. Later, on this or another phone, Import settings with that file.

**Expected:** the export is refused or disabled while Demo Mode is on, as the backend backup and the backend sync already are; or it exports the real, stored configuration.

**Actual:** the export succeeds; the file holds the demo instances and no secrets; the import replaces the real configuration with them.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `enableDemoMode` and `buildExportPayload` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe-demo-export.js`, plain Node, standard library only):
```
demoMode: true
exported services: {"qbittorrent":[{"id":"demo-uuid-1","enabled":true,"name":"qBittorrent","localUrl":"http://demo.local","remoteUrl":"","useRemote":false,"ignoreCertErrors":false}],"radarr":[{"id":"demo-uuid-2","enabled":true,"name":"Radarr","localUrl":"http://demo.local","remoteUrl":"","useRemote":false,"ignoreCertErrors":false}]}
exported secrets:  {}
real instances in the backup file: 0; real secrets in the backup file: 0
```

**Related:** the backend backup, added by #425, came with its Demo Mode check; the older file export never gained one. The guide promises of Demo Mode: "Turn it off and everything comes back exactly as it was" (`docs/guide.html:263`).

**Possible fix:** in `exportConfig`, return with a toast while `demoMode` is true, the check `uploadConfigBackup` makes, or disable the Export row while the switch is on. A test: enable Demo Mode, call `exportConfig`, and assert nothing is written, or that the payload equals the stored configuration.

*Outside the issue:* Arm: A+B. Claims GN (arm B run 1, finding 3) and CD (arm A run 1, finding 3), both final data-loss. Both arms have claims here, so the clearer steps were taken: GN's (arm B run 1), three steps that name the two guarded paths the export should match; CD's four say the same. The probe output is arm B's `probe-demo-export.js` as its report prints it (`arm-b-1-probes/`); arm A's probe (its step 2b) shows the same empty secrets. *Related*'s history of #425 is the shell session's reading at the re-check, from the pull request's description. Ledger row `DA-L03` (`control:A+B`).

---

## Draft 5 (group 6)

**Title:** [Bug] An import that fails partway deletes the old API keys for good and leaves a half-written configuration for the next launch

**Version:** `main` at `67f9eff`. Read at `bf3a060`; the code below is the same at the two, `lib/http-client.ts` at a new line number on `main`, and the line numbers are `main`'s.

**Summary:** `importConfigFromPayload` validates the file (`store/config-store.ts:2856-2857`), then deletes every current instance's API key, username, password and custom headers from the keychain (`:2868-2873`) and writes the imported service lists to storage (`:2877-2885`), before the steps that can still fail: the imported secrets' keychain writes (`:2891-2899`; `store/storage.ts:46-52`), the backend pairing's keychain writes (`:2978-2984`; `store/backend-store.ts:149-156`) and the Seerr session drains (`:3029-3036`), each awaited. The `try/finally` around the end only releases the Seerr login suspensions (`:3027`, `:3069-3071`); nothing rolls back, and the in-memory `set()` comes last (`:3040`). A throw anywhere there is shown as "Invalid config file" (`app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:117`), though the file was valid and part of it is already in storage.

**Result:** the old secrets are gone from the keychain and are not restored. The running app keeps working from its in-memory copy of them (`lib/http-client.ts:550` reads the store's secrets), so the user, told the file was invalid, sees nothing wrong until the next launch, which loads the imported service lists with whichever secrets had been written and none of the old ones: the old instances' keys cannot be recovered, and the new ones may be missing.

**Where:** `store/config-store.ts:2856-2857`, `:2868-2873`, `:2877-2885`, `:2891-2899`, `:2978-2984`, `:3027-3040`, `:3069-3071`; `store/storage.ts:46-52`; `store/backend-store.ts:149-156`; `app/(tabs)/(dashboard,services,settings)/settings/backup.tsx:117`.

**Steps:**
1. With real services configured, Settings > Backup & Storage > Import settings, with a valid backup, and let the import be interrupted after it has started: the app killed while it runs, or a keychain write that fails (the import awaits each one). The failing step cannot be forced from a screen; the order of the writes is the defect.
2. If "Invalid config file" appears, dismiss it. The app still shows the old services, and they still work.
3. Relaunch the app.

**Expected:** a failed import changes nothing, or reports what was and was not restored.

**Actual:** after the relaunch the imported service lists are there, with whichever secrets had been written; the old instances' keys are gone from the keychain.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Possible fix:** write the imported lists and secrets first and delete the old secrets last, after the in-memory `set()`; or keep the old secrets aside and put them back in a `catch`, with the stored lists. A test: an import whose first secret write rejects leaves the old secrets in the keychain and the stored lists unchanged.

*Outside the issue:* Arm: A. Claim QX (arm A run 1, finding 6; final data-loss), the group's only claim; its evidence is reading, and no probe ran on this group's code in any run, so no program clause and no probe output. *Result* follows judge run 2's correction of the claim: before the relaunch the old instances keep their keys in memory and requests keep working, so the loss shows at the next launch, not at once. The trigger is a fault, a keychain write that fails or the app killed mid-import, not a plain user action; the steps say so. **Flagged for Garrett:** reading with no probe, and a fault needed to reach it. Ledger row `DA-L09` (`control:A`).

---

## Draft 6 (group 9)

**Title:** [Bug] A service URL saved without "http://" on an older build is exported as stored and rejected on import, so that backup cannot be restored

**Version:** `main` at `67f9eff`. Read at `bf3a060`; the code below is the same at the two, `store/config-schema.ts` and `components/integrations/service-editor.tsx` at new line numbers on `main`, and the line numbers are `main`'s.

**Summary:** `getActiveUrl` adds `http://` on every read of a stored URL that has no scheme, its comment saying historical values can lack one (`store/config-store.ts:2615-2623`, after #106), and nothing rewrites the stored value: hydrate accepts any string URL (`:824-834`, `:959-963`), and only the service editor's Save normalizes, for the instance being edited (`components/integrations/service-editor.tsx:371-374`; `lib/url-validation.ts:54-59`). The export writes the instances as stored (`store/config-store.ts:3112`). The import's `isHttpUrlOrEmpty` parses with `new URL` and requires `http:` or `https:` (`store/config-schema.ts:42-51`, called at `:78-79`): `192.168.1.10:7878` throws in `URL`, and `server.local:7878` parses with protocol `server.local:`; either way the instance is refused and the whole file throws "Config services.<kind> entry is invalid" (`:525`). The editor's prefixing arrived with #73; a URL typed before it and never re-saved stays bare.

**Result:** the whole backup fails to restore, though the app has connected through that URL every day; the user learns of it only at restore time, on a new phone, with a message that names the service kind and not the URL.

**Where:** `store/config-store.ts:2615-2623`, `:824-834`, `:959-963`, `:3112`; `store/config-schema.ts:42-51`, `:78-79`, `:525`; `components/integrations/service-editor.tsx:371-374`; `lib/url-validation.ts:54-59`.

**Steps:**
1. On an install whose service URL was saved before the editor added the scheme (before #73), as `192.168.1.10:7878`, and never re-saved since: the app connects, since it adds `http://` when it reads the URL.
2. Settings > Backup & Storage > Export settings, and save the file; or let the backend backup upload.
3. Import the file on a new phone.

**Expected:** the import accepts the URL the app itself uses, or the export writes it normalized.

**Actual:** "Config services.radarr entry is invalid", under "Invalid config file"; nothing is restored.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `isHttpUrlOrEmpty` and `normalizeServiceUrl` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`validators.js`, plain Node, standard library only):
```
--- URLs without scheme (TJ)
"192.168.1.10:7878" URL.protocol: throws isHttpUrlOrEmpty: false normalized: http://192.168.1.10:7878 -> valid: true
"nas:7878" URL.protocol: nas: isHttpUrlOrEmpty: false normalized: http://nas:7878 -> valid: true
"localhost:7878" URL.protocol: localhost: isHttpUrlOrEmpty: false normalized: http://localhost:7878 -> valid: true
"http://192.168.1.10:7878" URL.protocol: http: isHttpUrlOrEmpty: true normalized: http://192.168.1.10:7878 -> valid: true
```

**Related:** #73 added the `http://` prefix in the editor for new saves; #106's disconnected services were fixed by normalizing on read, which left the stored values as they were. The Wake-on-LAN device and the name and header limits, reported separately, are the same pattern: the export writes what the import refuses.

**Possible fix:** normalize stored URLs once in hydrate and write them back, or run `normalizeServiceUrl` on each instance in `buildExportPayload`, or have `isHttpUrlOrEmpty` normalize before it parses, as the app does on read. A test: a stored instance whose `localUrl` is `192.168.1.10:7878` exports and imports.

*Outside the issue:* Arm: A. Claim TJ (arm A run 1, finding 5; final data-loss), the group's only claim; its steps. The probe output is the judge's (run 1, `judge-1-probes/validators.js`), which confirmed the numeric case by another path than the claim's: `URL` throws on `192.168.1.10:7878` rather than parsing a protocol that starts with a digit, and a host name parses with its own name as the protocol; either is a refusal. Judge run 2 found in the repo's history that the editor's prefixing arrived with #73's commit, so earlier saves kept what was typed; the claim's *Expected* and *Result* are kept. **Flagged for Garrett:** the starting state exists only on an install from before #73 (May 2026) whose instance was never re-saved, and no door on today's build creates it; the shell session read it as a user's stored configuration, legacy data rather than a crafted input (R491), and the steps say where it comes from. Garrett may hold this draft if the maintainer is likelier to answer that such installs no longer exist. Ledger row `DA-L05` (`control:A`).

---

## Not in this batch

- **Batch 2,** the four confirmed groups left, in the order of the table above: group 10 (HT, QT) and group 12 (LQ), data-loss, the Demo Mode writes that persist; group 4 (TH), wrong-result, the notification settings after an import; group 11 (JM), crash, the removed home network. Each is held by §9's cap of six, not by a reason, and waits for its own drafts and Garrett's go.
- **Not filed (FILING §4):** group 7 (WS), the backend backup slot that comes back after its delete, and group 8 (JW), the poster cache that grows in one storage row, both `stuck` by the judge's final verdicts, stay in the ledger (`DA-L12`, `DA-L07`).
- **Dropped by the re-check or the search:** none. No group is fixed on `main`, none is filed upstream, and no open pull request touches a cited file.

## Flagged for Garrett

Each draft Garrett should read before a go, and why:
- **Draft 2 (group 2, JV, `DA-L10`):** reading with no probe in any run; the steps' door, a dashboard that shows every instance, is the shell session's reading of judge run 2's notes, since the claim's own setup does not reach the bug; Seerr's server-side meaning of `DELETE /media/{id}` was not verified by the judge.
- **Draft 5 (group 6, QX, `DA-L09`):** reading with no probe; the trigger is a fault, a failed keychain write or the app killed during the import, and *Result* follows the judge's correction of the claim.
- **Draft 6 (group 9, TJ, `DA-L05`):** the starting state is legacy data from an install older than #73, created by no door on today's build; the shell session's judgement that this is a user's stored configuration, not a crafted input.
- **Draft 3 (group 3, PQ, `DA-L11`):** one step of the claim, the 33rd header, was refuted by both judges and dropped; the draft keeps the name and the header value, which both confirmed. The ledger row's title keeps the claim's wording.
- Drafts 1 and 4 (groups 1 and 5) rest on probes from both arms and the judge, start from a user's action and carry no judgement of the shell session beyond their *Related* lines.
