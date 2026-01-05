import express from "express";
import upload from "../middleware/upload.js";
import { identifyPerson } from "../controllers/visionController.js";

const router = express.Router();

router.post("/identify", upload.single("frame"), identifyPerson);

export default router;

