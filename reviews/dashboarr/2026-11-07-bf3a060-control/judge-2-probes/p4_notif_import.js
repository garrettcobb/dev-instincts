// Copies at bf3a060 (store/config-store.ts) with a plain-object storage stand-in:
//  - 2987-2992 importConfigFromPayload notification branch; 3067 set({notificationSettings})
//  - 1415-1421 hydrate notification read
const storage = {};
const setJSON = (k, v) => { storage[k] = JSON.stringify(v); };
const getJSON = (k) => (storage[k] ? JSON.parse(storage[k]) : undefined);
const DEFAULT_NOTIFICATION_SETTINGS = { enabled: true };
const KEY = "app.notificationSettings";
setJSON(KEY, { enabled: false }); // the phone had notifications off
let memory = { notificationSettings: { enabled: false } };
function importBranch(payload) {
  const imported = payload.notificationSettings
    ? { ...DEFAULT_NOTIFICATION_SETTINGS, ...payload.notificationSettings }
    : DEFAULT_NOTIFICATION_SETTINGS;
  if (payload.notificationSettings) { setJSON(KEY, imported); }
  memory = { notificationSettings: imported };
}
function hydrateRead() {
  const stored = getJSON(KEY);
  return { ...DEFAULT_NOTIFICATION_SETTINGS, ...(stored ?? {}) };
}
importBranch({ version: 99, services: {} }); // a backup with no notificationSettings
console.log("after import, in memory:", JSON.stringify(memory.notificationSettings), "| storage key:", storage[KEY]);
console.log("after relaunch (hydrate):", JSON.stringify(hydrateRead()));
