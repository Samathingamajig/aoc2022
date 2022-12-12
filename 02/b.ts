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
    if (b === 1) {
      // lose
      return 0 + (((a + 3 - 1 - 1) % 3) + 1);
    } else if (b === 2) {
      // tie
      return 3 + a;
    } else {
      // win
      return 6 + (((a + 3 + 1 - 1) % 3) + 1);
    }
  })
  .map((x) => console.log(x) || x)
  .reduce((a, b) => a + b, 0);

console.log(score);
