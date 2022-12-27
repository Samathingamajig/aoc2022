import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")));
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

const solution = (_input: string) => {
  //
  console.log("Merry Christmas!");
  console.log("(25b was completing the previous 49 challenges)");
};

// solution(test);
solution(input);
