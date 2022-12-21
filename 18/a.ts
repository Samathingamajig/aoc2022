import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")))).replace(/\n$/, "");
const input = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")))).replace(/\n$/, "");

const solution = (input: string) => {
  //
  const seen = new Set<string>();
  let score = 0;
  for (const line of input.split("\n")) {
    const [x, y, z] = line.split(",").map(Number);
    seen.add(`${x},${y},${z}`);
    // console.log({ x, y, z });
    for (let dir = 0; dir < 6; dir++) {
      const [x2, y2, z2] = [x, y, z].map((num, i) => num + (i % 3 === dir % 3 ? 1 : 0) * (dir % 2 === 0 ? 1 : -1));
      // console.log({ x2, y2, z2 });
      if (seen.has(`${x2},${y2},${z2}`)) score--;
      else score++;
    }
  }
  console.log(score);
};

// solution(test);
solution(input);
