// Run this from the rabbitai-frontend directory with
// `node ../scripts/generate_frontend_ts_tasklist.js `, then copy and paste the output into issue
// #10004
const { readdirSync } = require("fs");
const process = require("process");

const INITIAL_DIRECTORIES = ["spec", "src"];
const DEFAULT_DIRECTORY = process.cwd();

const getDirectories = (source) =>
  readdirSync(source, { withFileTypes: true })
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);

const getFilesByExtensions = (source, extensions) =>
  readdirSync(source, { withFileTypes: true })
    .filter((dirent) =>
      extensions.some((extension) => dirent.name.endsWith(extension))
    )
    .map((dirent) => dirent.name);

let directories = INITIAL_DIRECTORIES;

while (directories.length) {
  const curDirectory = directories.pop();
  process.chdir(curDirectory);
  // Check for existence of js, jsx, ts, and tsx files. Show a filled box if only ts and tsx,
  // show an empty box if any js or jsx, and don't print the line if neither exist in the
  // directory.
  const hasTypescriptFiles =
    getFilesByExtensions("./", [".ts", ".tsx"]).length > 0;
  const hasJavascriptFiles =
    getFilesByExtensions("./", [".js", ".jsx"]).length > 0;

  if (hasJavascriptFiles) {
    console.log(
      `${"  ".repeat(
        curDirectory.split("/").length - 1
      )}- [ ] \`${curDirectory}\``
    );
  } else if (hasTypescriptFiles) {
    console.log(
      `${"  ".repeat(
        curDirectory.split("/").length - 1
      )}- [x] \`${curDirectory}\``
    );
  }

  directories = directories.concat(
    getDirectories("./")
      .reverse() // For ABC order when pushed into the Array
      .map((directory) => `${curDirectory}/${directory}`)
  );
  process.chdir(DEFAULT_DIRECTORY);
}
