const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');
const app = express();

// ENABLE CORS REQUESTS FOR ALL POINTS
app.use(cors());

// PARSE JSON
app.use(express.json());

// POST :: ENDPOINT
app.post('/api/search', (req, res) => {
  const { word } = req.body;

  // RUN PY SCRIPT
  const pythonScriptPath = path.join(__dirname, 'word_processor.py');
  const command = `python3 ${pythonScriptPath} "${word}"`;  // or "python" if needed

  // EXECUTE PYTHON SCRIPT
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error('Error executing Python script:', error);
      return res.status(500).json({ error: 'Error executing Python script' });
    }

    if (stderr) {
      console.error('stderr:', stderr);
      return res.status(500).json({ error: 'stderr from Python script' });
    }

    // PARSE OUTPUT
    try {
      const wordData = JSON.parse(stdout);  // Parse the JSON output from Python script
      if (wordData.valid) {
        res.json({
          valid: true,
          word: wordData.word,
          synonyms: wordData.synonyms,
          antonyms: wordData.antonyms,
          collocations: wordData.collocations,
        });
      } else {
        res.json({
          valid: false,
          error: `Word "${word}" not found in database.`,
          suggestion: wordData.suggestion || null,
        });
      }
    } catch (e) {
      console.error('Error parsing Python script output:', e);
      res.status(500).json({ error: 'Failed to parse Python script output' });
    }
  });
});

// START SERVER
app.listen(5000, () => {
  console.log('Server is running on http://localhost:5000');
});
