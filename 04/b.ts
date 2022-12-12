import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

// const lines = input.split("\n");
// const overlaps = lines.reduce((acc, line) => {
//   const [left, right] = line.split(",");
//   const [l1, l2] = left.split("-").map(Number);
//   const [r1, r2] = right.split("-").map(Number);
//   if (l1 >= r1 && l1 <= r2) {
//     acc++;
//   } else if (r1 >= l1 && r1 <= l2) {
//     acc++;
//   } else if (l2 >= r1 && l2 <= r2) {
//     acc++;
//   } else if (r2 >= l1 && r2 <= l2) {
//     acc++;
//   }
//   return acc;
// }, 0);
// console.log(overlaps);

// console.log(input.split`
// `.map(v=>v.split`,`.map(v=>v.split`-`.map(v=>+v))).filter(v=>v[1][0]<=v[0][1]&v[0][0]<=v[1][1]).length)

console.log(input.split`
`.map(v=>v.split(/-|,/).map(v=>+v)).filter(v=>v[2]<=v[1]&v[0]<=v[3]).length)

console.log(input.split`
`.map(v=>v.split(/-|,/).map(v=>+v)).filter(([a,b,c,d])=>c<=b&a<=d).length)

console.log(input.split`
`.map(v=>v.split(/-|,/)).filter(([a,b,c,d])=>+c<=+b&+a<=+d).length)

console.log(input.split`
`.map(v=>v.split(/-|,/)).filter(([a,b,c,d])=>-c>~b&-a>~d).length)

console.log(input.split`
`.map(v=>v.split(/\D/)).filter(([a,b,c,d])=>-c>~b&-a>~d).length)