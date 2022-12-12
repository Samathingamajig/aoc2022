import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
import { dirname } from "https://deno.land/std@0.165.0/path/win32.ts";
const test = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")))).replace(/\n$/, "");
const input = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")))).replace(/\n$/, "");

const solution = (input: string) => {
  //s
  const instructions: [string, number][] = input
    .split("\n")
    .map((line) => line.split(" "))
    .map(([dir, num]) => [dir, parseInt(num)]);

  const sumRs = instructions.reduce((acc, [dir, num]) => acc + (dir === "R" ? num : 0), 0);
  const sumUs = instructions.reduce((acc, [dir, num]) => acc + (dir === "U" ? num : 0), 0);

  const grid: number[][] = new Array(sumRs).fill(0).map(() => new Array(sumUs).fill(0));

  let hx = 0,
    hy = 0,
    tx = 0,
    ty = 0;

  const positions = new Set<`${number},${number}`>([`${tx},${ty}`]);

  for (const [dir, num] of instructions) {
    for (let _ = 0; _ < num; _++) {
      if (dir === "R") {
        hx++;
      } else if (dir === "U") {
        hy++;
      } else if (dir === "L") {
        hx--;
      } else if (dir === "D") {
        hy--;
      }
      const dx = hx - tx;
      const dy = hy - ty;
      //console.log([hx, hy, tx, ty, dx, dy], dir, _);
      if (Math.abs(dx) > 1 || Math.abs(dy) > 1) {
        //console.log("jump");
        tx += dx === 0 ? 0 : dx / Math.abs(dx);
        ty += dy === 0 ? 0 : dy / Math.abs(dy);
      }
      //console.log([tx, ty]);
      positions.add(`${tx},${ty}`);
      // grid[tx][ty] = 1;
      //console.log(grid);
    }
  }
  //console.log(grid);
  console.log(positions.size);
};

// solution(test);
solution(input);
