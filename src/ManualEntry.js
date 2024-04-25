import React, { useState, useEffect } from 'react';
import { firestore } from "./firebase";
import { GeoPoint } from 'firebase/firestore';
import { collection, addDoc } from "@firebase/firestore";
import { TailSpin } from 'react-loading-icons';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';

const ManualEntry = () => {
  const [Weight, setWeight] = useState('');
  const [Zone, setZone] = useState('');
  const [Unit, setUnit] = useState('');
  const [manualLoading, setManualLoading] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleManualEntry = () => {
    if (Weight !== '' && Zone !== '' && Unit !== '') {
      setManualLoading(true);
      const data = {
        Weight: parseInt(Weight),
        Zone: parseInt(Zone),
        Date: new Date(),
        Unit: Unit
      };
      addDoc(collection(firestore, "Scale App"), data)
        .then(() => {
          alert("Manual entry added successfully!");
          setWeight('');
          setZone('');
          setUnit('');
          setManualLoading(false);
        })
        .catch(error => {
          console.error("Error adding document: ", error);
          setManualLoading(false);
        });
    } else {
      alert("Please enter valid Weight and Zone values and select the proper units.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center w-full mt-20">
      <div className="text-3xl font-bold mb-6 mt-20">Scale Manual Entry</div>
      <div className="flex flex-col items-center justify-center w-full">
        <div className="flex items-center mb-4">
          <input
            type="number"
            value={Weight}
            onChange={(e) => setWeight(e.target.value)}
            placeholder="Weight"
            className="rounded-lg border border-black px-4 py-2 mr-2"
          />
          <input
            type="number"
            value={Zone}
            onChange={(e) => setZone(e.target.value)}
            placeholder="Zone"
            className="rounded-lg border border-black px-4 py-2"
          />
        </div>
        <div>
          <select value={Unit} onChange={(e) => setUnit(e.target.value)} className="rounded-lg border border-black px-4 py-2">
            <option value="">Select Units</option>
            <option value="lb">Pounds (lb)</option>
            <option value="kg">Kilograms (kg)</option>
          </select>
        </div>
        <div className="flex items-center mb-4 mt-2">
          <img alt="clock" src={require("./ClockIcon.png")} className="w-5 h-5"/>
          &nbsp;{currentTime.toLocaleTimeString()}
        </div>
        <button onClick={handleManualEntry} className="flex items-center justify-center bg-green-800 text-white rounded-lg px-6 py-3">
          {manualLoading ? <TailSpin className="w-6 h-6 mr-2" /> : <AddCircleOutlineIcon className="mr-2" />}
          Add Entry
        </button>
      </div>
    </div>
  );
};

export default ManualEntry;
