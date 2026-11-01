# Proving "offline" (not just claiming it)

Reading the code isn't proof. PrivateApp's code read clean. Running it with the network cut showed the launcher's health check going out through the system proxy (OFF-01).

## Linux, in a container or VM (what ran in the trial)

1. **A namespace with only loopback:** `unshare -n bash -c 'ip link set lo up; ...'`. It needs CAP_NET_ADMIN. Everything below runs inside it.
2. **A private database inside the namespace:** `initdb` into a temp folder, listen on 127.0.0.1 only, on a non-default port.
3. **The app as it ships:** debug off, static files served the way the installer serves them, and the real launcher's serve path where possible (`start_app.sh`, `serve_shim.py`).
4. **Record every connection attempt:** `strace -f -e trace=connect,sendto,bind -o log` on the app server and the database.
5. **Drive every module in a browser,** also inside the namespace. Log every request with `page.on('request')` and flag anything that isn't 127.0.0.1, localhost, `data:` or `blob:` (`drive.cjs`, `headers.cjs`).
6. **Restart both servers while still offline,** and compare row counts before and after.
7. **Summarize:** every `connect()` target, every browser host, and anything that failed for lack of network (`summarize.py`).
8. **Probe the proxy path:** set `HTTP_PROXY`/`HTTPS_PROXY` to a dead address and confirm nothing tries to use it (`proxy_probe.py`). `urllib.urlopen` follows system proxies even for 127.0.0.1. Use an opener with `ProxyHandler({})`.

**Trial result:** the only targets were 127.0.0.1 and Unix sockets. There were no DNS lookups, and all 259 browser requests went to 127.0.0.1. The one leak (OFF-01) only showed up because of the proxy probe.

## Static inventory (do it too, but it's not proof)
- **The code and built bundle:** grep for `http://`, `https://`, `ws://`, fetch, XHR, WebSocket, EventSource, sendBeacon, CDN hosts, and remote `@font-face`/`url()`.
- **PDF libraries:** remote worker, cMap or font URLs.
- **Settings:** email backend, logging handlers, allowed hosts.
- **The launcher:** bind address, ports, and the database's `listen_addresses` and `pg_hba`.
- **Dependencies:** telemetry or phone-home. Keep build-time downloads separate from runtime.
- **Every place data is written:** the database, uploads, logs, backups, browser storage, caches, temp files and exports. And what happens if the data folder sits under OneDrive.

## Windows, on the real PC (the part a container can't prove)

The full step-by-step came from a private verification report. In short:

1. Outbound firewall block rules for the app's `python.exe` and `postgres.exe` (`New-NetFirewallRule -Direction Outbound -Action Block -Program ...`). This needs IT/admin.
2. A full workflow walk while watching `Get-NetTCPConnection -OwningProcess <pid>`. **Expect** only 127.0.0.1.
3. Resource Monitor → Network tab, filtered to those processes. **Expect** no remote addresses.
4. Optionally `pktmon` or `netsh trace` for a packet capture. This needs admin.
5. Airplane mode or unplugged: the whole workflow, plus a restart. **Expect** everything to work.

## Things that leave the PC through the browser, not the app
Edge sync and history (page titles), enhanced spellcheck (typed text), SmartScreen download checks and cloud clipboard. These are policy settings for IT. Also turn off `spellcheck` on editors in the app.

## Related hardening
- `Cache-Control: no-store` on authenticated pages and downloads.
- A Content-Security-Policy with `default-src 'self'`.
- Least-privilege database user.
- `127.0.0.1`, not `localhost`, when the server is IPv4-only.
- Disable Kerberos/SSL negotiation for local PostgreSQL (`PGGSSENCMODE=disable`, `sslmode=disable`).
- Local rotating log file.
