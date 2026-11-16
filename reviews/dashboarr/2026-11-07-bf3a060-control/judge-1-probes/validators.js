// Transcribed from repo at bf3a060 (TypeScript -> JavaScript, no behavior change):
//   store/config-schema.ts:41-50   isHttpUrlOrEmpty
//   store/config-schema.ts:54-67   HEADER_NAME_RE, MAX_HEADERS_PER_SCOPE, coerceHeaderMap
//   store/config-schema.ts:76      coerceServiceInstance name-length check (only that line)
//   store/config-schema.ts:172-186 coerceWolDevice
//   app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx:80-92 handleSave device construction
//   lib/url-validation.ts:54-59    normalizeServiceUrl
// Stand-ins: isPlainObject copied from config-schema.ts:37-39; generateId replaced by a constant.

function isPlainObject(v) { return typeof v === "object" && v !== null && !Array.isArray(v); }

function isHttpUrlOrEmpty(v) {
  if (typeof v !== "string") return false;
  if (v === "") return true;
  try { const u = new URL(v); return u.protocol === "http:" || u.protocol === "https:"; }
  catch { return false; }
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
    if (typeof v.port !== "number" || !Number.isInteger(v.port) || v.port < 1 || v.port > 65535) return null;
    out.port = v.port;
  }
  return out;
}

// wake-on-lan.tsx:86-92 (editingId null -> generateId())
function wolHandleSaveDevice(name, mac, broadcastAddress, port) {
  return {
    id: "wol-1",
    name: name.trim(),
    mac: mac.trim(),
    broadcastAddress: broadcastAddress.trim() || undefined,
    port: port.trim() ? Number(port.trim()) || 9 : undefined,
  };
}

function normalizeServiceUrl(raw) {
  const trimmed = raw.trim();
  if (trimmed === "") return "";
  if (/^[a-z]+:\/\//i.test(trimmed)) return trimmed;
  return `http://${trimmed}`;
}

console.log("--- WoL: editor output -> import validator");
for (const [port, mac, bcast] of [["70000","AA:BB:CC:DD:EE:FF",""],["9.5","AA:BB:CC:DD:EE:FF",""],["-7","AA:BB:CC:DD:EE:FF",""],["9","00:11:22:33:44:55 (Intel NIC, onboard)",""],["9","AA:BB:CC:DD:EE:FF","a".repeat(46)],["abc","AA:BB:CC:DD:EE:FF",""],["9","AA:BB:CC:DD:EE:FF","10.0.0.255"]]) {
  const d = wolHandleSaveDevice("NAS", mac, bcast, port);
  console.log(JSON.stringify({port, macLen: mac.length, bcastLen: bcast.length}), "->", JSON.stringify(d.port), "import:", coerceWolDevice(d) ? "accepted" : "REJECTED");
}
console.log("--- service name > 200 (coerceServiceInstance line 76)");
console.log("201 chars rejected:", "x".repeat(201).length > 200);
console.log("--- header maps");
const h33 = {}; for (let i = 0; i < 33; i++) h33["X-H" + i] = "v";
console.log("33 headers:", coerceHeaderMap(h33) ? "accepted" : "REJECTED");
console.log("value 4097:", coerceHeaderMap({ "X-A": "v".repeat(4097) }) ? "accepted" : "REJECTED");
console.log("key 201:", coerceHeaderMap({ ["X".repeat(201)]: "v" }) ? "accepted" : "REJECTED");
console.log("--- URLs without scheme (TJ)");
for (const u of ["192.168.1.10:7878", "nas:7878", "localhost:7878", "http://192.168.1.10:7878"]) {
  let proto; try { proto = new URL(u).protocol; } catch (e) { proto = "throws"; }
  console.log(JSON.stringify(u), "URL.protocol:", proto, "isHttpUrlOrEmpty:", isHttpUrlOrEmpty(u), "normalized:", normalizeServiceUrl(u), "-> valid:", isHttpUrlOrEmpty(normalizeServiceUrl(u)));
}
