import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const fetchNewWord = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/random-word`);
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchNewWord();
  }, []);

  // YouGlish Widget Effect
  useEffect(() => {
    if (data && data.word) {
      // 1. Clear existing widget container
      const container = document.getElementById('yg-widget-container');
      if (container) {
        container.innerHTML = ''; // Wipe it

        // 2. Create the Anchor
        const anchor = document.createElement('a');
        anchor.id = 'yg-widget-0';
        anchor.className = 'youglish-widget';
        anchor.setAttribute('data-query', data.word);
        anchor.setAttribute('data-lang', 'english');
        anchor.setAttribute('data-components', '8415');
        anchor.setAttribute('data-auto-start', '0');
        anchor.setAttribute('data-bkg-color', 'theme_light');
        anchor.href = 'https://youglish.com';
        anchor.innerText = 'Visit YouGlish.com';
        container.appendChild(anchor);

        // 3. (Re)Load the script
        // Remove old script if exists to force re-execution/re-initialization
        const oldScript = document.getElementById('yg-script');
        if (oldScript) oldScript.remove();

        const script = document.createElement('script');
        script.id = 'yg-script';
        script.src = 'https://youglish.com/public/emb/widget.js';
        script.async = true;
        document.body.appendChild(script);
      }
    }
  }, [data]);

  return (
    <div className="app-container">
      <header>
        <h1>📚 English Learning Hub</h1>
      </header>

      <main>
        {loading && <div className="loading">✨ Discovering new word...</div>}

        {!loading && data && (
          <div className="content">
            <section className="word-hero">
              <h2 className="main-word">{data.word}</h2>
              {data.audio_url && (
                <div className="audio-player">
                  <audio controls src={data.audio_url}>
                    Your browser does not support the audio element.
                  </audio>
                </div>
              )}
            </section>

            <section className="definitions-section">
              <h3>📖 Definitions</h3>
              <ul>
                {data.definitions.map((def, idx) => (
                  <li key={idx}>{def}</li>
                ))}
              </ul>
            </section>

            {data.images && data.images.length > 0 && (
              <section className="images-section">
                <h3>🖼️ Visual Context</h3>
                <div className="image-grid">
                  {data.images.map((url, idx) => (
                    <img key={idx} src={url} alt={`Context ${idx + 1}`} />
                  ))}
                </div>
              </section>
            )}

            <section className="pronunciation-section">
              <h3>🗣️ Pronunciation Coach</h3>
              <div id="yg-widget-container" className="yg-container"></div>

              {data.youglish && data.youglish.nearby_words && (
                <div className="nearby-words">
                  <h4>📍 Nearby Phonetic Words</h4>
                  <div className="tags">
                    {data.youglish.nearby_words.map((w, i) => (
                      <span key={i} className="tag">{w}</span>
                    ))}
                  </div>
                </div>
              )}
            </section>

            <button className="next-btn" onClick={fetchNewWord}>
              Next Random Word 🎲
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
