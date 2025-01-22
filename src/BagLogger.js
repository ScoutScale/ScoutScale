import React, { useState, useRef, useEffect } from 'react';
import "./App.css";
import { firestore } from "./firebase";
import { GeoPoint } from 'firebase/firestore';
import { collection, addDoc, query, getDocs, deleteDoc, limit, orderBy, where } from "@firebase/firestore";
import { TailSpin } from 'react-loading-icons';

const BagLogger = ({ authCode }) => {
  const [authLoading, setAuthLoading] = useState(false);
  const [numBags, setnumBags] = useState('');
  const [zoneNum, setzoneNum] = useState('');
  const [coords, setCoords] = useState(null);
  const [isChecked, setChecked] = useState(false);
  const [error, setError] = useState('');
  const [showIncrementDecrementButtons, setShowIncrementDecrementButtons] = useState(false);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      setCoords({longitude: position.coords.longitude, latitude: position.coords.latitude});
    })
  },[]);

  const bagRef = useRef();
  const zoneRef = useRef();
  const ref = collection(firestore, "React App");

  const handleNumBagChange = () => {
    const temp = bagRef.current.value.trim();
    if (temp === '' || !isNaN(parseInt(temp))) {
      setnumBags(temp === '' ? '' : parseInt(temp));
    }
  };

  const handleZoneChange = () => {
    const temp = zoneRef.current.value.trim();
    if (temp === '' || !isNaN(parseInt(temp))) {
      setzoneNum(temp === '' ? '' : parseInt(temp));
    }
  };

  const incrementCount = () => {
    if (numBags === '' || numBags === 0 || !isNaN(numBags)) {
      setnumBags((preValue) => preValue === '' ? 1 : preValue + 1);
    }
  };

  const decrementCount = () => {
    if (numBags === '' || numBags > 0) {
      setnumBags((preValue) => preValue === '' ? 0 : preValue - 1);
    }
  };

  const handleSetNumBags = (number) => {
    setnumBags(number);
    setShowIncrementDecrementButtons(number === 4);  // Only show + and - if the number is 4
  };


  const logBags = () => {
    if (bagRef.current.value !== "" && zoneRef.current.value !== "" && Number.isInteger(parseInt(bagRef.current.value)) && parseInt(bagRef.current.value) > 0 && Number.isInteger(parseInt(zoneRef.current.value)) && parseInt(zoneRef.current.value) > 0) {
      let latitude;
      let longitude;
      navigator.geolocation.getCurrentPosition((position) => {
        latitude = position.coords.latitude
        longitude =  position.coords.longitude
        setCoords({latitude: latitude, longitude: longitude})
      })  
      setAuthLoading(true);
        setTimeout(() => {
          alert(`Bag ${bagRef.current.value} has been added to Zone ${zoneRef.current.value}`);
          
          let data = {
            bags: parseInt(bagRef.current.value),
            zone: parseInt(zoneRef.current.value),
            location: new GeoPoint(latitude, longitude),
            time: new Date(),
            correction: isChecked,
            authCode: authCode
          };
    
          try {
            addDoc(ref, data).then(() => {
              if (isChecked) {
                const queryRef = query(ref, orderBy('time', 'desc'), where("authCode", "==", parseInt(authCode)), limit(2));  
                getDocs(queryRef).then((querySnapshot) => {
                    if (querySnapshot.size > 1) { 
                      const documents = querySnapshot.docs;
                      const docToDelete = documents[1]; 
                      deleteDoc(docToDelete.ref).then(() => console.log("Entry was replaced successfully")).catch((error) => console.log("Error replacing entry: ", error));
                    } else {
                      console.log("No entry to delete or only one entry found.");
                    }
                  }).catch((error) => console.log("Error accessing entry: ", error));
              }
            });
          } catch (e) {
            console.log(e)
          }
    
          bagRef.current.value = '';
          setAuthLoading(false);
          setChecked(false);
          }, 500);
      } else {
        alert("Please enter all fields and make sure they are valid integers.");
      }
    }

  return (
    <div className= "bag-logger-container">
      <div className="flex flex-row items-center justify-between w-full">
        <div />
        <div className="w-1/5 h-1/5 self-end">
          <img alt="logo" src={require("./scout_scale_logo.jpeg")} className=""/>
        </div>
      </div>
      <div className="flex items-center flex-col flex items-center" >
        <div className="text-slate-950 text-3xl font-bold mt-5 mb-10">Log Bag Pickup</div>
        <div className="text-center w-full">
          <div className="flex items-center justify-center space-x-2">
            {showIncrementDecrementButtons && (
              <button onClick={decrementCount} className="rounded-xl button w-1/6 h-10 text-xl font-bold">-</button>
            )}
            <input type="tel" className="rounded-xl input w-2/5 h-10 text-center placeholder:bold" ref={bagRef} 
              placeholder="Bags" value={numBags} onChange={handleNumBagChange}/>
            {showIncrementDecrementButtons && (
              <button onClick={incrementCount} className="rounded-xl button w-1/6 h-10 text-xl font-bold">+</button>
            )}
          </div>
          <br></br>
          <button onClick={() => handleSetNumBags(1)} className="justify-center items-center rounded-xl w-1/6 h-10 m-1 mb-2 button text-xl font-bold">1</button>
          <button onClick={() => handleSetNumBags(2)} className="justify-center items-center rounded-xl w-1/6 h-10 m-1 mb-2 button text-xl font-bold">2</button>
          <button onClick={() => handleSetNumBags(3)} className="justify-center items-center rounded-xl w-1/6 h-10 m-1 mb-2 button text-xl font-bold">3</button>
          <button onClick={() => handleSetNumBags(4)} className="justify-center items-center rounded-xl w-1/6 h-10 m-1 mb-10 button text-xl font-bold">4+</button>
        </div>

        <input type="tel" className="rounded-xl input w-2/5 h-10 text-center placeholder:bold mb-5" ref={zoneRef} placeholder="Zone" onChange={handleZoneChange}
          value={zoneNum}/>

        <div className="text-center">
          <label> 
            Is this a correction to the previous entry?&nbsp;&nbsp;
            <input type="checkbox" checked={isChecked} onChange={() => setChecked(!isChecked)}/>
          </label>
        </div>
        
        <button onClick={() => {logBags()}} className="flex justify-center items-center text-slate-50 button bg-cyan-50 mt-5 mb-5 w-1/5 rounded-lg h-10 text-xl font-bold">
          {authLoading ? (
            <TailSpin className="w-5 h-5" />
          ) : (
            <div>Log</div>
          )}
        </button>
      </div>
    </div>
  );
}

export default BagLogger;
