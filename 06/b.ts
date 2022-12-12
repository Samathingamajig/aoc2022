import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./text.txt")));
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

const solution = (input: string) => {
  //
  for (let i = 13; i < input.length; i++) {
    // console.log(i - 3, i + 1, new Set(input.slice(i - 3, i + 1)));
    if (new Set(input.slice(i - 13, i + 1)).size === 14) {
      console.log(i + 1);
      return;
    }
  }
};
// `bvwbjplbgvbhsrlpgdmjqwftvncz
// nppdvjthqldpwncqszvftbrmjlhg
// nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
// zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw`
//   .split("\n")
//   .forEach(solution);
// solution(test);
solution(input);
