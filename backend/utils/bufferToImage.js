module.exports = (buff, path) => {
  const b64 = Buffer.from(buff).toString("base64");
  require("fs").writeFile(path, b64, "base64", function (err) {
    console.log(err);
  });
};
