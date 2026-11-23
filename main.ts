// news-image-20261123 entry (Node 22, standard library only).
// The entry image lives in this repository as entry.png; this program
// copies it to the output directory the grader provides, so the judge
// sees exactly the bytes in the repository. The copy is byte-identical
// on every run, so the program is deterministic.
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);

if (!existsSync(source)) {
  throw new Error("entry.png is missing from this repository");
}

copyFileSync(source, join(outDir, "entry.png"));
