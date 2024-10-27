import React from 'react';

function Chatbot() {
  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <iframe 
        src="http://localhost:8501" 
        title="Chatbot Streamlit App" 
        style={{ height: '100%', width: '100%', border: 'none' }}
      ></iframe>
    </div>
  );
}

export default Chatbot;
