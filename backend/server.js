const express = require("express");
const cors = require("cors");
const morgan = require("morgan");
const path = require("path");
const routes = require("./api/routes");
const { connectDb } = require("./config/db");
const { port } = require("./config/env");

async function bootstrap() {
  await connectDb();

  const app = express();
  app.use(cors());
  app.use(express.json({ limit: "10mb" }));
  app.use(morgan("dev"));
  app.use("/storage", express.static(path.resolve(__dirname, "../storage")));

  app.get("/health", (_req, res) => res.json({ ok: true }));
  app.use("/api", routes);

  app.use((err, _req, res, _next) => {
    // Centralized error handling keeps controllers focused.
    console.error(err);
    res.status(500).json({ message: "Internal server error" });
  });

  app.listen(port, () => {
    console.log(`backend listening on ${port}`);
  });
}

bootstrap().catch((err) => {
  console.error("Failed to start backend", err);
  process.exit(1);
});
