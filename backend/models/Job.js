const mongoose = require("mongoose");

const jobSchema = new mongoose.Schema(
  {
    jobId: { type: String, required: true, unique: true, index: true },
    userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    type: {
      type: String,
      enum: ["lecture", "podcast", "flashcards", "upload"],
      required: true,
    },
    sourcePdfUrl: { type: String },
    status: {
      type: String,
      enum: ["pending", "partial", "complete", "failed"],
      default: "pending",
      index: true,
    },
    payload: { type: Object, default: {} },
    output: { type: Object, default: {} },
    error: { type: String, default: null },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Job", jobSchema);
