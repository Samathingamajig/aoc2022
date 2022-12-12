import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")));
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

const solution = (input: string) => {
  //
  const grid = input.split("\n").map((line) => line.split("").map((num) => [parseInt(num), false])) as [
    number,
    boolean,
  ][][];
  console.log(grid);
  for (let row = 0; row < grid.length; row++) {
    let colMax = -1;
    for (let col = 0; col < grid[row].length; col++) {
      if (colMax < grid[row][col][0]) {
        grid[row][col][1] = true;
      }
      colMax = Math.max(colMax, grid[row][col][0]);
    }
    colMax = -1;
    for (let col = grid[row].length - 1; col >= 0; col--) {
      if (colMax < grid[row][col][0]) {
        grid[row][col][1] = true;
      }
      colMax = Math.max(colMax, grid[row][col][0]);
    }
  }
  console.log(grid);
  for (let col = 0; col < grid[0].length; col++) {
    let rowMax = -1;
    for (let row = 0; row < grid.length; row++) {
      if (rowMax < grid[row][col][0]) {
        grid[row][col][1] = true;
      }
      rowMax = Math.max(rowMax, grid[row][col][0]);
    }
    rowMax = -1;
    for (let row = grid.length - 1; row >= 0; row--) {
      if (rowMax < grid[row][col][0]) {
        grid[row][col][1] = true;
      }
      rowMax = Math.max(rowMax, grid[row][col][0]);
    }
  }
  const count = grid.reduce((acc, row) => {
    return acc + row.filter((col) => col[1]).length;
  }, 0);
  console.log(grid);
  console.log(count);
};

// solution(test);
solution(input);
