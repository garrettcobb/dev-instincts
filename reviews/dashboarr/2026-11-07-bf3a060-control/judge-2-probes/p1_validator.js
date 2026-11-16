// Copies of functions at bf3a060:
//  - store/config-schema.ts:41-49 isHttpUrlOrEmpty
//  - store/config-schema.ts:54-70 HEADER_NAME_RE, MAX_HEADERS_PER_SCOPE, coerceHeaderMap
//  - store/config-schema.ts:72-85 coerceServiceInstance (leading checks only; later optional fields omitted)
//  - store/config-schema.ts:172-188 coerceWolDevice
//  - store/config-schema.ts:613-620 wolDevices loop of validateExportPayload
//  - app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx:80-92 handleSave device construction
// Standard library only. Transcribed from TypeScript to JavaScript.
function isPlainObject(v) { return typeof v === "object" && v !== null && !Array.isArray(v); }
function isHttpUrlOrEmpty(v) {
  if (typeof v !== "string") return false;
  if (v === "") return true;
  try { const u = new URL(v); return u.protocol === "http:" || u.protocol === "https:"; } catch { return false; }
}
const HEADER_NAME_RE = /^[A-Za-z0-9!#$%&'*+\-.^_`|~]+$/;
const MAX_HEADERS_PER_SCOPE = 32;
function coerceHeaderMap(v) {
  if (!isPlainObject(v)) return null;
  const out = {}; let count = 0;
  for (const [key, value] of Object.entries(v)) {
    if (typeof key !== "string" || key.length === 0 || key.length > 200) return null;
    if (!HEADER_NAME_RE.test(key)) return null;
    if (typeof value !== "string" || value.length > 4096) return null;
    if (/[\r\n]/.test(value)) return null;
    out[key] = value;
    if (++count > MAX_HEADERS_PER_SCOPE) return null;
  }
  return out;
}
function coerceServiceInstanceHead(v) {
  if (!isPlainObject(v)) return null;
  if (typeof v.id !== "string" || v.id.length === 0 || v.id.length > 128) return null;
  if (typeof v.enabled !== "boolean") return null;
  if (typeof v.name !== "string" || v.name.length > 200) return null;
  if (!isHttpUrlOrEmpty(v.localUrl)) return null;
  if (!isHttpUrlOrEmpty(v.remoteUrl)) return null;
  if (typeof v.useRemote !== "boolean") return null;
  return { id: v.id, enabled: v.enabled, name: v.name, localUrl: v.localUrl, remoteUrl: v.remoteUrl, useRemote: v.useRemote };
}
function coerceWolDevice(v) {
  if (!isPlainObject(v)) return null;
  if (typeof v.id !== "string" || v.id.length === 0 || v.id.length > 128) return null;
  if (typeof v.name !== "string" || v.name.length > 200) return null;
  if (typeof v.mac !== "string" || v.mac.length > 32) return null;
  const out = { id: v.id, name: v.name, mac: v.mac };
  if (v.broadcastAddress !== undefined) {
    if (typeof v.broadcastAddress !== "string" || v.broadcastAddress.length > 45) return null;
    out.broadcastAddress = v.broadcastAddress;
  }
  if (v.port !== undefined) {
    if (typeof v.port !== "number" || !Number.isInteger(v.port) || v.port < 1 || v.port > 65535) { return null; }
    out.port = v.port;
  }
  return out;
}
function validateWol(rawWol) {
  const devices = [];
  for (const item of rawWol) {
    const c = coerceWolDevice(item);
    if (!c) throw new Error("Config wolDevices entry is invalid");
    devices.push(c);
  }
  return devices;
}
// wake-on-lan.tsx:80-92
function handleSave(name, mac, broadcastAddress, port) {
  if (!name.trim() || !mac.trim()) return { error: "Name and MAC address are required" };
  return {
    id: "wol-1",
    name: name.trim(),
    mac: mac.trim(),
    broadcastAddress: broadcastAddress.trim() || undefined,
    port: port.trim() ? Number(port.trim()) || 9 : undefined,
  };
}
console.log("== XC/RW: WOL editor -> import validator");
const cases = [
  ["70000", "AA:BB:CC:DD:EE:FF"], ["9.5", "AA:BB:CC:DD:EE:FF"], ["-7", "AA:BB:CC:DD:EE:FF"],
  ["abc", "AA:BB:CC:DD:EE:FF"], ["9", "00:11:22:33:44:55 (Intel NIC, onboard)"], ["9", "AA:BB:CC:DD:EE:FF"],
];
for (const [port, mac] of cases) {
  const d = handleSave("NAS", mac, "", port);
  let r;
  try { validateWol([d]); r = "import accepted"; } catch (e) { r = "import throws: " + e.message; }
  console.log(" port=" + JSON.stringify(port) + " mac.len=" + mac.length + " -> saved " + JSON.stringify(d) + " -> " + r);
}
console.log("== TJ: isHttpUrlOrEmpty on scheme-less stored URLs");
for (const u of ["192.168.1.10:7878", "nas.local:7878", "localhost:7878", "http://192.168.1.10:7878", ""]) {
  console.log(" " + JSON.stringify(u) + " -> " + isHttpUrlOrEmpty(u));
}
console.log("== PQ: service name length and header map");
const base = { id: "a", enabled: true, localUrl: "http://h", remoteUrl: "", useRemote: false };
console.log(" name 200 chars ->", coerceServiceInstanceHead({ ...base, name: "x".repeat(200) }) ? "accepted" : "REJECTED");
console.log(" name 201 chars ->", coerceServiceInstanceHead({ ...base, name: "x".repeat(201) }) ? "accepted" : "REJECTED");
const h32 = {}, h33 = {};
for (let i = 0; i < 32; i++) h32["H" + i] = "v";
for (let i = 0; i < 33; i++) h33["H" + i] = "v";
console.log(" 32 headers ->", coerceHeaderMap(h32) ? "accepted" : "REJECTED", "| 33 headers ->", coerceHeaderMap(h33) ? "accepted" : "REJECTED");
console.log(" value 4096 ->", coerceHeaderMap({ A: "v".repeat(4096) }) ? "accepted" : "REJECTED", "| value 4097 ->", coerceHeaderMap({ A: "v".repeat(4097) }) ? "accepted" : "REJECTED");
