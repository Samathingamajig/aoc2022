import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

const elves = input
  .split("\n\n")
  .map((e) => e.split("\n").map(Number))
  .map((nums) => nums.reduce((a, b) => a + b));
console.log(elves);
const max = Math.max(...elves);
const index = elves.indexOf(max);
// console.log(index + 1);
console.log(max);
