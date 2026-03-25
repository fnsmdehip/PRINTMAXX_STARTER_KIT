// DEPRECATED: This file is kept for backwards compatibility.
// All chat functionality has moved to ./widget.js
// Use /api/widget/chat instead of /api/chat/chat
const express = require('express');
const router = express.Router();

router.all('*', (req, res) => {
  res.status(301).json({
    error: 'This endpoint has been moved.',
    newEndpoint: '/api/widget/chat',
  });
});

module.exports = router;
