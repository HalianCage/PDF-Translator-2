// frontend/src/components/TranslatorPage.jsx
import React, { useState, useRef } from 'react';
import '../App.css'; // Reuse the main App.css for styling
import appIcon from '../../public/PDF-Translation-App-Icon-2.jpg';

const TranslatorPage = () => {
  // All the state and functions from your previous App.jsx go here
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState('Select a PDF to begin.');
  const [isLoading, setIsLoading] = useState(false);
  const pollingInterval = useRef(null);

  

    // This function checks the status of the job
    const checkStatus = async (jobId) => {
        try {

            console.log('inside checkStatus with jobID: ', jobId, '\n')

            const response = await fetch(`http://localhost:8000/job-status/${jobId}`);
            if (!response.ok) throw new Error('Network response was not ok.');
            const data = await response.json();

            // Provide user-friendly status messages
            let userFriendlyStatus = data.status;
            switch (data.status) {
                case 'starting': userFriendlyStatus = 'Starting process...'; break;
                case 'extracting': userFriendlyStatus = 'Step 1/3: Extracting text...'; break;
                case 'translating': userFriendlyStatus = 'Step 2/3: Translating text...'; break;
                case 'creating_pdf': userFriendlyStatus = 'Step 3/3: Creating final PDF...'; break;
            }
            setStatus(userFriendlyStatus);
            
            // If the job is complete, stop polling and download the file
            if (data.status === 'complete') {
                clearInterval(pollingInterval.current);
                setStatus('Translation complete! Downloading...');
                window.location.href = `http://localhost:8000/download/${jobId}`;
                setIsLoading(false);
            } else if (data.status === 'error') {
                clearInterval(pollingInterval.current);
                setStatus(`Error: ${data.error}`);
                setIsLoading(false);
            }
        } catch (error) {
            console.error('Polling failed:', error);
            clearInterval(pollingInterval.current);
            setStatus('Error: Could not get job status.');
            setIsLoading(false);
        }
    };

    const handleTranslate = async () => {
        if (!selectedFile) return;
        setIsLoading(true);
        setStatus('Uploading file...');
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            console.log('starting the translation...')
            // Call the endpoint to start the job
            const response = await fetch('http://localhost:8000/start-translation/', {
                method: 'POST',
                body: formData,
        });
        const data = await response.json();

        if (data.job_id) {

            console.log('File has been uploaded. Starting the job...')
            
            setStatus('File uploaded. Starting job...');
            // Start polling for status every 3 seconds
            pollingInterval.current = setInterval(() => checkStatus(data.job_id), 3000);
        } else {
            throw new Error(data.error || 'Failed to start job.');
        }
        } catch (error) {
            console.error('Translation start failed:', error);
            setStatus(`Error: ${error.message}`);
            setIsLoading(false);
        }
    };

    const handleFileChange = (event) => {
        if (pollingInterval.current) {
            clearInterval(pollingInterval.current);
        }
        setSelectedFile(event.target.files[0]);
        setStatus('File selected. Ready to translate.');
        setIsLoading(false);
    };
    
  return (
    <div className="card">
      <div className="card-header">
        <div className="brand-row">
          <img src={appIcon} alt="App Icon" className="brand-logo" />
          <div>
            <h1 className="app-title">Tranzient - Chinese PDF Translator</h1>
            <p className="app-subtitle">Upload a Chinese PDF to translate it to English.</p>
          </div>
        </div>
      </div>
      <div className="card-content">
        <div className="container">
          <div className="controls">
            <div className="file-input">
              <input type="file" onChange={handleFileChange} accept=".pdf" disabled={isLoading} />
              <span className="helper">{selectedFile ? selectedFile.name : 'Select a PDF file (max ~200MB)'}</span>
            </div>
            <div className="actions">
              <button className="btn" onClick={handleTranslate} disabled={isLoading || !selectedFile}>
                {isLoading ? 'Processing…' : 'Translate'}
              </button>
            </div>
          </div>
          {isLoading && (
            <div className="progress" aria-hidden="true">
              <div className="progress-indicator"></div>
            </div>
          )}
          <p className={`status ${isLoading ? 'working' : ''}`}>{status}</p>
        </div>
      </div>
    </div>
  );
};

export default TranslatorPage;