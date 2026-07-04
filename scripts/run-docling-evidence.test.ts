import { describe, expect, test } from "bun:test";
import { join } from "node:path";
import { parseEvidenceArgs, paperIdFromPdf, resolveEvidencePaths } from "./run-docling-evidence.ts";

describe("run-docling-evidence helpers", () => {
  test("derives stable paper ids from PDF names", () => {
    expect(paperIdFromPdf("/tmp/1986-rumelhart-pdp-v1.pdf")).toBe("1986-rumelhart-pdp-v1");
    expect(paperIdFromPdf("/tmp/Godel, Escher, Bach.pdf")).toBe("godel-escher-bach");
  });

  test("defaults output under the pack golden folder", () => {
    const repoRoot = "/repo";
    const args = parseEvidenceArgs(["--input", "/tmp/paper.pdf", "--dry-run"]);
    const paths = resolveEvidencePaths(repoRoot, args);

    expect(paths.inputPdf).toBe("/tmp/paper.pdf");
    expect(paths.outputDir).toBe(join(repoRoot, "packs", "academic-pdf-to-mkd", "golden", "paper"));
    expect(paths.allowDownload).toBe(false);
    expect(paths.dryRun).toBe(true);
  });

  test("requires explicit download consent unless dry-run is requested", () => {
    expect(() => parseEvidenceArgs(["--input", "/tmp/paper.pdf"])).toThrow("--allow-download");
    expect(parseEvidenceArgs(["--input", "/tmp/paper.pdf", "--allow-download"]).allowDownload).toBe(true);
  });
});
