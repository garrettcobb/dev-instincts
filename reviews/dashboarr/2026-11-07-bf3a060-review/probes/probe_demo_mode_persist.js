// Probe: edits made while Demo Mode is on are persisted over the real
// configuration, so "Turn it off and everything comes back exactly as it was"
// (docs/guide.html:259-263) does not hold.
//
// Standalone, Node standard library only. Copies the control flow of
// RenzoBeux/Dashboarr at bf3a060, transcribed from TypeScript to plain JS:
//   store/storage.ts:17-24, 60-74        getString/setString/getJSON/setJSON
//                                        (cache + write-through; AsyncStorage
//                                        replaced by a Map)
//   store/config-store.ts:958-983        hydrate: read services.<kind> lists
//   store/config-store.ts:824-834        isServiceInstance
//   store/config-store.ts:1154-1157,     hydrate: read dashboards, keep
//                         1184-1185,     attachedInstances only when stored
//                         1195-1204
//   store/config-store.ts:1423-1448      hydrate: demo-mode swap (in memory)
//   store/config-store.ts:1641-1649      updateInstance persist
//   store/config-store.ts:2354-2368      addWidget persist
//   store/config-store.ts:2716-2756      enableDemoMode (demo instances built
//                                        in memory, attachedInstances deleted
//                                        in memory, demoMode flag persisted)
//   store/config-store.ts:2758-2762      disableDemoMode -> hydrate()
//   lib/config-defaults.ts:55-65         defaultServiceConfig
// Stand-ins: generateInstanceId is a counter; SERVICE_IDS is ["radarr"];
// zustand set() mutates one state object; the pieces of hydrate that do not
// touch these keys are omitted. No network, no files.

"use strict";

// --- store/storage.ts:17-24, 60-74, with AsyncStorage as a Map -------------
const AsyncStorage = new Map();
const cache = {};
function initStorage() {
  for (const [key, value] of AsyncStorage.entries()) cache[key] = value;
}
function setString(key, value) {
  cache[key] = value;
  AsyncStorage.set(key, value);
}
function getBoolean(key) {
  return cache[key] === "true";
}
function setBoolean(key, value) {
  cache[key] = String(value);
  AsyncStorage.set(key, String(value));
}
function deleteKey(key) {
  delete cache[key];
  AsyncStorage.delete(key);
}
function getJSON(key) {
  const raw = cache[key];
  if (!raw) return undefined;
  try {
    return JSON.parse(raw);
  } catch {
    return undefined;
  }
}
function setJSON(key, value) {
  const json = JSON.stringify(value);
  cache[key] = json;
  AsyncStorage.set(key, json);
}

// --- stand-ins ---------------------------------------------------------------
const STORAGE_KEYS = { services: "services", dashboards: "app.dashboards", demoMode: "app.demoMode" };
const SERVICE_IDS = ["radarr"];
let idCounter = 0;
const generateInstanceId = () => `uuid-${++idCounter}`;
const isPlainObject = (v) => typeof v === "object" && v !== null && !Array.isArray(v);
// lib/config-defaults.ts:55-65
function defaultServiceConfig(id) {
  return { enabled: false, name: "Radarr", localUrl: "", remoteUrl: "", useRemote: false, ignoreCertErrors: false };
}
// store/config-store.ts:824-834
function isServiceInstance(v) {
  if (!isPlainObject(v)) return false;
  return (
    typeof v.id === "string" &&
    typeof v.enabled === "boolean" &&
    typeof v.name === "string" &&
    typeof v.localUrl === "string" &&
    typeof v.remoteUrl === "string" &&
    typeof v.useRemote === "boolean"
  );
}

const state = { demoMode: false, serviceInstances: {}, dashboards: [], activeDashboardId: "" };
const set = (fn) => Object.assign(state, typeof fn === "function" ? fn(state) : fn);

// --- store/config-store.ts hydrate, the parts that read these keys ----------
function hydrate() {
  initStorage();
  // :958-983 (the legacy-singleton and fresh-install branches omitted: not hit here)
  const instances = {};
  for (const id of SERVICE_IDS) {
    const stored = getJSON(`${STORAGE_KEYS.services}.${id}`);
    let list = [];
    if (Array.isArray(stored)) {
      for (const entry of stored) {
        if (isServiceInstance(entry)) list.push(entry);
      }
    }
    instances[id] = list;
  }
  // :1154-1157, :1184-1185, :1195-1204
  const dashboards = [];
  const storedDashboards = getJSON(STORAGE_KEYS.dashboards);
  if (Array.isArray(storedDashboards)) {
    for (const d of storedDashboards) {
      if (!isPlainObject(d)) continue;
      const widgets = Array.isArray(d.widgets) ? d.widgets.slice() : [];
      if (typeof d.id === "string" && typeof d.name === "string") {
        const dashboard = { id: d.id, name: d.name, widgets };
        if (Array.isArray(d.attachedInstances)) {
          const seen = new Set();
          const attached = [];
          for (const id of d.attachedInstances) {
            if (typeof id !== "string" || id.length === 0) continue;
            if (seen.has(id)) continue;
            seen.add(id);
            attached.push(id);
          }
          dashboard.attachedInstances = attached;
        }
        dashboards.push(dashboard);
      }
    }
  }
  // :1423-1448
  const demoMode = getBoolean(STORAGE_KEYS.demoMode) ?? false;
  if (demoMode) {
    for (const id of SERVICE_IDS) {
      const demoInst = {
        id: generateInstanceId(),
        ...defaultServiceConfig(id),
        enabled: true,
        localUrl: "http://demo.local",
        remoteUrl: "",
      };
      instances[id] = [demoInst];
    }
    for (let i = 0; i < dashboards.length; i++) {
      if (dashboards[i].attachedInstances === undefined) continue;
      const next = { ...dashboards[i] };
      delete next.attachedInstances;
      dashboards[i] = next;
    }
  }
  set({ demoMode, serviceInstances: instances, dashboards, activeDashboardId: dashboards[0]?.id ?? "" });
}

// --- store/config-store.ts:2716-2756 enableDemoMode ---------------------------
function enableDemoMode() {
  setBoolean(STORAGE_KEYS.demoMode, true);
  const demoInstances = {};
  for (const id of SERVICE_IDS) {
    const inst = {
      id: generateInstanceId(),
      ...defaultServiceConfig(id),
      enabled: true,
      localUrl: "http://demo.local",
      remoteUrl: "",
    };
    demoInstances[id] = [inst];
  }
  set((state) => {
    // v22: force every dashboard into auto-attach mode in memory (not
    // persisted) so the resolver picks up the freshly-generated demo UUIDs.
    const demoDashboards = state.dashboards.map((d) => {
      if (d.attachedInstances === undefined) return d;
      const next = { ...d };
      delete next.attachedInstances;
      return next;
    });
    return { demoMode: true, serviceInstances: demoInstances, dashboards: demoDashboards };
  });
}

// --- store/config-store.ts:2758-2762 disableDemoMode --------------------------
function disableDemoMode() {
  deleteKey(STORAGE_KEYS.demoMode);
  hydrate();
}

// --- store/config-store.ts:2354-2368 addWidget --------------------------------
function addWidget(widgetId) {
  const slot = { id: generateInstanceId(), widgetId };
  let added = false;
  set((state) => {
    const dashboards = state.dashboards.map((d) => {
      if (d.id !== state.activeDashboardId) return d;
      added = true;
      return { ...d, widgets: [...d.widgets, slot] };
    });
    if (!added) return state;
    setJSON(STORAGE_KEYS.dashboards, dashboards);
    return { dashboards };
  });
  return added ? slot : null;
}

// --- store/config-store.ts:1641-1649 updateInstance (the persisting part) ------
function updateInstance(id, instanceId, patch) {
  set((state) => {
    const list = state.serviceInstances[id] ?? [];
    const idx = list.findIndex((i) => i.id === instanceId);
    if (idx === -1) return state;
    const prev = list[idx];
    const next = [...list];
    next[idx] = { ...prev, ...patch, id: prev.id };
    const serviceInstances = { ...state.serviceInstances, [id]: next };
    setJSON(`${STORAGE_KEYS.services}.${id}`, next);
    return { serviceInstances };
  });
}

// --- store/config-store.ts:3088-3113 buildExportPayload (services + secrets) ---
// exportConfig (:2764-2801) serialises this with no demoMode check; the backend
// upload (services/backend-backup.ts:79) returns "skipped" in demo mode.
function buildExportPayload() {
  const { serviceInstances, instanceSecrets, dashboards } = state;
  return { version: 63, services: serviceInstances, secrets: instanceSecrets ?? {}, dashboards };
}

// --- scenario -----------------------------------------------------------------
const summary = (label) => {
  console.log(label);
  for (const d of state.dashboards) {
    console.log(`  dashboard ${d.id}: attachedInstances=${JSON.stringify(d.attachedInstances)} widgets=${d.widgets.length}`);
  }
  for (const inst of state.serviceInstances.radarr) {
    console.log(`  radarr instance: id=${inst.id} name=${JSON.stringify(inst.name)} localUrl=${inst.localUrl} useRemote=${inst.useRemote}`);
  }
};

// A real configuration, as the app would have persisted it.
AsyncStorage.set(
  "services.radarr",
  JSON.stringify([{ id: "radarr-home", enabled: true, name: "Radarr Home", localUrl: "http://10.0.0.5:7878", remoteUrl: "https://radarr.example.net", useRemote: false }]),
);
AsyncStorage.set(
  "app.dashboards",
  JSON.stringify([
    { id: "dash-home", name: "Home", widgets: [{ id: "slot-1", widgetId: "calendar" }], attachedInstances: ["radarr-home"] },
    { id: "dash-cabin", name: "Cabin", widgets: [], attachedInstances: ["radarr-cabin"] },
  ]),
);
hydrate();
summary("1. Real configuration after launch:");

console.log("\n2. Settings > Backup & Storage > Advanced > Demo Mode: on");
enableDemoMode();
summary("   In memory while Demo Mode is on:");

console.log("\n2b. While in Demo Mode: Settings > Backup & Storage > Export settings (same screen as the Demo Mode toggle)");
const exported = buildExportPayload();
console.log(`   exported services.radarr: ${JSON.stringify(exported.services.radarr)}`);
console.log(`   exported secrets: ${JSON.stringify(exported.secrets)}`);
console.log(`   exported dashboards attachedInstances: ${JSON.stringify(exported.dashboards.map((d) => d.attachedInstances))}`);

console.log("\n3. While in Demo Mode: add a widget to the active dashboard, and flip 'Use remote' on the (demo) Radarr");
addWidget("downloads");
updateInstance("radarr", state.serviceInstances.radarr[0].id, { useRemote: true });
console.log(`   persisted app.dashboards: ${AsyncStorage.get("app.dashboards")}`);
console.log(`   persisted services.radarr: ${AsyncStorage.get("services.radarr")}`);

console.log("\n4. Demo Mode: off (disableDemoMode -> hydrate)");
disableDemoMode();
summary("   Real configuration after Demo Mode is turned off:");

const home = state.dashboards.find((d) => d.id === "dash-home");
const cabin = state.dashboards.find((d) => d.id === "dash-cabin");
const radarr = state.serviceInstances.radarr[0];
console.log("\nExpected: Home attached ['radarr-home'], Cabin attached ['radarr-cabin'], radarr instance id 'radarr-home' at http://10.0.0.5:7878");
console.log(
  `Actual:   Home attached ${JSON.stringify(home.attachedInstances)}, Cabin attached ${JSON.stringify(cabin.attachedInstances)}, radarr instance id '${radarr.id}' at ${radarr.localUrl}`,
);
const lost = home.attachedInstances === undefined && cabin.attachedInstances === undefined && radarr.id !== "radarr-home";
console.log(lost ? "RESULT: real workspace attachments and the real Radarr connection were overwritten by Demo Mode edits" : "RESULT: no loss");
process.exitCode = lost ? 1 : 0;
