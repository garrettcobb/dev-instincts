// Copies at bf3a060:
//  - lib/url-validation.ts:128-135 workspaceForcesRemote
//  - store/config-store.ts:700-712 repairOrphanedHomeNetworkSelection
//  - store/config-store.ts:1945-1953 removeHomeNetwork (list filter only; homeNetworksPatch 579-619 touches no dashboard)
//  - store/config-store.ts:1918-1927 addHomeNetwork (new id each time)
//  - store/config-store.ts:2636-2637 getActiveUrl step 2: forcesRemote -> return remote
function workspaceForcesRemote(dashboard, homeNetworks) {
  const ids = dashboard?.homeNetworkIds;
  if (!Array.isArray(ids)) return false;
  return !ids.some((id) => homeNetworks.some((n) => n.id === id));
}
function repairOrphanedHomeNetworkSelection(dashboards, homeNetworks) {
  const validIds = new Set(homeNetworks.map((n) => n.id));
  return dashboards.map((d) => {
    const ids = d.homeNetworkIds;
    if (!Array.isArray(ids) || ids.length === 0) return d;
    if (ids.some((id) => validIds.has(id))) return d;
    const { homeNetworkIds: _orphaned, ...rest } = d;
    return rest;
  });
}
let seq = 1;
const newId = () => "net-" + seq++;
let homeNetworks = [{ id: newId(), ssid: "Casa", bssid: "" }];
let dashboards = [{ id: "home", homeNetworkIds: [homeNetworks[0].id] }];
const urlOutcome = (fr) => (fr ? "getActiveUrl returns remote ('' when only a Local URL is set -> 'No URL configured')" : "local/remote by auto-switch");
const report = (label) => {
  const fr = workspaceForcesRemote(dashboards[0], homeNetworks);
  console.log(label, "networks=" + JSON.stringify(homeNetworks.map((n) => n.id + ":" + n.ssid)), "dash.homeNetworkIds=" + JSON.stringify(dashboards[0].homeNetworkIds), "forcesRemote=" + fr, "->", urlOutcome(fr));
};
report("1 before:");
homeNetworks = homeNetworks.filter((n) => n.id !== "net-1"); report("2 removed Casa:");
homeNetworks = [...homeNetworks, { id: newId(), ssid: "Casa", bssid: "" }]; report("3 re-added Casa:");
dashboards = repairOrphanedHomeNetworkSelection(dashboards, homeNetworks); report("4 after import-only repair:");
