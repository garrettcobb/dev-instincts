// Probe: a Wake-on-LAN device the editor accepts makes every later config
// export unrestorable: the import validator rejects the whole file.
//
// Standalone, Node standard library only. Copies the control flow of
// RenzoBeux/Dashboarr at bf3a060, transcribed from TypeScript to plain JS:
//   app/(tabs)/(dashboard,services,settings)/wake-on-lan.tsx:80-92
//       handleSave: the only checks are "name and MAC non-empty"; the port
//       field becomes `Number(port.trim()) || 9`
//   store/config-schema.ts:37-39     isPlainObject
//   store/config-schema.ts:172-189   coerceWolDevice
//   store/config-schema.ts:613-622   validateExportPayload, the wolDevices loop
// Stand-ins: generateId is a constant; setWolDevices stores into an array;
// the export file is the payload object itself (exportConfig at
// store/config-store.ts:2764-2801 serialises buildExportPayload() without
// running validateExportPayload; the backend backup upload, services/
// backend-backup.ts:40-51, does the same). No network, no files.

"use strict";

// --- store/config-schema.ts:37-39 -------------------------------------------
function isPlainObject(v) {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

// --- store/config-schema.ts:172-189 -----------------------------------------
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

// --- store/config-schema.ts:613-622 (inside validateExportPayload) -----------
function validateWolDevices(raw) {
  const payload = {};
  if (raw.wolDevices !== undefined && raw.wolDevices !== null) {
    if (!Array.isArray(raw.wolDevices)) throw new Error("Config wolDevices is invalid");
    const devices = [];
    for (const item of raw.wolDevices) {
      const coerced = coerceWolDevice(item);
      if (!coerced) throw new Error("Config wolDevices entry is invalid");
      devices.push(coerced);
    }
    payload.wolDevices = devices;
  }
  return payload;
}

// --- wake-on-lan.tsx:80-92 handleSave, with the form fields as arguments -----
function handleSave(wolDevices, { name, mac, broadcastAddress, port }, toast) {
  if (!name.trim() || !mac.trim()) {
    toast("Name and MAC address are required", "error");
    return wolDevices;
  }
  const device = {
    id: "wol-1",
    name: name.trim(),
    mac: mac.trim(),
    broadcastAddress: broadcastAddress.trim() || undefined,
    port: port.trim() ? Number(port.trim()) || 9 : undefined,
  };
  toast(`${device.name} added`, "success");
  return [...wolDevices, device];
}

// --- scenario ---------------------------------------------------------------
const cases = [
  { label: "port typed as 70000", form: { name: "NAS", mac: "AA:BB:CC:DD:EE:FF", broadcastAddress: "", port: "70000" } },
  { label: "port typed as 9.5", form: { name: "NAS", mac: "AA:BB:CC:DD:EE:FF", broadcastAddress: "", port: "9.5" } },
  { label: "port typed as -7", form: { name: "NAS", mac: "AA:BB:CC:DD:EE:FF", broadcastAddress: "", port: "-7" } },
  { label: "broadcast address 46 chars", form: { name: "NAS", mac: "AA:BB:CC:DD:EE:FF", broadcastAddress: "a".repeat(46), port: "" } },
  { label: "valid device (control)", form: { name: "NAS", mac: "AA:BB:CC:DD:EE:FF", broadcastAddress: "10.0.0.255", port: "9" } },
];

let failures = 0;
for (const c of cases) {
  let toasted = "";
  const saved = handleSave([], c.form, (msg, kind) => (toasted = `${kind}: ${msg}`));
  const exportPayload = { wolDevices: saved }; // what buildExportPayload would carry, unvalidated
  let importOutcome;
  try {
    validateWolDevices(exportPayload);
    importOutcome = "import accepted";
  } catch (e) {
    importOutcome = `import REJECTED: ${e.message}`;
    if (c.label !== "valid device (control)") failures++;
  }
  console.log(`${c.label}`);
  console.log(`  editor: ${toasted}; stored device = ${JSON.stringify(saved[0])}`);
  console.log(`  later restore of the export: ${importOutcome}`);
}
console.log("\nExpected: a device the editor saved with a success toast restores with the rest of the config");
console.log(`Actual:   ${failures} of ${cases.length - 1} editor-accepted devices make the whole import throw`);
process.exitCode = failures > 0 ? 1 : 0;
