import { readdir } from "node:fs/promises";
import { join } from "node:path";
import { loadPack } from "@bridle/packs";

const root = new URL("..", import.meta.url).pathname;
const packsDir = join(root, "packs");
const entries = await readdir(packsDir, { withFileTypes: true });

let failures = 0;
for (const entry of entries) {
  if (!entry.isDirectory()) continue;
  const packRoot = join(packsDir, entry.name);
  try {
    const pack = await loadPack(packRoot);
    console.log(`${pack.name}@${pack.version} ${pack.contentHash}`);
  } catch (error) {
    failures += 1;
    console.error(`${entry.name}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

if (failures > 0) process.exit(1);
