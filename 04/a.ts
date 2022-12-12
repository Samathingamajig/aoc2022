import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

const lines = input.split("\n");
const overlaps = lines.reduce((acc, line) => {
  const [left, right] = line.split(",");
  const [l1, l2] = left.split("-").map(Number);
  const [r1, r2] = right.split("-").map(Number);
  if (l1 >= r1 && l2 <= r2) {
    acc++;
  } else if (r1 >= l1 && r2 <= l2) {
    acc++;
  }
  return acc;
}, 0);
console.log(overlaps);
