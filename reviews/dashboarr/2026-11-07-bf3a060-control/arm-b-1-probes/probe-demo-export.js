// Probe: "Export settings" while Demo Mode is on writes a backup of the demo
// placeholders, not of the user's configuration.
//
// Copied from repo at bf3a060, store/config-store.ts:
//   - enableDemoMode, the instances part: lines 2716-2728 and 2749-2754
//   - buildExportPayload: lines 3088-3135 (fields not relevant to the point are kept as-is)
//   - exportConfig's use of it: line 2771 (`const payload = buildExportPayload();`)
// Compared with the two sibling paths that DO skip demo mode:
//   - services/backend-backup.ts line 79:   if (config.demoMode) return "skipped";
//   - services/backend-api.ts   line 275:   if (configState.demoMode) return;
// Transcribed from TypeScript to JavaScript. Stand-ins (control flow unchanged):
//   zustand store -> plain object; SERVICE_IDS reduced to two kinds;
//   defaultServiceConfig/generateInstanceId -> literal equivalents;
//   useBackendStore -> fixed values; CURRENT_CONFIG_VERSION -> 63.

const SERVICE_IDS = ["qbittorrent", "radarr"];
const SERVICE_DEFAULTS = { qbittorrent: { name: "qBittorrent" }, radarr: { name: "Radarr" } };
function defaultServiceConfig(id) {
  return { enabled: false, name: SERVICE_DEFAULTS[id].name, localUrl: "", remoteUrl: "", useRemote: false, ignoreCertErrors: false };
}
let counter = 0;
function generateInstanceId() { return `demo-uuid-${++counter}`; }

let state = {
  demoMode: false,
  serviceInstances: {
    qbittorrent: [{ id: "real-qb", enabled: true, name: "qBittorrent Home", localUrl: "http://192.168.1.10:8080", remoteUrl: "https://qb.example.net", useRemote: false }],
    radarr: [{ id: "real-radarr", enabled: true, name: "Radarr", localUrl: "http://192.168.1.10:7878", remoteUrl: "", useRemote: false }],
  },
  instanceSecrets: { "real-qb": { username: "admin", password: "hunter2" }, "real-radarr": { apiKey: "0123456789abcdef" } },
  autoSwitchNetwork: true, treatVpnAsHome: false, homeNetworks: [{ id: "n1", ssid: "HomeWiFi", bssid: "" }],
  servicesOrder: [], dashboards: [{ id: "d1", name: "Default", widgets: [] }], activeDashboardId: "d1",
  wolDevices: [], shortcuts: [], hapticsEnabled: true, globalCustomHeaders: {}, uiScale: 1, appTheme: "zinc", weekStart: "auto",
  notificationSettings: { enabled: true },
};
function set(updater) { state = { ...state, ...updater(state) }; }

// --- enableDemoMode (lines 2716-2728, 2749-2754), instances part ---
function enableDemoMode() {
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
  set((state) => ({
    demoMode: true,
    serviceInstances: demoInstances,
    instanceSecrets: {},
  }));
}

// --- buildExportPayload (lines 3088-3135) ---
function buildExportPayload() {
  const {
    serviceInstances, instanceSecrets, autoSwitchNetwork, treatVpnAsHome, homeNetworks, servicesOrder,
    dashboards, activeDashboardId, wolDevices, shortcuts, hapticsEnabled, globalCustomHeaders, uiScale,
    appTheme, weekStart, notificationSettings: notifSettings,
  } = state;
  const { url, sharedSecret, deviceId, ignoreCertErrors } = { url: null, sharedSecret: null, deviceId: null, ignoreCertErrors: false };
  return {
    version: 63,
    exportedAt: new Date(0).toISOString(),
    services: serviceInstances,
    secrets: instanceSecrets,
    autoSwitchNetwork, treatVpnAsHome, homeNetworks, servicesOrder, dashboards, activeDashboardId,
    backend: { url, sharedSecret, deviceId, ignoreCertErrors },
    notificationSettings: notifSettings,
    wolDevices, shortcuts, hapticsEnabled, globalCustomHeaders, uiScale, appTheme, weekStart,
  };
}

// --- exportConfig line 2771: no demoMode check before this call ---
enableDemoMode();
const payload = buildExportPayload();
console.log("demoMode:", state.demoMode);
console.log("exported services:", JSON.stringify(payload.services));
console.log("exported secrets: ", JSON.stringify(payload.secrets));
const realLeft = Object.values(payload.services).flat().filter((i) => i.id.startsWith("real-")).length;
console.log(`real instances in the backup file: ${realLeft}; real secrets in the backup file: ${Object.keys(payload.secrets).length}`);
