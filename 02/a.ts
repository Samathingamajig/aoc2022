import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

const map = {
  A: 1,
  B: 2,
  C: 3,
  X: 1,
  Y: 2,
  Z: 3,
} as const;

const rounds = input
  .split("\n")
  .map((line) => line.split(" "))
  // @ts-ignore
  .map(([a, b]) => [map[a], map[b]]);

const score = rounds
  .map(([a, b]) => {
    if (a === b) {
      return 3 + b;
    } else if (b - 1 === a) {
      return 6 + b;
    } else if (b == 1 && a == 3) {
      return 6 + b;
    } else {
      return b;
    }
  })
  .reduce((a, b) => a + b, 0);

console.log(score);
