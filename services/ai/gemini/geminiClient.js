const { GoogleGenerativeAI } = require('@google/generative-ai');

const API_KEY = process.env.GEMINI_API_KEY;
const PROJECT_ID = process.env.GEMINI_PROJECT_ID; // Not directly used by GenerativeAI, but good to include
const DEFAULT_MODEL = process.env.GEMINI_DEFAULT_MODEL || 'gemini-1.5-pro';

if (!API_KEY) {
  console.warn("GEMINI_API_KEY is not set in environment variables.");
}

const genAI = new GoogleGenerativeAI(API_KEY);

/**
 * Generates text content using a specified Gemini model.
 * @param {string} prompt The text prompt.
 * @param {string} [modelId=DEFAULT_MODEL] The ID of the Gemini model to use.
 * @param {boolean} [streaming=false] Whether to stream the response.
 * @returns {Promise<object>} The generation result.
 */
async function generateText(prompt, modelId = DEFAULT_MODEL, streaming = false) {
  const model = genAI.getGenerativeModel({ model: modelId });
  const result = await model.generateContent(prompt);
  // TODO: Implement streaming logic if streaming is true
  return result.response;
}

/**
 * Generates multimodal content using a specified Gemini model.
 * @param {Array<string|object>} parts Array of text and/or image parts.
 * @param {string} [modelId=DEFAULT_MODEL] The ID of the Gemini model to use.
 * @param {boolean} [streaming=false] Whether to stream the response.
 * @returns {Promise<object>} The generation result.
 */
async function generateMultimodal(parts, modelId = DEFAULT_MODEL, streaming = false) {
  const model = genAI.getGenerativeModel({ model: modelId });
  const result = await model.generateContent(parts);
  // TODO: Implement streaming logic if streaming is true
  return result.response;
}

module.exports = {
  generateText,
  generateMultimodal,
};
