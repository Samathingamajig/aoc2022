import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

const rows = input.split("\n");
const firstNumberLineIndex = rows.findIndex((row) => /\d/.test(row));

const numColumns = rows[firstNumberLineIndex].trim().split(/\s+/).length;
console.log(numColumns);

const grid = rows.slice(0, firstNumberLineIndex).map((row) => {
  const boxes = [];
  for (let i = 0; i < numColumns; i++) {
    boxes.push(row.slice(1 + i * 4, 1 + i * 4 + 3));
  }
  return boxes.map((box) => box.replace(/\[|\]|\s/g, ""));
});
const newGrid = grid
  .reduce((newGrid, row, rowIndex) => {
    // flip rows and cols
    row.forEach((num, colIndex) => {
      newGrid[colIndex] = newGrid[colIndex] || [];
      newGrid[colIndex][rowIndex] = num;
    });
    return newGrid;
  }, [] as string[][])
  .map((column) => column.reverse().filter((val) => val));

const instructions = rows.slice(firstNumberLineIndex + 2).map((row) => row.match(/\d+/g)!.map((s) => parseInt(s)));

for (const [move, from, to] of instructions) {
  for (let i = 0; i < move; i++) {
    console.log(move, from, to, i, newGrid);
    const top = newGrid[from - 1].pop();
    if (top != null) newGrid[to - 1].push(top);
  }
}

console.log(newGrid);

const tops = newGrid.map((column) => column[column.length - 1]);

console.log(tops.join(""));
