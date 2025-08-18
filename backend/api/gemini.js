const express = require('express');
const router = express.Router();
const geminiClient = require('../../services/ai/gemini/geminiClient'); // Adjust path as needed

// POST /api/ai/gemini/text
router.post('/text', async (req, res) => {
  const { prompt, modelId, streaming } = req.body;
  try {
    const response = await geminiClient.generateText(prompt, modelId, streaming);
    res.json(response);
  } catch (error) {
    console.error('Error in /api/ai/gemini/text:', error);
    res.status(500).json({ error: error.message });
  }
});

// POST /api/ai/gemini/multimodal
router.post('/multimodal', async (req, res) => {
  const { parts, modelId, streaming } = req.body;
  try {
    const response = await geminiClient.generateMultimodal(parts, modelId, streaming);
    res.json(response);
  } catch (error) {
    console.error('Error in /api/ai/gemini/multimodal:', error);
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
