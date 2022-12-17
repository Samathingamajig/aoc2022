import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")))).replace(/\n$/, "");
const input = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")))).replace(/\n$/, "");

const MIN_X = 0;
const MAX_X = 7;

class Piece {
  public y: number;
  constructor(public x: number, highestY: number, public shape: [number, number][]) {
    this.y = highestY + 4 + Math.max(...shape.map(([_, y]) => y));
  }

  move(direction: string, board: Set<string>, verbose: boolean): number {
    if (verbose) {
      console.log(
        [
          [
            direction === "<",
            this.x > MIN_X,
            !this.shape.some(([x, y]) => board.has(`${this.x + x - 1},${this.y - y}`)),
          ],
          [
            direction === ">",
            this.x < MAX_X - 1,
            !this.shape.some(([x, y]) => board.has(`${this.x + x + 1},${this.y - y}`) || this.x + x >= MAX_X),
          ],
          [
            !this.shape.some(([x, y]) => board.has(`${this.x + x},${this.y - y - 1}`)),
            !this.shape.some(([_, y]) => this.y - y <= 0),
          ],
        ].map((a) => [a.map((b) => (b ? "T" : "F")).join(" "), a.reduce((acc, cur) => acc && cur, true) ? "T" : "F"]),
      );
    }
    if (
      direction === "<" &&
      this.x - 1 >= MIN_X &&
      !this.shape.some(([x, y]) => board.has(`${this.x + x - 1},${this.y - y}`))
    ) {
      this.x--;
    } else if (
      direction === ">" &&
      this.x < MAX_X - 1 &&
      !this.shape.some(([x, y]) => board.has(`${this.x + x + 1},${this.y - y}`) || this.x + x >= MAX_X - 1)
    ) {
      this.x++;
    }
    //console.log(
    //   !this.shape.some(([x, y]) => board.has(`${this.x + x},${this.y - y - 1}`)),
    //   !this.shape.some(([_, y]) => this.y - y <= 0),
    // );
    if (this.isBottomSafe(board)) {
      this.y--;
      // console.log("down");
    }
    return this.y;
  }

  insertIntoBoard(board: Set<string>) {
    for (const [x, y] of this.shape) {
      board.add(`${this.x + x},${this.y - y}`);
    }
  }

  removeFromBoard(board: Set<string>) {
    for (const [x, y] of this.shape) {
      board.delete(`${this.x + x},${this.y - y}`);
    }
  }

  isBottomSafe(board: Set<string>) {
    return !this.shape.some(([x, y]) => board.has(`${this.x + x},${this.y - y - 1}`) || this.y - y <= 0);
  }
}

const SHAPES = [
  // row
  [
    [0, 0],
    [1, 0],
    [2, 0],
    [3, 0],
  ],
  // plus
  [
    [1, 0],
    [0, 1],
    [1, 1],
    [2, 1],
    [1, 2],
  ],
  // bottom right
  [
    [2, 0],
    [2, 1],
    [0, 2],
    [1, 2],
    [2, 2],
  ],
  // column
  [
    [0, 0],
    [0, 1],
    [0, 2],
    [0, 3],
  ],
  // square
  [
    [0, 0],
    [1, 0],
    [0, 1],
    [1, 1],
  ],
] as [number, number][][];

const printBoard = (board: Set<string>) => {
  const maxY = Math.max(...[...board].map((s) => parseInt(s.split(",")[1])));
  for (let y = maxY; y >= 0; y--) {
    let line = "|";
    for (let x = 0; x < MAX_X; x++) {
      line += board.has(`${x},${y}`) ? "#" : ".";
    }
    line += "|";
    console.log(line);
  }
  console.log("+" + "-".repeat(MAX_X) + "+");
};

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const solution = (input: string) => {
  //
  //console.log("hello");
  // await sleep(4000);
  // for (let i = 0; i < 100; i++) {
  //   console.log();
  // }
  const board = new Set<string>();
  let highestY = -1;
  let i = 0;
  for (let rock = 0; rock < 2022; rock++) {
    //console.log(rock);
    const piece = new Piece(2, highestY, SHAPES[rock % SHAPES.length]);
    // piece.insertIntoBoard(board);
    // printBoard(board);
    // piece.removeFromBoard(board);
    let previousY = piece.y;
    while (true) {
      // console.log(input[i % input.length], piece.x, piece.y);
      // await sleep(1000);
      const newY = piece.move(input[i++ % input.length], board, false);
      // console.log(newY, previousY);
      // if (!piece.isBottomSafe(board)) {
      //   break;
      // }
      if (newY === previousY) {
        break;
      }
      previousY = newY;
      // piece.insertIntoBoard(board);
      // printBoard(board);
      // piece.removeFromBoard(board);
    }
    highestY = Math.max(highestY, piece.y);
    piece.insertIntoBoard(board);
    // printBoard(board);
    // console.log("next");
    // if (rock == 3) break;
  }
  // console.log(board);
  console.log(highestY + 1);
};

// solution(test);
solution(input);
