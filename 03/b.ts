import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

const scores = input
  .split("\n")
  .reduce((acc, line, i) => {
    acc[Math.floor(i / 3)] = acc[Math.floor(i / 3)] || [];
    acc[Math.floor(i / 3)].push(line);
    return acc;
  }, [] as string[][])
  .map(([a, b, c]) => {
    console.log([a, b, c]);
    const setA = new Set(a);
    const setB = new Set(b);
    const setC = new Set(c);
    const intersection = new Set([...setA].filter((x) => setB.has(x) && setC.has(x)));
    return [...intersection.values()][0];
  })
  .map((x) => {
    if (x.charCodeAt(0) >= 65 && x.charCodeAt(0) <= 90) {
      return x.charCodeAt(0) - 64 + 26;
    } else {
      return x.charCodeAt(0) - 96;
    }
  })
  .reduce((a, b) => a + b, 0);

console.log(scores);
