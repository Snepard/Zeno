const Redis = require("ioredis");
const { redisUrl } = require("./env");

const redis = new Redis(redisUrl, {
  maxRetriesPerRequest: null,
  enableReadyCheck: false,
});

module.exports = { redis };
