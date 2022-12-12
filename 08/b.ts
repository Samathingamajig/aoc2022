import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")));
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

const getScore = (grid: [number, boolean][][], row: number, col: number): number => {
  let up = 0,
    down = 0,
    left = 0,
    right = 0;

  let nRow = row - 1;
  while (nRow >= 0 && grid[nRow][col][0] < grid[row][col][0]) {
    up++;
    nRow--;
  }
  if (nRow >= 0) up++;
  nRow = row + 1;
  while (nRow < grid.length && grid[nRow][col][0] < grid[row][col][0]) {
    down++;
    nRow++;
  }
  if (nRow < grid.length) down++;

  let nCol = col - 1;
  while (nCol >= 0 && grid[row][nCol][0] < grid[row][col][0]) {
    left++;
    nCol--;
  }
  if (nCol >= 0) left++;
  nCol = col + 1;
  while (nCol < grid[row].length && grid[row][nCol][0] < grid[row][col][0]) {
    right++;
    nCol++;
  }
  if (nCol < grid[row].length) right++;
  up = Math.max(1, up);
  down = Math.max(1, down);
  left = Math.max(1, left);
  right = Math.max(1, right);
  // console.log(grid[row][col], row, col, [up, down, left, right], up * down * left * right);
  return up * down * left * right;
};

const solution = (input: string) => {
  //
  const grid = input.split("\n").map((line) => line.split("").map((num) => [parseInt(num), false])) as [
    number,
    boolean,
  ][][];
  // console.log(grid);

  // getScore(grid, 3, 2);
  let bestScore = 0;
  for (let row = 1; row < grid.length - 1; row++) {
    for (let col = 1; col < grid[row].length - 1; col++) {
      const score = getScore(grid, row, col);

      if (score > bestScore) {
        bestScore = score;
      }
    }
  }
  console.log(bestScore);
};

// solution(test);
solution(input);
