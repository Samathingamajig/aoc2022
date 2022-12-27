import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")))).replace(/\n$/, "");
const input = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")))).replace(/\n$/, "");

const decimalToSnafu = (num: number): string => {
  if (num < 3) return num.toString();

  const digits: (number | string)[] = ["", ...num.toString(5)].map(Number);

  for (let i = digits.length - 1; i >= 1; i--) {
    //
    if (digits[i] === 3) {
      digits[i - 1] = +digits[i - 1] + 1;
      digits[i] = "=";
    } else if (digits[i] === 4) {
      digits[i - 1] = +digits[i - 1] + 1;
      digits[i] = "-";
    } else if (digits[i] === 5) {
      digits[i - 1] = +digits[i - 1] + 1;
      digits[i] = 0;
    }
  }

  if (digits[0] == 0) {
    digits.splice(0, 1);
  }

  return digits.join("");
};

const snafuToDecimal = (str: string): number => {
  const rev = [...str].reverse().join("");
  let output = 0;
  for (let i = 0; i < str.length; i++) {
    if ("012".includes(rev[i])) {
      output += 5 ** i * +rev[i];
    } else if (rev[i] == "-") {
      output -= 5 ** i;
    } else if (rev[i] == "=") {
      output -= 5 ** i * 2;
    }
  }
  return output;
};

const solution = (input: string) => {
  //
  const snafus = input.split("\n");
  // const nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 2022, 12345, 314159265];
  const nums = snafus.map((n) => snafuToDecimal(n));
  console.log(nums);

  // const snafus2 = nums.map((n) => decimalToSnafu(n));
  // console.log(snafus2);

  const sum = nums.reduce((a, b) => a + b, 0);
  console.log(decimalToSnafu(sum));
};

// solution(test);
solution(input);
