import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")))).replace(/\n$/, "");
const input = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")))).replace(/\n$/, "");

const solution = (input: string) => {
  //
  let cycle = 0;
  let x = 1;
  let sum = 0;

  const inc = () => {
    cycle++;
    // console.log(cycle, x, sum);
    if ([20, 60, 100, 140, 180, 220].includes(cycle)) {
      console.log(cycle, x, x * cycle, sum);
      sum += x * cycle;
    }
  };

  for (const line of input.split("\n")) {
    inc();
    if (line === "noop") continue;
    const num = parseInt(line.split(" ")[1]);
    inc();
    x += num;
    // inc();
  }
  console.log(sum);
};

// solution(test);
solution(input);
