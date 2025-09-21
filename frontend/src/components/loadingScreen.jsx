// frontend/src/components/LoadingScreen.jsx
import React from 'react';
import './loadingScreen.css'; // We'll create this file for the spinner animation

const LoadingScreen = () => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <h1>Initializing Backend</h1>
      <p>The translation model is loading. This may take a moment on the first start...</p>
    </div>
  );
};

export default LoadingScreen;