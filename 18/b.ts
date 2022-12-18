import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")))).replace(/\n$/, "");
const input = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")))).replace(/\n$/, "");

const stringify = (x: number, y: number, z: number) => `${x},${y},${z}`;
const parse = (position: string) => position.split(",").map(Number) as [number, number, number];

const neighbors = (x: number, y: number, z: number) =>
  new Array(6)
    .fill(0)
    .map(
      (_, dir) =>
        [x, y, z].map((num, i) => num + (i % 3 === dir % 3 ? 1 : 0) * (dir % 2 === 0 ? 1 : -1)) as [
          number,
          number,
          number,
        ],
    );

const cubesTouching = (x: number, y: number, z: number, rocks: Set<string>) => {
  let score = 0;
  // console.log({ x, y, z });

  for (const [x2, y2, z2] of neighbors(x, y, z)) {
    // console.log({ x2, y2, z2 });
    if (rocks.has(stringify(x2, y2, z2))) score++;
  }
  return score;
};

const solution = (input: string) => {
  //
  const visited = new Set<string>();
  const cubes = new Set(input.split("\n"));

  let [minX, maxX, minY, maxY, minZ, maxZ] = [0, 0, 0, 0, 0, 0];
  for (const cube of cubes) {
    const [x, y, z] = parse(cube);
    minX = Math.min(x, minX);
    maxX = Math.max(x, maxX);
    minY = Math.min(y, minY);
    maxY = Math.max(y, maxY);
    minZ = Math.min(z, minZ);
    maxZ = Math.max(z, maxZ);
  }
  console.log([minX, maxX, minY, maxY, minZ, maxZ]);

  let score = 0;

  const [min, max] = [
    Math.min(minX, maxX, minY, maxY, minZ, maxZ) - 1,
    Math.max(minX, maxX, minY, maxY, minZ, maxZ) + 1,
  ];
  // const [min, max] = [-1, 7];

  const queue: string[] = [];
  queue.push(`-1,-1,-1`);

  while (queue.length) {
    const [x, y, z] = parse(queue.pop()!);
    // console.log(x, y, z);

    const unvisitedAirNeighbors = neighbors(x, y, z).filter(
      (v) => !cubes.has(stringify(...v)) && !visited.has(stringify(...v)) && v.every((n) => min <= n && n <= max),
    );
    score += cubesTouching(x, y, z, cubes);
    for (const n of unvisitedAirNeighbors) {
      visited.add(stringify(...n));
      queue.push(stringify(...n));
    }
  }

  console.log(score);
};

// solution(test);
solution(input);
