const { v4: uuidv4 } = require("uuid");
const Job = require("../models/Job");
const { enqueueJob } = require("../services/queueService");

function toPublicStoragePath(filePath) {
  return filePath.replace(/\\/g, "/");
}

function toLegacySlides(output) {
  const slides = output?.slides || [];
  return slides.map((slide) => ({
    heading: slide.title || `Slide ${slide.slide_number}`,
    summary: (slide.bullets || []).join(" "),
    important_points: slide.bullets || [],
    script: slide.speaker_notes || "",
    audio_url: output?.[`audio_slide_${slide.slide_number}`] || null,
    slide_url: slide.slide_url || null,
  }));
}

async function uploadPdf(req, res) {
  if (!req.file) {
    return res.status(400).json({ message: "PDF file is required" });
  }

  const pdfUrl = toPublicStoragePath(req.file.path);
  return res.status(201).json({
    pdf_url: pdfUrl,
    status: "complete",
  });
}

async function generateLecture(req, res) {
  const { pdf_url, title } = req.body;
  const jobId = uuidv4();

  await Job.create({
    jobId,
    userId: req.user.id,
    type: "lecture",
    sourcePdfUrl: pdf_url,
    status: "pending",
    payload: { title },
  });

  await enqueueJob("lecture", {
    job_id: jobId,
    user_id: req.user.id,
    pdf_url,
    title,
  });

  return res.status(202).json({
    job_id: jobId,
    status: "pending",
  });
}

async function getLectureById(req, res) {
  const { id } = req.params;
  const job = await Job.findOne({ jobId: id, userId: req.user.id });

  if (!job) {
    return res.status(404).json({ message: "Lecture job not found" });
  }

  return res.json({
    job_id: job.jobId,
    status: job.status,
    output: job.output,
    lecture_title: job.output?.title || "AI Lecture",
    slides: toLegacySlides(job.output),
    error: job.error,
  });
}

async function generatePodcast(req, res) {
  if (req.body?.slide_content) {
    const script = String(req.body.slide_content);
    const midpoint = Math.max(1, Math.floor(script.length / 2));
    const first = script.slice(0, midpoint).trim() || "Let us begin.";
    const second = script.slice(midpoint).trim() || "That wraps this topic.";

    return res.json({
      dialogue: [
        { speaker: "ziva", text: first },
        { speaker: "zyro", text: second },
      ],
      timings: [
        { start: 0, end: 4, speaker: "ziva" },
        { start: 4, end: 8, speaker: "zyro" },
      ],
      audio_url: null,
      status: "partial",
    });
  }

  const { pdf_url, tone = "educational" } = req.body;
  const jobId = uuidv4();

  await Job.create({
    jobId,
    userId: req.user.id,
    type: "podcast",
    sourcePdfUrl: pdf_url,
    status: "pending",
    payload: { tone },
  });

  await enqueueJob("podcast", {
    job_id: jobId,
    user_id: req.user.id,
    pdf_url,
    tone,
  });

  return res.status(202).json({
    job_id: jobId,
    status: "pending",
  });
}

async function generateFlashcards(req, res) {
  const { pdf_url, count = 20 } = req.body;
  const jobId = uuidv4();

  await Job.create({
    jobId,
    userId: req.user.id,
    type: "flashcards",
    sourcePdfUrl: pdf_url,
    status: "pending",
    payload: { count },
  });

  await enqueueJob("flashcards", {
    job_id: jobId,
    user_id: req.user.id,
    pdf_url,
    count,
  });

  return res.status(202).json({
    job_id: jobId,
    status: "pending",
  });
}

module.exports = {
  uploadPdf,
  generateLecture,
  getLectureById,
  generatePodcast,
  generateFlashcards,
};
