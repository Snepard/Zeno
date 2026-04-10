const { redis } = require("../config/redis");

async function enqueueJob(queueName, payload) {
  const message = JSON.stringify(payload);
  await redis.lpush(`jobs:${queueName}`, message);
}

module.exports = { enqueueJob };
