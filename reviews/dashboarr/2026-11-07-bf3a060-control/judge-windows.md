# The judge's windows for dashboarr (testing/CONTROL.md §10)

Section 10's three windows with dashboarr's values, the record of what Garrett pastes for the judge's run 1 (section 13, step 7), in the form of `arm-b-windows.md`'s section of 2026-11-08; each window is one paste. The folder is `$env:DEV_CONTROL_HOME\dashboarr-judge\`. The clone, the checkout and every `status` line carry `-c core.longpaths=true` right after `git` (after the path, for `git -C`), since on Windows Dashboarr's checkout at bf3a060 fails without it (section 16, item 19 (a)); window 1 also runs `status --porcelain` after the checkout, as arm B's window 1 does, the one check that the clone is whole. The claims file copied in is the control folder's `claims.md`, public as written: no claim is a security finding, so there is no private file (section 13, step 6). Window 2 puts the prompt on the clipboard itself, from `prompts\judge-1.txt`, read as UTF-8, after the `/export` line and before the variables are removed, so the window is the clipboard's last writer (section 16, item 20). Window 3's check takes `--term dev-control/dashboarr/` and `--term dev-control/dashboarr-2/`, arm B's two folders, the void attempt's and the run's (section 9), and `--prompt` naming `judge-1.txt`. The coordinator's, 2026-11-09, for Garrett to confirm.

In the session: paste the prompt as the first message, and type nothing else; a question gets section 7's fixed reply, word for word; when it says the file is written, type the `/export` line window 2 printed, then `/exit`, at once (section 16, item 21).

## Window 1: step 1, before the run

```powershell
if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {
# 1. The folder, the clone and the claims
New-Item -ItemType Directory -Force $env:DEV_CONTROL_HOME\dashboarr-judge\scratch | Out-Null
git -c core.longpaths=true clone --filter=blob:none --no-checkout https://github.com/RenzoBeux/Dashboarr $env:DEV_CONTROL_HOME\dashboarr-judge\repo
git -C $env:DEV_CONTROL_HOME\dashboarr-judge\repo -c core.longpaths=true -c advice.detachedHead=false checkout bf3a060a35170ba789f73195e3defaa0703e93e9
git -C $env:DEV_CONTROL_HOME\dashboarr-judge\repo rev-parse HEAD     # bf3a060a35170ba789f73195e3defaa0703e93e9
git -C $env:DEV_CONTROL_HOME\dashboarr-judge\repo -c core.longpaths=true status --porcelain     # prints nothing
Copy-Item $env:DEV_INSTINCTS_HOME\reviews\dashboarr\2026-11-07-bf3a060-control\claims.md $env:DEV_CONTROL_HOME\dashboarr-judge\claims.md    # the claims, public as written: no security claim, so no private file (section 13, step 6)
Get-ChildItem $HOME\.claude\agents                                             # lists nothing: still parked
$slug = (Join-Path $env:DEV_CONTROL_HOME dashboarr-judge) -replace '[^A-Za-z0-9]', '-'    # the session folder's name in Claude Code (section 6)
Test-Path $HOME\.claude\projects\$slug                                         # False
}
```

## Window 2: step 2, the session

```powershell
# 2. Open the session, in a new PowerShell window
if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {
Set-Location $env:DEV_CONTROL_HOME\dashboarr-judge
"/export $PWD\transcript.txt"                                                  # prints the /export line to type at the end of the session
Get-Content $env:DEV_INSTINCTS_HOME\reviews\dashboarr\2026-11-07-bf3a060-control\prompts\judge-1.txt -Raw -Encoding UTF8 | Set-Clipboard   # the prompt onto the clipboard: paste it as the first message, copying nothing else first
Remove-Item Env:DEV_INSTINCTS_HOME, Env:DEV_CONTROL_HOME
Test-Path Env:DEV_INSTINCTS_HOME, Env:DEV_CONTROL_HOME                         # False, False
$env:CLAUDE_CODE_DISABLE_CLAUDE_MDS = "1"
$env:CLAUDE_CODE_DISABLE_AUTO_MEMORY = "1"
claude --safe-mode --strict-mcp-config --model claude-fable-5-1 --effort high --permission-mode auto --tools "Read,Grep,Glob,Bash,Write,Edit" --disallowedTools "Bash(npm:*),Bash(npx:*),Bash(pnpm:*),Bash(yarn:*)"
}
```

## Window 3: step 3, after the session

```powershell
# 3. After the session, in another PowerShell window (step 2's has the variables removed)
if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {
$slug = (Join-Path $env:DEV_CONTROL_HOME dashboarr-judge) -replace '[^A-Za-z0-9]', '-'
Copy-Item $HOME\.claude\projects\$slug\*.jsonl $env:DEV_CONTROL_HOME\dashboarr-judge\    # first: the kept transcript (section 13.1)
git -C $env:DEV_CONTROL_HOME\dashboarr-judge\repo -c core.longpaths=true status --porcelain --ignored    # prints nothing: nothing written, installed or built in the clone
$t = (Get-ChildItem $HOME\.claude\projects\$slug\*.jsonl).FullName
python -I $env:DEV_INSTINCTS_HOME\tools\control.py session $t --clone $env:DEV_CONTROL_HOME\dashboarr-judge\repo --report $env:DEV_CONTROL_HOME\dashboarr-judge\verdicts.md --leak --term dev-control/dashboarr/ --term dev-control/dashboarr-2/ --prompt $env:DEV_INSTINCTS_HOME\reviews\dashboarr\2026-11-07-bf3a060-control\prompts\judge-1.txt
}
```

## Runs 2 and 3

Run 2 is the three windows above with `dashboarr-judge-2` in place of `dashboarr-judge` in every folder path (so in `$slug` too), the same `claims.md`, and `prompts\judge-2.txt`, `judge-1.txt` byte for byte, in window 2's clipboard line and window 3's `--prompt`; run 1's files are in Dev Instincts first and Garrett deletes its folder before run 2 opens; window 3's check adds `--term dev-control/dashboarr-judge/`, run 1's folder (section 10.1). Run 3, only if the two disagree on a claim, is the same again with `dashboarr-judge-3`, `claims-3.md` copied in under the name `claims.md`, `prompts\judge-3.txt`, and `--term dev-control/dashboarr-judge-2/` added (section 10.1). The prompt file's path under `reviews\` keeps `dashboarr` in every run.

## Window 4: the agents' return

After the judge's last run: `arm-b-windows.md`'s window 4, word for word (section 7, step 5).
