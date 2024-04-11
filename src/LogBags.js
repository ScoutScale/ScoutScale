import { useState, useRef, useEffect } from 'react';
import "./App.css";
import { TailSpin } from 'react-loading-icons';
import MenuIcon from '@mui/icons-material/Menu';
import { firestore } from "./firebase";
import { GeoPoint } from 'firebase/firestore';
import { collection, addDoc, query, getDocs, deleteDoc, limit, orderBy, where } from "@firebase/firestore";

export const LogBags = ({ authCode }) => {
  const [authLoading, setAuthLoading] = useState(false);
  const [isChecked, setChecked] = useState(false);
  const [numBags, setnumBags] = useState('');
  const [zoneNum, setzoneNum] = useState('');
  const [newLocation, setNewLocation] = useState(0);
  const [coords, setCoords] = useState(null)

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      setCoords({longitude: position.coords.longitude, latitude: position.coords.latitude});
    })
  },[])


  const bagRef = useRef();
  const zoneRef = useRef();
  const ref = collection(firestore, "React App");
  const valueChange = () => {setChecked(!isChecked);};

  
  //Increment/Decrement Button Stuff
  const handleNumBagChange = () => {
    const temp = bagRef.current.value.trim();
    if (temp === '' || !isNaN(parseInt(temp))) {
      setnumBags(temp === '' ? '' : parseInt(temp));
    }
  };

  //Makes Sure zone is int
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
    <div>
    {coords?.latitude ? (
        <div>
            <div className="flex flex-row items-center justify-between w-full">
            <div className="w-2/5 h-2/5" >
                <MenuIcon className="text-sm"/>
            </div>
            <div className="w-1/5 h-1/5 self-end">
                <img alt="logo" src={require("./scout_scale_logo.jpeg")} className=""/>
            </div>
            </div>
            <div className="flex items-center flex-col flex items-center mt-10">
            <div className="text-slate-950 text-3xl font-bold mt-10 mb-20">Log Bag Pickup</div>
            <div className = "text-center w-full">
              <button onClick={decrementCount} className = "rounded-xl button w-1/6 h-10 mr-2" >-</button>
              <input className="rounded-xl input w-2/5 h-10 text-center placeholder:bold mb-10" ref={bagRef} placeholder="bags" 
              value={numBags} onChange={handleNumBagChange}/>
              <button onClick={incrementCount} className = "rounded-xl button w-1/6 h-10 ml-2">+</button>
            </div>
            <input className="rounded-xl input w-2/5 h-10 text-center placeholder:bold mb-20" ref={zoneRef} placeholder="zone" onChange={handleZoneChange}
             value={zoneNum}/>
            <div className="text-center">
              <label> 
                Is this a correction to the previous entry?&nbsp;&nbsp;
                <input type="checkbox" checked={isChecked} onChange={valueChange}/>
                    <p>Warning: This WILL delete and replace your last entry. This action cannot be undone.</p>
              </label>
            </div>
            <button onClick={() => {logBags()}} className="flex justify-center items-center   text-slate-50 button bg-cyan-50 mt-20 w-1/5 rounded-lg h-10 text-xl font-bold">
                {authLoading ? (
                <TailSpin className="w-5 h-5" />
                ) : (
                <div>Log</div>
                )}
            </button>
            </div>
        </div>
    ) : (
        <div className="flex flex-col items-center justify-center w-full h-screen">
            <p className="w-4/5 text-center ">Please Select "Allow" on the prompt.</p>
        </div>
    )}
    </div>
  );

}
