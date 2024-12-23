import React, { useState } from 'react';
import './styles/Sidebar.css';

function Sidebar({ onResultReceived }) {
  const [job, setJob] = useState('');
  const [location, setLocation] = useState('');
  const [domain, setDomain] = useState('');
  const [resume, setResume] = useState(null);
  const [sliderValue, setSliderValue] = useState(300);

  const handleJobChange = (event) => setJob(event.target.value);
  const handleLocationChange = (event) => setLocation(event.target.value);
  const handleDomainChange = (event) => setDomain(event.target.value);
  const handleResumeChange = (event) => setResume(event.target.files[0]);
  const handleSliderChange = (event) => setSliderValue(event.target.value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('file', resume);
    formData.append('job_title', job);
    formData.append('location', location);
    formData.append('domain', domain);
    formData.append('num_outputs', sliderValue);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        // Pass the jobs to App component using the onResultReceived prop
        onResultReceived(result.jobs); 
      } else {
        console.error('Error:', result.error);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form className="sidebar" onSubmit={handleSubmit}>
      <h2>Upload your Resume</h2>
      <div className="upload-box">
        <input
          type="file"
          id="resumeUpload"
          accept=".pdf,.doc,.docx"
          onChange={handleResumeChange}
        />
        <label htmlFor="resumeUpload" className="browse-button">Choose File</label>
        <span className="filename">{resume ? resume.name : 'No file chosen'}</span>
      </div>

      <h2>Preferred Job</h2>
      <input
        type="text"
        className="input-box"
        value={job}
        onChange={handleJobChange}
      />

      <h2>Preferred Location</h2>
      <input
        type="text"
        className="input-box"
        value={location}
        onChange={handleLocationChange}
      />

      <div>
        <h2>Search Domain</h2>
        <div className="slider-container">
          <input
            className="slider-input"
            type="range"
            min="300"
            max="3000"
            step="300"
            value={sliderValue}
            onChange={handleSliderChange}
          />
          <span>{sliderValue}</span>
        </div>
      </div>

      <button className="submit-button" type="submit" onSubmit={handleSubmit}>Submit</button>
    </form>
  );
}

export default Sidebar;
