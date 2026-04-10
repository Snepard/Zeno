const bcrypt = require("bcryptjs");
const User = require("../models/User");
const { signToken } = require("../auth/jwt");

async function register(req, res) {
  const { email, password, name } = req.body;

  const existing = await User.findOne({ email: email.toLowerCase() });
  if (existing) {
    return res.status(409).json({ message: "Email already in use" });
  }

  const passwordHash = await bcrypt.hash(password, 10);
  const user = await User.create({
    email: email.toLowerCase(),
    passwordHash,
    name,
  });

  return res.status(201).json({
    token: signToken(user),
    user: { id: user._id, email: user.email, name: user.name },
  });
}

async function login(req, res) {
  const { email, password } = req.body;
  const user = await User.findOne({ email: email.toLowerCase() });

  if (!user) {
    return res.status(401).json({ message: "Invalid credentials" });
  }

  const ok = await bcrypt.compare(password, user.passwordHash);
  if (!ok) {
    return res.status(401).json({ message: "Invalid credentials" });
  }

  return res.json({
    token: signToken(user),
    user: { id: user._id, email: user.email, name: user.name },
  });
}

module.exports = { register, login };
