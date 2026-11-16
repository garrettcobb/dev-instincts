# Arm B's windows for dashboarr (testing/CONTROL.md §7)

Section 7's four windows with dashboarr's values, the record of what Garrett pastes for arm B's run 1 (section 13, step 3); each window is one paste. The coordinator's addition, 2026-11-07, for Garrett to confirm.

Amended 2026-11-08, before the run, after the coordinator's dry check in a scratch folder of its own (testing/CONTROL.md section 16, item 19 (a)): in window 1 the clone, checkout and status lines, and in window 3 the status line, carry `-c core.longpaths=true` right after `git` (after the path, for `git -C`), since on Windows the checkout of Dashboarr at bf3a060 fails with "Filename too long" on a route-group folder under `app/(tabs)/` without it, leaving a half-written checkout behind, and `status` then prints a false deletion for that folder; with it the checkout completes and `status --porcelain` prints nothing. Nothing else changed; the sha and every other value stand.

## Window 1: steps 1 and 2, before the run

```powershell
if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {
# 1. The folder and the clone
New-Item -ItemType Directory -Force $env:DEV_CONTROL_HOME\dashboarr\scratch | Out-Null
git -c core.longpaths=true clone --filter=blob:none --no-checkout https://github.com/RenzoBeux/Dashboarr $env:DEV_CONTROL_HOME\dashboarr\repo
git -C $env:DEV_CONTROL_HOME\dashboarr\repo -c core.longpaths=true -c advice.detachedHead=false checkout bf3a060a35170ba789f73195e3defaa0703e93e9
git -C $env:DEV_CONTROL_HOME\dashboarr\repo rev-parse HEAD           # bf3a060a35170ba789f73195e3defaa0703e93e9
git -C $env:DEV_CONTROL_HOME\dashboarr\repo -c core.longpaths=true status --porcelain       # prints nothing

# 2. Park the agents; check the folder has no memory yet
New-Item -ItemType Directory -Force $HOME\.claude\agents-parked | Out-Null
Move-Item $HOME\.claude\agents\*.md $HOME\.claude\agents-parked\
Get-ChildItem $HOME\.claude\agents                                       # lists nothing
$slug = (Join-Path $env:DEV_CONTROL_HOME dashboarr) -replace '[^A-Za-z0-9]', '-'    # the session folder's name in Claude Code (section 6)
Test-Path $HOME\.claude\projects\$slug                                   # False
}
```

## Window 2: step 3, the session

```powershell
# 3. Open the session, in a new PowerShell window
if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {
Set-Location $env:DEV_CONTROL_HOME\dashboarr
"/export $PWD\transcript.txt"                                            # prints the /export line to type at the end of the session
Remove-Item Env:DEV_INSTINCTS_HOME, Env:DEV_CONTROL_HOME
Test-Path Env:DEV_INSTINCTS_HOME, Env:DEV_CONTROL_HOME                   # False, False
$env:CLAUDE_CODE_DISABLE_CLAUDE_MDS = "1"
$env:CLAUDE_CODE_DISABLE_AUTO_MEMORY = "1"
claude --safe-mode --strict-mcp-config --model claude-fable-5-1 --effort high --permission-mode auto --tools "Read,Grep,Glob,Bash,Write,Edit" --disallowedTools "Bash(npm:*),Bash(npx:*),Bash(pnpm:*),Bash(yarn:*)"
}
```

## Window 3: step 4, after the session

```powershell
# 4. After the session, in another PowerShell window (step 3's has the variables removed)
if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {
$slug = (Join-Path $env:DEV_CONTROL_HOME dashboarr) -replace '[^A-Za-z0-9]', '-'
Copy-Item $HOME\.claude\projects\$slug\*.jsonl $env:DEV_CONTROL_HOME\dashboarr\    # first: the kept transcript (section 13.1)
git -C $env:DEV_CONTROL_HOME\dashboarr\repo -c core.longpaths=true status --porcelain --ignored    # prints nothing: nothing written, installed or built in the clone
$t = (Get-ChildItem $HOME\.claude\projects\$slug\*.jsonl).FullName
python -I $env:DEV_INSTINCTS_HOME\tools\control.py session $t --clone $env:DEV_CONTROL_HOME\dashboarr\repo --report $env:DEV_CONTROL_HOME\dashboarr\report.md --leak --prompt $env:DEV_INSTINCTS_HOME\reviews\dashboarr\2026-11-07-bf3a060-control\prompts\arm-b-1.txt
}
```

## Window 4: step 5, after the judge

```powershell
# 5. After the judge (section 10): move the agents back
Move-Item $HOME\.claude\agents-parked\*.md $HOME\.claude\agents\
Remove-Item $HOME\.claude\agents-parked
Get-ChildItem $HOME\.claude\agents       # dev-architect.md, instinct-reviewer.md, senior-coder.md
```

## Run 1 again, in dashboarr-2, 2026-11-08

The first attempt of 2026-11-08 (11:07 local) is void: its first message was not the prompt, and it read Dev Instincts (`metrics/CONTROL.md`, the void bullet; `testing/CONTROL.md` §16, item 20). Its folder, `$env:DEV_CONTROL_HOME\dashboarr\`, is deleted, and the run is made again in a fresh folder, `dashboarr-2`, section 13's rule, with the same prompt file, `prompts\arm-b-1.txt`; it is still arm B run 1. Windows 1, 2 and 3 re-filled: `dashboarr-2` in every folder path and in `$slug`, as section 7.1 does for a second run; window 1's step 2 keeps its two checks and drops the two agent moves, since the agents are parked (section 7.1); window 2 gains, after the `/export` line and before `Remove-Item`, the line that puts the prompt on the clipboard from the committed file, read as UTF-8, so the window is the clipboard's last writer; window 3's session check adds `--term dev-control/dashboarr/`, the void attempt's folder, and keeps `--prompt` naming `arm-b-1.txt`; the long-path flag stays on every git line that touches the clone. Window 4 is unchanged, as above. The coordinator's, 2026-11-08, for Garrett to confirm.

### Window 1: steps 1 and 2, before the run

```powershell
if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {
# 1. The folder and the clone
New-Item -ItemType Directory -Force $env:DEV_CONTROL_HOME\dashboarr-2\scratch | Out-Null
git -c core.longpaths=true clone --filter=blob:none --no-checkout https://github.com/RenzoBeux/Dashboarr $env:DEV_CONTROL_HOME\dashboarr-2\repo
git -C $env:DEV_CONTROL_HOME\dashboarr-2\repo -c core.longpaths=true -c advice.detachedHead=false checkout bf3a060a35170ba789f73195e3defaa0703e93e9
git -C $env:DEV_CONTROL_HOME\dashboarr-2\repo rev-parse HEAD           # bf3a060a35170ba789f73195e3defaa0703e93e9
git -C $env:DEV_CONTROL_HOME\dashboarr-2\repo -c core.longpaths=true status --porcelain       # prints nothing

# 2. The agents are parked already (section 7.1): check it, and that the folder has no memory yet
Get-ChildItem $HOME\.claude\agents                                       # lists nothing
$slug = (Join-Path $env:DEV_CONTROL_HOME dashboarr-2) -replace '[^A-Za-z0-9]', '-'    # the session folder's name in Claude Code (section 6)
Test-Path $HOME\.claude\projects\$slug                                   # False
}
```

### Window 2: step 3, the session

```powershell
# 3. Open the session, in a new PowerShell window
if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {
Set-Location $env:DEV_CONTROL_HOME\dashboarr-2
"/export $PWD\transcript.txt"                                            # prints the /export line to type at the end of the session
Get-Content $env:DEV_INSTINCTS_HOME\reviews\dashboarr\2026-11-07-bf3a060-control\prompts\arm-b-1.txt -Raw -Encoding UTF8 | Set-Clipboard   # the prompt onto the clipboard: paste it as the first message, copying nothing else first
Remove-Item Env:DEV_INSTINCTS_HOME, Env:DEV_CONTROL_HOME
Test-Path Env:DEV_INSTINCTS_HOME, Env:DEV_CONTROL_HOME                   # False, False
$env:CLAUDE_CODE_DISABLE_CLAUDE_MDS = "1"
$env:CLAUDE_CODE_DISABLE_AUTO_MEMORY = "1"
claude --safe-mode --strict-mcp-config --model claude-fable-5-1 --effort high --permission-mode auto --tools "Read,Grep,Glob,Bash,Write,Edit" --disallowedTools "Bash(npm:*),Bash(npx:*),Bash(pnpm:*),Bash(yarn:*)"
}
```

### Window 3: step 4, after the session

```powershell
# 4. After the session, in another PowerShell window (step 3's has the variables removed)
if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {
$slug = (Join-Path $env:DEV_CONTROL_HOME dashboarr-2) -replace '[^A-Za-z0-9]', '-'
Copy-Item $HOME\.claude\projects\$slug\*.jsonl $env:DEV_CONTROL_HOME\dashboarr-2\    # first: the kept transcript (section 13.1)
git -C $env:DEV_CONTROL_HOME\dashboarr-2\repo -c core.longpaths=true status --porcelain --ignored    # prints nothing: nothing written, installed or built in the clone
$t = (Get-ChildItem $HOME\.claude\projects\$slug\*.jsonl).FullName
python -I $env:DEV_INSTINCTS_HOME\tools\control.py session $t --clone $env:DEV_CONTROL_HOME\dashboarr-2\repo --report $env:DEV_CONTROL_HOME\dashboarr-2\report.md --leak --term dev-control/dashboarr/ --prompt $env:DEV_INSTINCTS_HOME\reviews\dashboarr\2026-11-07-bf3a060-control\prompts\arm-b-1.txt
}
```

### Window 4: step 5, after the judge

Unchanged: the window above, word for word.

The three windows above ran as written on 2026-11-08, at 11:30, 11:32 and 23:36 local (UTC-6), with the outputs their comments give: window 1 the clone at `bf3a060a35170ba789f73195e3defaa0703e93e9`, `status --porcelain` printing nothing, `$HOME\.claude\agents` listing nothing and `Test-Path` False; window 2 the clipboard set from `prompts\arm-b-1.txt` itself and the prompt pasted as the first message at 11:33:34; window 3 the `.jsonl` copied (SHA-256 b5fd61a999840bdd74a48c9972f7247d84e68cfa170f2d81f033f7661f2e5b9f, equal to the projects folder's), `status --porcelain --ignored` printing nothing, and the session check reading `arm-b-1.txt: matches`, `time used 18.3 min`, `instruction files loaded none` and `leak terms none found`, the output kept as `session-check-arm-b-1.txt` beside this file (run again at intake on the scrubbed transcript, every line but the transcript's name the same). Garrett's ruling on the check, 2026-11-09, "Yes, it stands" (`testing/CONTROL.md` §17; `metrics/CONTROL.md`, the provenance bullet). The coordinator's, 2026-11-09.
