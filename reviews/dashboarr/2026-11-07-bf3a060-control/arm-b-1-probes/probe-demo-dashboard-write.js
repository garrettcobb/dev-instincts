// Probe: any dashboard edit made while Demo Mode is on permanently drops every
// dashboard's attachment list (and any demo instance pin) from storage.
//
// Copied from repo at bf3a060, store/config-store.ts:
//   - enableDemoMode, the dashboards part: lines 2731-2756
//   - renameDashboard: lines 2099-2107
//   - hydrate, the attachedInstances read-back: lines 1195-1204 and the
//     "attachedInstances stays undefined" fallback at lines 1316-1320
// Transcribed from TypeScript to JavaScript. Stand-ins (control flow unchanged):
//   - zustand's `set(updater)` / `get()` -> a plain object + merge
//   - store/storage.ts setJSON/getJSON -> an in-memory Map standing in for AsyncStorage
//   - recomputeDerivedFromActive -> omitted; it only computes derived views
//     (activeInstance/services/secrets), which this probe does not read.

const STORAGE_KEYS = { dashboards: "app.dashboards" };
const asyncStorage = new Map();
function setJSON(key, value) { asyncStorage.set(key, JSON.stringify(value)); }
function getJSON(key) { const raw = asyncStorage.get(key); return raw ? JSON.parse(raw) : undefined; }

let state;
function set(updater) { state = { ...state, ...updater(state) }; }

// --- enableDemoMode (lines 2731-2756), dashboards part ---
function enableDemoMode() {
  set((state) => {
    // v22: force every dashboard into auto-attach mode in memory (not
    // persisted) so the resolver picks up the freshly-generated demo UUIDs.
    // The user's stored attachments come back on disableDemoMode → hydrate.
    const demoDashboards = state.dashboards.map((d) => {
      if (d.attachedInstances === undefined) return d;
      const next = { ...d };
      delete next.attachedInstances;
      return next;
    });
    return { demoMode: true, dashboards: demoDashboards };
  });
}

// --- renameDashboard (lines 2099-2107) ---
function renameDashboard(dashboardId, name) {
  set((state) => {
    const dashboards = state.dashboards.map((d) =>
      d.id === dashboardId ? { ...d, name: name.trim() || d.name } : d,
    );
    setJSON(STORAGE_KEYS.dashboards, dashboards);
    return { dashboards };
  });
}

// --- hydrate (lines 1195-1204, 1316-1320): how attachedInstances is read back ---
function hydrateDashboards() {
  const stored = getJSON(STORAGE_KEYS.dashboards);
  return stored.map((d) => {
    const dashboard = { id: d.id, name: d.name, widgets: d.widgets };
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
    // attachedInstances stays undefined on pre-v20 dashboards intentionally —
    // the render-time fallback treats absent as "all currently-known instances
    // attached" (lines 1316-1320).
    return dashboard;
  });
}

// --- Scenario: two curated workspaces, Home and Cabin, each attaching its own instances ---
const saved = [
  { id: "dash-home", name: "Home", widgets: [], attachedInstances: ["qbit-home", "radarr-home"] },
  { id: "dash-cabin", name: "Cabin", widgets: [], attachedInstances: ["qbit-cabin", "radarr-cabin"] },
];
setJSON(STORAGE_KEYS.dashboards, saved);
state = { demoMode: false, dashboards: hydrateDashboards() };
console.log("before demo:", JSON.stringify(state.dashboards.map((d) => [d.name, d.attachedInstances])));

enableDemoMode();
console.log("demo on, storage still intact:",
  JSON.stringify(hydrateDashboards().map((d) => [d.name, d.attachedInstances])));

// The user renames one dashboard while demo mode is on (any other dashboard
// setter — icon, color, add/move/remove widget, pin tabs — writes the same array).
renameDashboard("dash-home", "Home (renamed)");

// Demo mode off -> hydrate re-reads storage.
const afterDemo = hydrateDashboards();
console.log("after demo off:", JSON.stringify(afterDemo.map((d) => [d.name, d.attachedInstances])));
const lost = afterDemo.filter((d) => d.attachedInstances === undefined).map((d) => d.name);
console.log(`dashboards whose attachment list was lost: ${JSON.stringify(lost)} (undefined = every instance attached)`);
