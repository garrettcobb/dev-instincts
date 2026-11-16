// Copies of functions at bf3a060 (store/config-store.ts), with a plain-object
// stand-in for store/storage.ts setJSON/getJSON (cache + write-through; no control flow):
//  - 2731-2740 enableDemoMode: strip attachedInstances in memory; 2749 serviceInstances = demo list
//  - 2354-2368 addWidget: maps state.dashboards, setJSON(dashboards, whole array)
//  - 2099-2107 renameDashboard
//  - 1640-1649 updateInstance: setJSON(services.<id>, next)
//  - 1195-1204 hydrate: attachedInstances copied only when it is an array; 959-963 services read
const storage = {};
const setJSON = (k, v) => { storage[k] = JSON.stringify(v); };
const getJSON = (k) => (storage[k] ? JSON.parse(storage[k]) : undefined);
let state = {
  dashboards: [
    { id: "home", name: "Home", widgets: [{ id: "s1", widgetId: "calendar" }], attachedInstances: ["radarr-home"] },
    { id: "cabin", name: "Cabin", widgets: [], attachedInstances: ["radarr-cabin"] },
  ],
  activeDashboardId: "home",
  serviceInstances: { radarr: [{ id: "radarr-home", enabled: true, name: "Radarr Home", localUrl: "http://10.0.0.5:7878", remoteUrl: "", useRemote: false }] },
};
setJSON("app.dashboards", state.dashboards);
setJSON("services.radarr", state.serviceInstances.radarr);
function enableDemoMode() {
  const demoInstances = { radarr: [{ id: "uuid-1", enabled: true, name: "Radarr", localUrl: "http://demo.local", remoteUrl: "", useRemote: false }] };
  const demoDashboards = state.dashboards.map((d) => {
    if (d.attachedInstances === undefined) return d;
    const next = { ...d };
    delete next.attachedInstances;
    return next;
  });
  state = { ...state, demoMode: true, serviceInstances: demoInstances, dashboards: demoDashboards };
}
function addWidget(widgetId) {
  const slot = { id: "s2", widgetId };
  let added = false;
  const dashboards = state.dashboards.map((d) => {
    if (d.id !== state.activeDashboardId) return d;
    added = true;
    return { ...d, widgets: [...d.widgets, slot] };
  });
  if (!added) return;
  setJSON("app.dashboards", dashboards);
  state = { ...state, dashboards };
}
function renameDashboard(id, name) {
  const dashboards = state.dashboards.map((d) => (d.id === id ? { ...d, name: name.trim() || d.name } : d));
  setJSON("app.dashboards", dashboards);
  state = { ...state, dashboards };
}
function updateInstance(id, instanceId, patch) {
  const list = state.serviceInstances[id] ?? [];
  const idx = list.findIndex((i) => i.id === instanceId);
  if (idx === -1) return;
  const prev = list[idx];
  const next = [...list];
  next[idx] = { ...prev, ...patch, id: prev.id };
  setJSON("services." + id, next);
  state = { ...state, serviceInstances: { ...state.serviceInstances, [id]: next } };
}
function hydrateAttached() {
  return getJSON("app.dashboards").map((d) => {
    const dashboard = { id: d.id, name: d.name };
    if (Array.isArray(d.attachedInstances)) dashboard.attachedInstances = [...d.attachedInstances];
    return dashboard;
  });
}
const show = () => console.log(
  "  storage dashboards:", JSON.stringify(hydrateAttached().map((d) => [d.name, d.attachedInstances ?? null])),
  "| storage services.radarr:", JSON.stringify(getJSON("services.radarr").map((i) => i.id + "@" + i.localUrl + " useRemote=" + i.useRemote)),
);
console.log("before demo:"); show();
enableDemoMode(); console.log("demo on, nothing edited:"); show();
console.log("HT: renameDashboard('cabin','Cabin 2') while demo on:"); renameDashboard("cabin", "Cabin 2"); show();
console.log("QT: addWidget('downloads') while demo on:"); addWidget("downloads"); show();
console.log("LQ: updateInstance('radarr','uuid-1',{useRemote:true}) while demo on:"); updateInstance("radarr", "uuid-1", { useRemote: true }); show();
console.log("(disableDemoMode -> hydrate reads exactly the storage rows above)");
