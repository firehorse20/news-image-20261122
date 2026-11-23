// "The World Today — 22 November 2026" (Node 22, standard library only):
// the entry is the entry.png beside this file, a 1024x1024 front page summing
// up the world news of Sunday 22 November 2026, rendered from HTML/CSS in
// headless Chromium. The program copies it to /output/entry.png, the whole
// file the judge sees.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);

if (!existsSync(src)) {
  throw new Error('entry.png is missing next to main.ts');
}

mkdirSync(out, { recursive: true });
const dest = join(out, 'entry.png');
copyFileSync(src, dest);

// A truncated or empty copy would hand the judge a broken image: refuse it
// here instead of silently passing the gate with a bad file.
if (statSync(dest).size === 0 || statSync(dest).size !== statSync(src).size) {
  throw new Error('entry.png was not copied whole to the output directory');
}
