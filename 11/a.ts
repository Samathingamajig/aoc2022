import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")))).replace(/\n$/, "");
const input = (await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")))).replace(/\n$/, "");

interface Monkey {
  items: number[];
  operator: "+" | "-" | "*" | "/";
  opVal: number | string;
  test: number;
  toTrue: number;
  toFalse: number;
  inspections: number;
}

const solution = (input: string) => {
  //
  const monkeys = input.split("\n\n").map((data) => {
    const lines = data.split("\n");
    const items = lines[1].split(": ")[1].split(", ").map(Number);
    const operator = lines[2].split("old ")[1][0] as "+" | "-" | "*" | "/";
    const opVal = isNaN(Number(lines[2].split("old ")[1].split(" ")[1]))
      ? "old"
      : Number(lines[2].split("old ")[1].split(" ")[1]);
    const test = Number(lines[3].split("by ")[1]);
    const toTrue = Number(lines[4].split("to monkey ")[1]);
    const toFalse = Number(lines[5].split("to monkey ")[1]);
    const monkey: Monkey = {
      items,
      operator,
      opVal,
      test,
      toTrue,
      toFalse,
      inspections: 0,
    };
    // console.log(monkey);
    return monkey;
  });

  console.log(monkeys);

  for (let round = 0; round < 20; round++) {
    for (const monkey of monkeys) {
      while (monkey.items.length) {
        monkey.inspections++;
        let value = monkey.items[0];
        if (monkey.operator === "*") {
          value *= monkey.opVal === "old" ? monkey.items[0] : (monkey.opVal as number);
        } else if (monkey.operator === "/") {
          value /= monkey.opVal === "old" ? monkey.items[0] : (monkey.opVal as number);
          value = Math.floor(value);
        } else if (monkey.operator === "+") {
          value += monkey.opVal === "old" ? monkey.items[0] : (monkey.opVal as number);
        } else if (monkey.operator === "-") {
          value -= monkey.opVal === "old" ? monkey.items[0] : (monkey.opVal as number);
        }
        value = Math.floor(value / 3);

        if (value % monkey.test === 0) {
          monkeys[monkey.toTrue].items.push(value);
        } else {
          monkeys[monkey.toFalse].items.push(value);
        }
        monkey.items.shift();
      }
    }
  }

  console.log(monkeys.map((m) => m.inspections).join("\n"));
  const sorted = monkeys.sort((a, b) => b.inspections - a.inspections);
  console.log(sorted[0].inspections * sorted[1].inspections);
};

// solution(test);
solution(input);
