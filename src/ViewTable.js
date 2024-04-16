import React, { useState } from 'react';
import Papa from 'papaparse';
import './Table.css'; 

const ViewTable = ({ authCode }) => {
  const [csvData, setCsvData] = useState(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      Papa.parse(file, {
        complete: (result) => {
          setCsvData(result.data);
        },
        header: true,
      });
    }
  };

  const downloadInstructions = () => {
    const fileId = '1vyCfCf5Ug5yvwm53zYCjR35LMDgauqow';
    const instructionsFile = `https://drive.google.com/uc?export=download&id=${fileId}`;
    window.location.href = instructionsFile;
  };

  return (
    <div>
        <p className="text-center mt-20">
            Download <span onClick={downloadInstructions} className="download-link">here</span> for instructions on how to view your data.
        </p>
        <div className="table-container">
            <div className="input-file-container text-center">
            <label htmlFor="file" className="input-file-label">Upload CSV File</label>
            <input type="file" id="file" accept=".csv" className="input-file" onChange={handleFileUpload} />
            </div>
            {csvData && (
            <div className="table-container mt-5">
                <table className="table">
                <thead>
                    <tr>
                    {Object.keys(csvData[0]).map((header) => (
                        <th key={header}>{header}</th>
                    ))}
                    </tr>
                </thead>
                <tbody>
                    {csvData.map((row, index) => (
                    <tr key={index}>
                        {Object.values(row).map((value, idx) => (
                        <td key={idx}>{value}</td>
                        ))}
                    </tr>
                    ))}
                </tbody>
                </table>
            </div>
            )}
        </div>
    </div>
  );
};

export default ViewTable;
