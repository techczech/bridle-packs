import { mkdir, readdir, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { basename, join } from "node:path";
import { importBridleCore, importBridlePacks, resolveBridleRoot } from "./bridle-runtime.ts";

const PACK_RELATIVE = join("packs", "academic-pdf-to-mkd");
const SCRIPT_ID = "extract-docling";
const ASSET_ID = "docling-models";
const MAX_DOCLING_BYTES = 1_000_000_000;

export interface EvidenceArgs {
  input?: string;
  output?: string;
  dryRun: boolean;
  allowDownload: boolean;
}

export interface EvidencePaths {
  inputPdf: string;
  outputDir: string;
  paperId: string;
  dryRun: boolean;
  allowDownload: boolean;
}

export { resolveBridleRoot };

export function paperIdFromPdf(path: string): string {
  const stem = basename(path).replace(/\.pdf$/i, "").toLowerCase().replace(/\s+/g, "-");
  return stem.replace(/[^a-z0-9_-]/g, "").replace(/-+/g, "-").replace(/^-|-$/g, "") || "paper";
}

export function parseEvidenceArgs(argv: string[]): EvidenceArgs {
  const args: EvidenceArgs = { dryRun: false, allowDownload: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]!;
    if (arg === "--input") args.input = argv[++i];
    else if (arg.startsWith("--input=")) args.input = arg.slice("--input=".length);
    else if (arg === "--output") args.output = argv[++i];
    else if (arg.startsWith("--output=")) args.output = arg.slice("--output=".length);
    else if (arg === "--dry-run") args.dryRun = true;
    else if (arg === "--allow-download") args.allowDownload = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!args.dryRun && !args.allowDownload) {
    throw new Error("Live evidence run requires --allow-download. Use --dry-run for a no-download plan.");
  }
  return args;
}

export function resolveEvidencePaths(repoRoot: string, args: EvidenceArgs): EvidencePaths {
  const inputPdf = args.input ?? "";
  if (!inputPdf) throw new Error("No input PDF found. Pass --input /path/to/paper.pdf.");
  const paperId = paperIdFromPdf(inputPdf);
  return {
    inputPdf,
    paperId,
    outputDir: args.output ?? join(repoRoot, PACK_RELATIVE, "golden", paperId),
    dryRun: args.dryRun,
    allowDownload: args.allowDownload,
  };
}

function toCorePack(pack: any): any {
  return {
    root: pack.root,
    name: pack.name,
    version: pack.version,
    scripts: pack.scripts.map((script) => ({
      id: script.id,
      entry: script.entry,
      runtime: script.runtime,
      argsSchema: script.argsSchema,
      tier: script.tier,
      requiredProbes: script.requiredProbes,
      requiredAssets: script.requiredAssets,
    })),
    probes: pack.probes,
    assets: pack.assets,
  };
}

async function defaultInputPdf(): Promise<string | undefined> {
  const skillExamples = "/Users/dominiklukes/gitrepos/05_skills/academic-pdf-to-mkd/examples";
  const downloads = join(homedir(), "Downloads");
  const searchDirs = [skillExamples, join(downloads, "50-Reading"), downloads];
  for (const dir of searchDirs) {
    if (!existsSync(dir)) continue;
    const found = await firstPdf(dir);
    if (found) return found;
  }
  return undefined;
}

async function firstPdf(dir: string): Promise<string | undefined> {
  const entries = await readdir(dir, { withFileTypes: true });
  for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
    const path = join(dir, entry.name);
    if (entry.isFile() && entry.name.toLowerCase().endsWith(".pdf") && !/invoice|1password|emergency/i.test(entry.name)) return path;
    if (entry.isDirectory()) {
      const nested = await firstPdf(path);
      if (nested) return nested;
    }
  }
  return undefined;
}

async function main(): Promise<void> {
  const repoRoot = new URL("..", import.meta.url).pathname;
  const bridleCore = await importBridleCore(repoRoot);
  const bridlePacks = await importBridlePacks(repoRoot);
  const args = parseEvidenceArgs(Bun.argv.slice(2));
  if (!args.input) args.input = await defaultInputPdf();
  const paths = resolveEvidencePaths(repoRoot, args);
  const pack = await bridlePacks.loadPack(join(repoRoot, PACK_RELATIVE));
  const corePack = toCorePack(pack);
  const probeResults = await bridleCore.runPackProbes(corePack);
  const availability = bridleCore.getPackScriptAvailability(corePack, probeResults);
  const card = bridleCore.getManagedAssetCard(corePack, ASSET_ID);
  if (card.sizeBytes > MAX_DOCLING_BYTES) {
    throw new Error(`Docling asset exceeds approved size: ${card.sizeBytes} > ${MAX_DOCLING_BYTES}`);
  }

  const plan = {
    pack: `${pack.name}@${pack.version}`,
    contentHash: pack.contentHash,
    inputPdf: paths.inputPdf,
    outputDir: paths.outputDir,
    paperId: paths.paperId,
    hfHome: process.env.HF_HOME || join(homedir(), ".cache", "huggingface"),
    doclingAsset: card,
    probes: probeResults,
    availability,
    dryRun: paths.dryRun,
  };

  if (paths.dryRun) {
    console.log(JSON.stringify(plan, null, 2));
    return;
  }

  const auditEvents: unknown[] = [];
  const ctx = {
    trigger: { id: "docling-evidence", source: "user" as const, trust: "interactive" as const },
    sessionId: `docling-evidence-${Date.now()}`,
    audit: (event: unknown) => { auditEvents.push(event); },
  };

  const downloadCap = bridleCore.createManagedAssetDownloadCapability({
    pack: corePack,
    assetId: ASSET_ID,
    maxBytes: MAX_DOCLING_BYTES,
  });
  const downloadResult = await downloadCap.execute({ consent: paths.allowDownload }, ctx);
  if (downloadResult.isError) throw new Error(downloadResult.text);

  await mkdir(paths.outputDir, { recursive: true });
  const scriptCap = bridleCore.createPackScriptCapability({ pack: corePack, scriptId: SCRIPT_ID });
  const runResult = await scriptCap.execute({
    input_pdf: paths.inputPdf,
    output_dir: paths.outputDir,
    paper_id: paths.paperId,
  }, ctx);
  if (runResult.isError) throw new Error(runResult.text);

  await writeFile(join(paths.outputDir, "bridle-evidence-audit.json"), JSON.stringify({ plan, auditEvents, downloadResult, runResult }, null, 2));
  console.log(JSON.stringify({ outputDir: paths.outputDir, audit: join(paths.outputDir, "bridle-evidence-audit.json") }, null, 2));
}

if (import.meta.main) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
  });
}
