import { useState } from 'react';

function App() {
  const [formData, setFormData] = useState({
    yardline_100: '',
    ydstogo: '',
    score_differential: '',
    game_seconds_remaining: '',
    qtr: ''
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: Number(e.target.value) });
  };

  const handleSubmit = async () => {
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    const data = await response.json();
    setResult(data);
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>4th Down Decision Model</h1>

      <input name="yardline_100" placeholder="Yards from end zone" onChange={handleChange} />
      <input name="ydstogo" placeholder="Yards to go" onChange={handleChange} />
      <input name="score_differential" placeholder="Score differential" onChange={handleChange} />
      <input name="game_seconds_remaining" placeholder="Seconds remaining" onChange={handleChange} />
      <input name="qtr" placeholder="Quarter" onChange={handleChange} />

      <button onClick={handleSubmit}>Get Recommendation</button>

      {result && (
        <div style={{ marginTop: '1rem' }}>
          <p><strong>Recommended:</strong> {result.recommended}</p>
          <p>Go: {result.expected_values.go.toFixed(3)}</p>
          <p>Punt: {result.expected_values.punt.toFixed(3)}</p>
          <p>Field Goal: {result.expected_values.field_goal.toFixed(3)}</p>
        </div>
      )}
    </div>
  );
}

export default App;