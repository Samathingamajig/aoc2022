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
      .map((val, i) => `${val}|${i}`),
  );
  const numbers = [...originalNumbers];

  for (const numStr of originalNumbers) {
    // if (numberToMove === 0) continue;
    const [numberToMove] = numStr.split("|").map(Number);

    const beginIndex = numbers.indexOf(numStr);

    // const newIndex =
    //   (((beginIndex + numberToMove + (numberToMove < 0 ? -1 : 0)) % numbers.length) +
    //     Math.abs(Math.trunc((numberToMove + beginIndex) / numbers.length)) +
    //     numbers.length * 2) %
    //   numbers.length;
    // const wraps =
    // let newIndex =
    //   (((beginIndex + numberToMove) % numbers.length) + numbers.length * 2 + (numberToMove < 0 ? -1 : 0)) %
    //   numbers.length;
    // if (newIndex === 0 && numberToMove < 0) newIndex = newIndex + numbers.length - 1;

    numbers.splice(beginIndex, 1);
    let i = (((beginIndex + numberToMove) % numbers.length) + 2 * numbers.length) % numbers.length;
    if (numberToMove < 0 && i == 0) {
      i = numbers.length;
    }
    // if (numberToMove > 0 && )

    // if (numberToMove === -12) {
    //   console.log([
    //     beginIndex + numberToMove + (numberToMove < 0 ? -1 : 0),

    //     (beginIndex + numberToMove + (numberToMove < 0 ? -1 : 0)) % numbers.length,

    //     Math.abs(Math.trunc((numberToMove + beginIndex) / numbers.length)),

    //     ((beginIndex + numberToMove + (numberToMove < 0 ? -1 : 0)) % numbers.length) +
    //       Math.abs(Math.trunc((numberToMove + beginIndex) / numbers.length)) +
    //       numbers.length * 2,

    //     (((beginIndex + numberToMove + (numberToMove < 0 ? -1 : 0)) % numbers.length) +
    //       Math.abs(Math.trunc((numberToMove + beginIndex) / numbers.length)) +
    //       numbers.length * 2) %
    //       numbers.length,
    //   ]);
    // }

    numbers.splice(
      i,
      //  + (beginIndex < newIndex ? 1 : 0)
      0,
      numStr,
    );
    // console.log(
    //   numberToMove,
    //   //
    //   numbers.join(", "),
    // );
  }
  // const indexOfZeroInOriginal = input.split("\n").map(Number).indexOf(0)
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

  // console.log(numbers);
};

// solution(test);
solution(input);
// solution(custom);

/*
const newIndex =
      (((beginIndex + numberToMove) % numbers.length) +
        (numberToMove < 0 ? -1 : 0)-
        Math.trunc((numberToMove + ) / Number.length) +
        2 * originalNumbers.length) %
      originalNumbers.length;

    numbers.splice(newIndex, 0, numberToMove);
    // console.log({ numberToMove, numbers: numbers.join(" ") });
    console.log(numbers.join(", "));
*/
