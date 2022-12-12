import * as p from "https://deno.land/std@0.165.0/path/mod.ts";
const test = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./test.txt")));
const input = await Deno.readTextFile(p.fromFileUrl(import.meta.resolve("./input.txt")));

interface Directory {
  name: string;
  path: string;
  filesSize: number;
  subdirectories: Directory[];
  parent: Directory | null;
  totalSize: number;
}
console.log("hello");

const solution = (input: string) => {
  const root = {
    name: "/",
    path: "/",
    filesSize: 0,
    subdirectories: [],
    parent: null,
    totalSize: 0,
  } as Directory;

  let workingDirectoryPath = "/";

  const directories = new Map<string, Directory>([["/", root]]);

  for (const line of input.split("\n")) {
    // console.log(workingDirectory);
    if (line.startsWith("$")) {
      if (line.startsWith("$ ls")) continue;
      const newDir = line.slice(5);
      const previousWorkingDirectoryPath = workingDirectoryPath;
      console.log([workingDirectoryPath, newDir]);
      if (newDir === "/") {
        workingDirectoryPath = "/";
      } else if (newDir === "..") {
        workingDirectoryPath = workingDirectoryPath.slice(0, workingDirectoryPath.lastIndexOf("/"));
        if (workingDirectoryPath === "") workingDirectoryPath = "/";
      } else {
        workingDirectoryPath += (workingDirectoryPath === "/" ? "" : "/") + newDir;
      }
      if (!directories.has(workingDirectoryPath)) {
        directories.set(workingDirectoryPath, {
          name: newDir,
          path: workingDirectoryPath,
          filesSize: 0,
          subdirectories: [],
          parent: directories.get(previousWorkingDirectoryPath)!,
          totalSize: 0,
        });
        directories.get(previousWorkingDirectoryPath)!.subdirectories.push(directories.get(workingDirectoryPath)!);
      }
    } else if (!line.startsWith("dir")) {
      const [sizeString, name] = line.split(" ");
      const size = parseInt(sizeString);
      const directory = directories.get(workingDirectoryPath)!;
      directory.filesSize += size;
    }
  }
  // let smallCount = 0;
  // let smallTotal = 0;
  let total = 0;
  for (const directory of [...directories.values()].reverse()) {
    total += directory.filesSize;
  }
  const cutoff = total - (70000000 - 30000000);
  let smallestLargeEnough = Infinity;
  for (const directory of [...directories.values()].reverse()) {
    directory.totalSize = directory.filesSize + directory.subdirectories.reduce((acc, cur) => acc + cur.totalSize, 0);
    console.log(directory.path, directory.totalSize, smallestLargeEnough);
    if (directory.totalSize < smallestLargeEnough && directory.totalSize >= cutoff) {
      console.log("hit");
      smallestLargeEnough = directory.totalSize;
      // smallCount++;
      // smallTotal += directory.totalSize;
    }
  }
  // console.log([smallCount, smallTotal]);
  console.log(smallestLargeEnough);
};

// solut/ion(test);
solution(input);
