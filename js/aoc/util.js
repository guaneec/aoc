import fs from "fs";
import path from "path";

import { dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

export function getInput(year, day) {
  return fs.readFileSync(
    path.join(
      __dirname,
      `../../data/${year}/${day.toString().padStart(2, 0)}.input.txt`
    ),
    "utf8"
  );
}
