import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")))).replace(/\n$/, "");
const input = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")))).replace(/\n$/, "");
const custom = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./custom.txt")))).replace(/\n$/, "");

const solution = (input: string) => {
  //
  const originalNumbers = Object.freeze(
    input
      .split("\n")
      .map(Number)
      .map((n) => n * 811589153)
      .map((val, i) => `${val}|${i}`),
  );
  const numbers = [...originalNumbers];

  for (let AA = 0; AA < 10; AA++) {
    for (const numStr of originalNumbers) {
      // if (numberToMove === 0) continue;
      const [numberToMove] = numStr.split("|").map(Number);

      const beginIndex = numbers.indexOf(numStr);

      numbers.splice(beginIndex, 1);
      let i = (((beginIndex + numberToMove) % numbers.length) + 2 * numbers.length) % numbers.length;
      // This part isn't actually needed for the computation, but it is for
      if (numberToMove < 0 && i == 0) {
        i = numbers.length;
      }

      numbers.splice(i, 0, numStr);
      // console.log(
      //   numberToMove,
      //   //
      //   numbers.join(", "),
      // );
    }
  }
  const indexOfZero = numbers.findIndex((val) => val.split("|")[0] === "0");

  const _1000 = parseInt(
    numbers[((indexOfZero % numbers.length) + 1000 + 2 * originalNumbers.length) % originalNumbers.length].split(
      "|",
    )[0],
  );
  const _2000 = parseInt(
    numbers[((indexOfZero % numbers.length) + 2000 + 2 * originalNumbers.length) % originalNumbers.length].split(
      "|",
    )[0],
  );
  const _3000 = parseInt(
    numbers[((indexOfZero % numbers.length) + 3000 + 2 * originalNumbers.length) % originalNumbers.length].split(
      "|",
    )[0],
  );
  console.log(_1000, _2000, _3000);
  console.log(_1000 + _2000 + _3000);
};

// solution(test);
solution(input);
// solution(custom);
