const express = require("express");
const multer = require("multer");
const fs = require("fs");
const path = require("path");
const {
  uploadPdf,
  generateLecture,
  getLectureById,
  generatePodcast,
  generateFlashcards,
} = require("../controllers/jobController");

const router = express.Router();

const uploadDir = path.resolve(__dirname, "../../storage/uploads");
fs.mkdirSync(uploadDir, { recursive: true });

const storage = multer.diskStorage({
  destination: (_req, _file, cb) => cb(null, uploadDir),
  filename: (_req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`),
});

const upload = multer({ storage });

router.post("/upload-pdf", upload.single("pdf"), uploadPdf);
router.post("/generate-lecture", generateLecture);
router.get("/lecture/:id", getLectureById);
router.post("/generate-podcast", generatePodcast);
router.post("/generate-flashcards", generateFlashcards);

module.exports = router;
