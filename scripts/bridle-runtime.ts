import { existsSync } from "node:fs";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

export function resolveBridleRoot(repoRoot: string, env: Record<string, string | undefined> = process.env): string {
  if (env.BRIDLE_ROOT?.trim()) return env.BRIDLE_ROOT;
  const sibling = join(repoRoot, "..", "bridle");
  if (existsSync(join(sibling, "packages", "packs", "src", "index.ts"))) return sibling;
  throw new Error("Set BRIDLE_ROOT to a Bridle checkout before running pack validation.");
}

export async function importBridlePacks(repoRoot: string): Promise<any> {
  const bridleRoot = resolveBridleRoot(repoRoot);
  return await import(pathToFileURL(join(bridleRoot, "packages", "packs", "src", "index.ts")).href);
}

export async function importBridleCore(repoRoot: string): Promise<any> {
  const bridleRoot = resolveBridleRoot(repoRoot);
  return await import(pathToFileURL(join(bridleRoot, "packages", "core", "src", "index.ts")).href);
}
