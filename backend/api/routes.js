const express = require("express");
const authRoutes = require("./authRoutes");
const jobRoutes = require("./jobRoutes");
const { authGuard } = require("../auth/middleware");

const router = express.Router();

router.use("/auth", authRoutes);
router.use("/", authGuard, jobRoutes);

module.exports = router;
