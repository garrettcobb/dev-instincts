# Claims

Each claim has a code. The order is random.

## JW: The Downloads widget's poster cache grows forever in one storage row, and storage writes are never checked, so a long-lived install can stop loading its settings on Android

Severity: crash
Where: hooks/use-torrent-poster-map.ts:22, hooks/use-torrent-poster-map.ts:89, hooks/use-torrent-poster-map.ts:113, store/storage.ts:7, store/storage.ts:21, store/storage.ts:70, at bf3a060
What the user loses: the app's start. The hash-to-poster cache adds every download id seen in the queue or the latest 50 history rows and never evicts, persisting the whole map as one value (about 300 bytes per entry). On Android a single value past the 2 MB cursor window makes the read of all keys at start fail, which is how every setting is loaded; and because every write is fire-and-forget with no error handling, a store that has hit its size limit makes later saves fail silently.
Steps:
1. Keep the Downloads widget on a dashboard on Android, with Radarr or Sonarr grabbing many releases over a long period (on the order of seven thousand distinct downloads).
2. Relaunch the app.
Expected: the cache is capped or evicted; a failed storage write is reported.
Actual: by the code, the start-up read throws once the row is too large, and failed writes are dropped without a message. The size was not measured in a running app.
Evidence: reading
