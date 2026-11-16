// Probe: deleting a home network that a workspace had selected pins that
// workspace to "always remote", silently and permanently; re-adding the same
// WiFi does not undo it, because the new entry gets a new id.
//
// Standalone, Node standard library only. Copies the control flow of
// RenzoBeux/Dashboarr at bf3a060, transcribed from TypeScript to plain JS:
//   store/config-store.ts:1918-1927   addHomeNetwork
//   store/config-store.ts:1945-1953   removeHomeNetwork (filters the global
//                                     list only; dashboards untouched)
//   store/config-store.ts:594         homeNetworksPatch: the storage write
//   lib/network.ts:77-88              resolveEffectiveHomeNetworks
//   lib/url-validation.ts:128-135     workspaceForcesRemote
//   store/config-store.ts:700-712     repairOrphanedHomeNetworkSelection,
//                                     the repair the IMPORT path applies and
//                                     the delete path does not
// Stand-ins: generateHomeNetworkId is a counter; normalizeBssid is identity;
// zustand set() mutates one state object; invalidateForHomeNetworkEdit and the
// away-flag re-check inside homeNetworksPatch are omitted (they do not touch
// dashboards). No network, no files.

"use strict";

let idCounter = 0;
const generateHomeNetworkId = () => `net-${++idCounter}`;
const normalizeBssid = (v) => v;
const persisted = {};
const setJSON = (key, value) => (persisted[key] = JSON.stringify(value));
const STORAGE_KEYS = { homeNetworks: "app.homeNetworks" };

const state = { homeNetworks: [], dashboards: [], activeDashboardId: "" };
const set = (fn) => Object.assign(state, fn(state));

// store/config-store.ts:594 (the part of homeNetworksPatch that persists)
function homeNetworksPatch(state, next) {
  setJSON(STORAGE_KEYS.homeNetworks, next);
  return { homeNetworks: next };
}
// store/config-store.ts:1918-1927
function addHomeNetwork(network) {
  const created = { id: generateHomeNetworkId(), ssid: network.ssid.trim(), bssid: normalizeBssid(network.bssid) };
  set((state) => homeNetworksPatch(state, [...state.homeNetworks, created]));
  return created;
}
// store/config-store.ts:1945-1953
function removeHomeNetwork(id) {
  set((state) => homeNetworksPatch(state, state.homeNetworks.filter((n) => n.id !== id)));
}
// lib/network.ts:77-88
function resolveEffectiveHomeNetworks(dashboards, activeDashboardId, globalHomeNetworks) {
  const active = dashboards.find((d) => d.id === activeDashboardId) ?? dashboards[0];
  const ids = active?.homeNetworkIds;
  if (ids === undefined) return globalHomeNetworks;
  const selected = new Set(ids);
  return globalHomeNetworks.filter((n) => selected.has(n.id));
}
// lib/url-validation.ts:128-135
function workspaceForcesRemote(dashboard, homeNetworks) {
  const ids = dashboard?.homeNetworkIds;
  if (!Array.isArray(ids)) return false;
  return !ids.some((id) => homeNetworks.some((n) => n.id === id));
}
// store/config-store.ts:700-712 (import path only)
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

const report = (label) => {
  const active = state.dashboards.find((d) => d.id === state.activeDashboardId);
  const effective = resolveEffectiveHomeNetworks(state.dashboards, state.activeDashboardId, state.homeNetworks).map((n) => n.ssid);
  console.log(`${label}`);
  console.log(`  saved networks: ${JSON.stringify(state.homeNetworks.map((n) => `${n.id}:${n.ssid}`))}`);
  console.log(`  workspace "${active.name}" homeNetworkIds=${JSON.stringify(active.homeNetworkIds)} -> effective home networks ${JSON.stringify(effective)}, forcesRemote=${workspaceForcesRemote(active, state.homeNetworks)}`);
};

// 1. One home network; the Home workspace selected exactly it (dashboard editor).
const home = addHomeNetwork({ ssid: "Casa", bssid: "" });
state.dashboards = [{ id: "dash-home", name: "Home", widgets: [], homeNetworkIds: [home.id] }];
state.activeDashboardId = "dash-home";
report("1. Before: Casa saved, Home workspace selects Casa");

// 2. Settings > Network > Home Networks: remove Casa ("Stop treating Casa as a home network?"), then add it again.
removeHomeNetwork(home.id);
report("2. After removing Casa");
addHomeNetwork({ ssid: "Casa", bssid: "" });
report("3. After adding Casa back");

// 4. The same dashboards through the import path's repair, for contrast.
const repaired = repairOrphanedHomeNetworkSelection(state.dashboards, state.homeNetworks);
console.log(`4. Same dashboards through repairOrphanedHomeNetworkSelection (import only): homeNetworkIds=${JSON.stringify(repaired[0].homeNetworkIds)}, forcesRemote=${workspaceForcesRemote(repaired[0], state.homeNetworks)}`);

const active = state.dashboards[0];
const forced = workspaceForcesRemote(active, state.homeNetworks);
console.log("\nExpected: after re-adding Casa the Home workspace is at home on Casa again (or at least uses all networks)");
console.log(`Actual:   Home workspace keeps the dead id ${JSON.stringify(active.homeNetworkIds)}, effective home networks [], forcesRemote=${forced}: every service in it uses its Remote URL on the home WiFi, for good`);
process.exitCode = forced ? 1 : 0;
