import React, { useState, useEffect } from 'react';
import { firestore } from "./firebase";
import { GeoPoint } from 'firebase/firestore';
import { collection, addDoc } from "@firebase/firestore";
import { TailSpin } from 'react-loading-icons';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';

const ManualEntry = () => {
  const [bags, setBags] = useState('');
  const [zone, setZone] = useState('');
  const [corrected, setCorrected] = useState(false);
  const [authCode, setAuthCode] = useState('');
  const [manualLoading, setManualLoading] = useState(false);
  const [coords, setCoords] = useState(null);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      setCoords({latitude: position.coords.latitude, longitude: position.coords.longitude});
    });
  }, []);

  const handleManualEntry = () => {
    if (bags !== '' && zone !== '' && coords && authCode !== '') {
      setManualLoading(true);
      const data = {
        bags: parseInt(bags),
        zone: parseInt(zone),
        location: new GeoPoint(coords.latitude, coords.longitude),
        time: new Date(),
        correction: corrected,
        authCode: parseInt(authCode)
      };
      addDoc(collection(firestore, "React App"), data)
        .then(() => {
          alert("Manual entry added successfully!");
          setBags('');
          setZone('');
          setCorrected(false);
          setAuthCode('');
          setManualLoading(false);
        })
        .catch(error => {
          console.error("Error adding document: ", error);
          setManualLoading(false);
        });
    } else {
      alert("Please enter bags, zone, auth code, and make sure location is available.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center w-full mt-20">
      <div className="text-3xl font-bold mb-6 mt-20">Manual Entry</div>
      <div className="flex flex-col items-center justify-center w-full">
        <div className="flex items-center mb-4">
          <input
            type="number"
            value={bags}
            onChange={(e) => setBags(e.target.value)}
            placeholder="Bags"
            className="rounded-lg border border-black px-4 py-2 mr-2"
          />
          <input
            type="number"
            value={zone}
            onChange={(e) => setZone(e.target.value)}
            placeholder="Zone"
            className="rounded-lg border border-black px-4 py-2"
          />
        </div>
        <label className="flex items-center mb-4">
          <input
            type="checkbox"
            checked={corrected}
            onChange={(e) => setCorrected(e.target.checked)}
            className="mr-2"
          />
          Is this a correction to the previous entry?
        </label>
        <div className="flex items-center mb-4">
          <LocationOnIcon className="text-gray-500 mr-2" />
          <span>{coords ? `${coords.latitude}, ${coords.longitude}` : 'Loading location...'}</span>
        </div>
        <input
            type="number"
            value={authCode}
            onChange={(e) => setAuthCode(e.target.value)}
            placeholder="Auth Code"
            className="rounded-lg border border-black px-4 py-2 mb-4"
            onKeyDown={(e) => {if(e.key === 'Enter'){handleManualEntry()}}}
        />
        <button onClick={handleManualEntry} className="flex items-center justify-center bg-green-800 text-white rounded-lg px-6 py-3">
          {manualLoading ? <TailSpin className="w-6 h-6 mr-2" /> : <AddCircleOutlineIcon className="mr-2" />}
          Add Manual Entry
        </button>
      </div>
    </div>
  );
};

export default ManualEntry;
