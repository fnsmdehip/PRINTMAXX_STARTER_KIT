const { HfInference } = require('@huggingface/inference');
const logger = require('../lib/logger');

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`;

const hf = process.env.HUGGINGFACE_API_KEY
  ? new HfInference(process.env.HUGGINGFACE_API_KEY)
  : null;

/**
 * Build the system prompt with knowledge base context.
 */
function buildPrompt(knowledgeItems, conversationHistory, userMessage, websiteName) {
  let contextBlock = '';
  if (knowledgeItems && knowledgeItems.length > 0) {
    contextBlock = knowledgeItems
      .map((item) => `### ${item.title}\n${item.content}`)
      .join('\n\n');
  }

  const historyBlock = conversationHistory
    .map((m) => `${m.role === 'user' ? 'Customer' : 'Support Agent'}: ${m.content}`)
    .join('\n');

  return {
    systemPrompt: `You are a helpful, friendly AI customer support agent for "${websiteName || 'this website'}".
Answer questions based ONLY on the knowledge base provided below. If you don't know something, say so honestly and suggest the customer contact human support.
Keep responses concise (2-3 sentences max unless more detail is needed). Be warm but professional.

${contextBlock ? `=== KNOWLEDGE BASE ===\n${contextBlock}\n=== END KNOWLEDGE BASE ===` : 'No knowledge base items are configured yet. Provide helpful general responses and suggest the customer contact human support for specific questions.'}`,
    conversationText: historyBlock
      ? `${historyBlock}\nCustomer: ${userMessage}\nSupport Agent:`
      : `Customer: ${userMessage}\nSupport Agent:`,
  };
}

/**
 * Call Gemini API (primary).
 */
async function callGemini(systemPrompt, conversationText) {
  const body = {
    contents: [
      {
        parts: [{ text: `${systemPrompt}\n\n${conversationText}` }],
      },
    ],
    generationConfig: {
      temperature: 0.7,
      topP: 0.9,
      maxOutputTokens: 300,
    },
  };

  const response = await fetch(GEMINI_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Gemini API error ${response.status}: ${errorText}`);
  }

  const data = await response.json();
  const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!text) {
    throw new Error('Empty response from Gemini');
  }
  return text.trim();
}

/**
 * Call HuggingFace Inference (fallback).
 */
async function callHuggingFace(systemPrompt, conversationText) {
  if (!hf) {
    throw new Error('HuggingFace API key not configured');
  }

  const response = await hf.textGeneration({
    model: 'microsoft/DialoGPT-medium',
    inputs: `${systemPrompt}\n\n${conversationText}`,
    parameters: {
      max_new_tokens: 200,
      temperature: 0.7,
      top_p: 0.9,
      repetition_penalty: 1.2,
    },
  });

  return response.generated_text.trim();
}

/**
 * Generate AI response with Gemini primary + HuggingFace fallback.
 */
async function generateResponse(
  knowledgeItems,
  conversationHistory,
  userMessage,
  websiteName
) {
  const { systemPrompt, conversationText } = buildPrompt(
    knowledgeItems,
    conversationHistory,
    userMessage,
    websiteName
  );

  try {
    return await callGemini(systemPrompt, conversationText);
  } catch (geminiError) {
    logger.warn('Gemini failed, trying fallback', { error: geminiError.message });
  }

  try {
    return await callHuggingFace(systemPrompt, conversationText);
  } catch (hfError) {
    logger.warn('HuggingFace fallback also failed', { error: hfError.message });
  }

  return "I'm sorry, I'm having trouble processing your request right now. Please try again in a moment, or contact our support team directly for assistance.";
}

module.exports = { generateResponse };
