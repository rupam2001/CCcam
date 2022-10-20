const express = require("express");
const app = express();
const WebSocket = require("ws");
const wss = new WebSocket.Server({ port: 5001 });
console.log("Websocket Stated at port", 5001);

const bufferToImage = require("./utils/bufferToImage");

app.post("/chunk", (req, res) => {
  console.log("chunk endpoint Hit");
});

app.get("/", (req, res) => {
  console.log("main endpoint hit");
  res.send("Server running");
});

let viewer = null;

wss.on("connection", (ws, req) => {
  console.log("New Client Joined");

  ws.on("message", (msg) => {
    onMessage(msg, ws);
  });
});

let i = 0;

function onMessage(msg, ws) {
  console.log("onMessage hit", i++);

  try {
    let oldmsg = msg;
    try {
      msg = JSON.parse(msg.toString());
    } catch (error) {
      if (viewer) {
        viewer.ws.send(oldmsg);
        console.log("sent to viewer", i);
        if (viewer["saveData"]) {
          bufferToImage(oldmsg, "./saved/images/" + i + ".jpg");
        }
      }
      return;
    }
    console.log(msg);
    if (msg.viewer != "yes") {
      console.log(msg, "buffer");
      if (viewer) {
        viewer.ws.send(oldmsg);
        console.log("sent to viewer", i);
        if (viewer["saveData"]) {
          bufferToImage(oldmsg, "./saved/images/" + i + ".jpg");
        }
      }
    } else {
      // msg = JSON.parse(msg.toString());
      if (msg.viewer == "yes" && msg.saveData) {
        viewer["saveData"] = msg.start;
        console.log("saveData Mode turned ", msg.start);
      } else if (msg.viewer == "yes") {
        viewer = { ws };
        console.log("viwer joined");
      }
    }
  } catch (e) {
    console.log("err", e);
  }
}

const path = require("path");
app.use("/static", express.static(path.join(__dirname, "public")));

app.listen(5000, () => console.log("Server is running at port 5000"));
