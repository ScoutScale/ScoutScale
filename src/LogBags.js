import { useState, useRef } from 'react';
import "./App.css";
import { TailSpin } from 'react-loading-icons';
import MenuIcon from '@mui/icons-material/Menu';
import { firestore } from "./firebase";
import { GeoPoint } from 'firebase/firestore';
import { collection, addDoc } from "@firebase/firestore";
import { useGeolocated } from "react-geolocated";

export const LogBags = () => {
  const [authLoading, setAuthLoading] = useState(false);

  const { coords, isGeolocationAvailable, isGeolocationEnabled } =
  useGeolocated({
      positionOptions: {
          enableHighAccuracy: false,
      },
      userDecisionTimeout: 10000,
  });

  const bagRef = useRef();
  const zoneRef = useRef();
  const ref = collection(firestore, "React App");

  const logBags = () => {
    if(bagRef.current.value !== "" && zoneRef.current.value !== "") {
      setAuthLoading(true);
      setTimeout(() => {
        alert(`Bag ${bagRef.current.value} has been added to Zone ${zoneRef.current.value}`);

        let data = {
          bags: bagRef.current.value,
          zone: zoneRef.current.value,
          location: new GeoPoint(coords?.latitude, coords?.longitude),
          time: new Date().toLocaleString()
        };

        try {
          addDoc(ref, data)
        }catch(e){
          console.log(e)
        }

        bagRef.current.value = '';
        zoneRef.current.value = '';
        setAuthLoading(false);
      }, 500);
    }else {
      alert("Please enter all fields");
    }
  }

  return (
    <div>
    {!isGeolocationAvailable ? (
        <div className="flex flex-col items-center justify-center w-full h-screen">
            <p className="w-4/5 text-center ">Your browser does not support geolocation</p>
        </div>
    ) : !isGeolocationEnabled ? (
        <div className="flex flex-col items-center justify-center w-full h-screen">
            <p className="w-4/5 text-center ">Please enable geolocation on your browser's settings, or use a different device and allow location permissions.</p>
        </div>
    ) : coords ? (
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
            <input className="rounded-xl input w-2/5 h-10 text-center placeholder:bold mb-10" ref={bagRef} placeholder="bags"/>
            <input className="rounded-xl input w-2/5 h-10 text-center placeholder:bold mb-20" ref={zoneRef} placeholder="zone"/>
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
