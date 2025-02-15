const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(cors());

// Serve JSON files from the translations directory
app.use('/translations', express.static(path.join(__dirname, '..', 'translations')));

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`JSON server running on http://localhost:${PORT}`);
});
