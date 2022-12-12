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

  const positions = new Array(10).fill(0).map(() => [0, 0]);

  const visitedPositions = new Set<`${number},${number}`>([`${0},${0}`]);

  for (const [dir, num] of instructions) {
    for (let _ = 0; _ < num; _++) {
      if (dir === "R") {
        positions[0][0]++;
      } else if (dir === "U") {
        positions[0][1]++;
      } else if (dir === "L") {
        positions[0][0]--;
      } else if (dir === "D") {
        positions[0][1]--;
      }
      for (let i = 1; i < positions.length; i++) {
        const dx = positions[i - 1][0] - positions[i][0];
        const dy = positions[i - 1][1] - positions[i][1];
        //console.log([hx, hy, tx, ty, dx, dy], dir, _);
        if (Math.abs(dx) > 1 || Math.abs(dy) > 1) {
          //console.log("jump");
          positions[i][0] += dx === 0 ? 0 : dx / Math.abs(dx);
          positions[i][1] += dy === 0 ? 0 : dy / Math.abs(dy);
        }
      }

      //console.log([tx, ty]);
      visitedPositions.add(`${positions[9][0]},${positions[9][1]}`);
      // grid[tx][ty] = 1;
      //console.log(grid);
    }
  }
  //console.log(grid);
  console.log(visitedPositions.size);
};

solution(test);
solution(input);
