// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import LoadingScreen from './components/loadingScreen';
import TranslatorPage from './components/TranslatorPage';

// A simple component to display a fatal error
const ErrorDisplay = ({ message }) => (
  <div style={{ textAlign: 'center', margin: '50px', fontFamily: 'sans-serif' }}>
    <h1>❌ Application Error</h1>
    <p>Could not connect to the backend server.</p>
    <p>Please ensure the backend is running correctly and try restarting the application.</p>
    <pre style={{ background: '#f0f0f0', padding: '10px', borderRadius: '5px', color: '#c7254e' }}>
      {message}
    </pre>
  </div>
);

function App() {
  const [isBackendReady, setIsBackendReady] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  const MAX_RETRIES = 15; // Try for 30 seconds (15 retries * 2 seconds)

  useEffect(() => {
    // This function will poll the backend's /health endpoint
    const checkBackendStatus = async () => {
      // If the backend is already marked as ready, do nothing.
      if(retryCount > MAX_RETRIES) return;
      if (isBackendReady) return;

      try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
          console.log("Backend is ready!");
          setIsBackendReady(true);
          // Stop polling once the backend is ready
          clearInterval(intervalId);
        } else {
          // The server is up but returned a non-ok status
          throw new Error(`Server responded with status: ${response.status}`);
        }
      } catch (error) {
        // If fetch fails, the server is likely still starting up or has crashed.
        console.log(`Waiting for backend... (Attempt ${retryCount + 1})`);
        setRetryCount(prevCount => prevCount + 1);
      }
    };

    const intervalId = setInterval(checkBackendStatus, 2000);

    // Cleanup function to stop polling when the component unmounts
    return () => clearInterval(intervalId);
  }, [isBackendReady, retryCount]); // Re-run effect if these change

  // This effect checks if the retry limit has been reached
  useEffect(() => {
    if (retryCount > MAX_RETRIES) {
      setErrorMessage('The backend server failed to start.');
      // Find the interval ID in the first useEffect and clear it here
      // This part is complex, the logic above is simpler by stopping inside checkStatus
      // For simplicity, we just set the error message. The polling will stop naturally
      // when the component re-renders to show the error.
    }
  }, [retryCount]);

  // Use conditional rendering to show the correct screen
  if (errorMessage) {
    return <ErrorDisplay message={errorMessage} />;
  }

  return (
    <div>
      {isBackendReady ? <TranslatorPage /> : <LoadingScreen />}
    </div>
  );
}

export default App;