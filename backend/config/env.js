require("dotenv").config();

module.exports = {
  port: process.env.BACKEND_PORT || 4000,
  mongoUri: process.env.MONGODB_URI || "mongodb://localhost:27017/zeno",
  redisUrl: process.env.REDIS_URL || "redis://localhost:6379/0",
  jwtSecret: process.env.JWT_SECRET || "change-me",
  aiEngineUrl: process.env.AI_ENGINE_URL || "http://localhost:8000",
};
