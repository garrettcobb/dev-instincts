// Probe: a Wake-on-LAN device saved by the app can make its own backup unrestorable.
//
// Copied from repo at bf3a060:
//   - app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx lines 80-92
//     (handleSave: the `device` object literal, in particular the `port` expression)
//   - store/config-schema.ts lines 170-186 (coerceWolDevice)
//   - store/config-schema.ts lines 600-608 (the wolDevices loop of validateExportPayload)
// Transcribed from TypeScript to JavaScript; no other changes.

// --- wake-on-lan.tsx handleSave (lines 80-92), with form fields as parameters ---
function handleSave(name, mac, broadcastAddress, port) {
  if (!name.trim() || !mac.trim()) {
    return { error: "Name and MAC address are required" };
  }
  const device = {
    id: "wol-1",
    name: name.trim(),
    mac: mac.trim(),
    broadcastAddress: broadcastAddress.trim() || undefined,
    port: port.trim() ? Number(port.trim()) || 9 : undefined,
  };
  return { device };
}

// --- config-schema.ts isPlainObject (line 36) and coerceWolDevice (lines 170-186) ---
function isPlainObject(v) {
  return typeof v === "object" && v !== null && !Array.isArray(v);
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
    if (typeof v.port !== "number" || !Number.isInteger(v.port) || v.port < 1 || v.port > 65535) {
      return null;
    }
    out.port = v.port;
  }
  return out;
}

// --- validateExportPayload, wolDevices section (lines 600-608) ---
function validateWolDevices(rawWolDevices) {
  if (!Array.isArray(rawWolDevices)) throw new Error("Config wolDevices is invalid");
  const devices = [];
  for (const item of rawWolDevices) {
    const coerced = coerceWolDevice(item);
    if (!coerced) throw new Error("Config wolDevices entry is invalid");
    devices.push(coerced);
  }
  return devices;
}

// --- Scenario: the user types a port of 70000 (a typo for 7 or 9), a MAC pasted
//     with a vendor prefix comment, or a decimal, and taps Save. ---
const cases = [
  ["Media Server", "00:11:22:33:44:55", "", "70000"],
  ["Media Server", "00:11:22:33:44:55", "", "1.5"],
  ["Media Server", "00:11:22:33:44:55", "", "-7"],
  ["Media Server", "00:11:22:33:44:55 (Intel NIC, onboard)", "", "9"],
];
for (const [name, mac, bcast, port] of cases) {
  const saved = handleSave(name, mac, bcast, port);
  console.log(`typed port=${JSON.stringify(port)} mac=${JSON.stringify(mac)}`);
  console.log(`  app saves:   ${JSON.stringify(saved)}`);
  try {
    validateWolDevices([saved.device]);
    console.log("  import:      accepted");
  } catch (e) {
    console.log(`  import:      throws "${e.message}" (whole backup rejected)`);
  }
}
