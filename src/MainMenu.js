import React, { useState, useRef, useEffect } from 'react';
import { firestore } from "./firebase";
import { collection } from "@firebase/firestore";
import { TailSpin } from 'react-loading-icons';
import MenuIcon from '@mui/icons-material/Menu';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import "./App.css";
import BagLogger from './BagLogger'; 
import Heat from './Heat';
import { DriverCodes } from './DriverCodes';
import ViewTable from './ViewTable';
import ManualEntry from './ManualEntry';
import DeleteData from './DeleteData';

export const MainMenu = ({ authCode }) => {
  const [newLocation, setNewLocation] = useState(0);
  const [adminAuthenticated, setAdminAuthenticated] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [adminPassword, setAdminPassword] = useState('');
  const [menuItem, setMenuItem] = useState(1);
  const [adminButtonLoading, setAdminButtonLoading] = useState(false);
  const [showHeatMap, setShowHeatMap] = useState(false);
  const [coords, setCoords] = useState(null);
  const [isChecked, setChecked] = useState(false);
  const [error, setError] = useState('');
  const [scrollEnabled, setScrollEnabled] = useState(false); 

  
  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      setCoords({longitude: position.coords.longitude, latitude: position.coords.latitude});
    })
  },[]);

  const bagRef = useRef();
  const zoneRef = useRef();
  const ref = collection(firestore, "React App");
  const adminPasswordRef = useRef();
  const valueChange = () => {setChecked(!isChecked);};

  const toggleHeatMap = () => {
    setShowHeatMap(prev => !prev);
  };

  const handleMenuItemClick = (item) => {
    setMenuOpen(false); 
    setMenuItem(item); 
    if (item === 3 || item === 4) {
      setScrollEnabled(true);
    } else {
      setScrollEnabled(false);
    }
  };


  const checkAdminPassword = () => {
    let password = 'adminpassword123'
    setAdminButtonLoading(true);
    setTimeout(() => {
      setAdminButtonLoading(false);
      if (adminPassword.trim() == password) {
        setAdminAuthenticated(true)
      }else {
        setError('incorrect password');
        adminPasswordRef.current.value = '';
      }
    }, Math.floor((Math.random() * 1000) + 100))

  }

  useEffect(() => {
    if (!scrollEnabled) {
      document.body.style.overflow = 'hidden'; 
    } else {
      document.body.style.overflow = 'visible'; 
    }
    return () => {
      document.body.style.overflow = 'visible'; 
    };
  }, [scrollEnabled]);

  
  return (
    <div>
      {coords?.latitude && menuItem == 2 ? (
        <div className="absolute z-0 w-full h-100vh">
          <div className="text-center text-3xl font-bold m-5 mt-20">ScoutScale Heatmap</div>
          <div>
            <Heat />
          </div>
        </div>
      ) : null}
      <div className="relative h-0">
        <button onClick={() => {setMenuOpen(true)}} className= "relative left-2 top-5" >
            <MenuIcon className="text-sm ml-5"/>
        </button>
        <div className={`absolute w-screen z-10 top-0 h-screen bg-[#fff8e8] border border-r-1 left-0 ${menuOpen ? 'translate-x-0 transition ease-in-out duration-300' : '-translate-x-[100%] transition ease-in-out duration-300'}`}>
          <button onClick={() => {setMenuOpen(false)}}>
            <ArrowBackIcon className="text-sm ml-7 mt-5" />
          </button>
          {adminAuthenticated ? (
            <div className="w-full h-full flex items-center flex-col pt-0">
              <button onClick={() => {handleMenuItemClick(1)}} className={`border-b-1 border-blue-300 w-full flex items-center justify-center h-12 font-bold ${menuItem == 1 ? 'text-green-700' : 'text-black'}`}>
                Log Bags
              </button>
              <button onClick={() => {handleMenuItemClick(2); setShowHeatMap(true); }} className={`w-full flex items-center justify-center h-12 font-bold ${menuItem === 2 ? 'text-green-700' : 'text-black'}`}>
                Heat Map
              </button>
              <button onClick={() => {handleMenuItemClick(3)}} className={`w-full flex items-center justify-center h-12 font-bold ${menuItem == 3 ? 'text-green-700' : 'text-black'}`}>
                Driver Codes
              </button>
              <button onClick={() => {handleMenuItemClick(4)}} className={`w-full flex items-center justify-center h-12 font-bold ${menuItem == 4 ? 'text-green-700' : 'text-black'}`}>
                Export Data
              </button>
              <button onClick={() => {handleMenuItemClick(5)}} className={`w-full flex items-center justify-center h-12 font-bold ${menuItem == 5 ? 'text-green-700' : 'text-black'}`}>
                Scale Manual Entry
              </button>
              <button onClick={() => {handleMenuItemClick(6)}} className={`w-full flex items-center justify-center h-12 font-bold ${menuItem == 6 ? 'text-green-700' : 'text-black'}`}>
                Delete All Database Data
              </button>
            </div>
          ) : (
            <div className="w-full h-full flex justify-evenly items-center flex-col">
              <div className="flex items-center flex-col">
                {error !== '' && (
                  <div className="font-bold text-md text-orange-500 mb-5">{error}</div>
                )}
                <div className="font-bold text-xl mb-10">Enter Admin Password:</div>
                <input className="rounded-xl input w-3/5 h-10 text-center placeholder:bold" type="password" ref={adminPasswordRef} placeholder="password" onChange={(e) => {setAdminPassword(e.target.value); if(error !== ''){setError('')}}} />
              </div>
              <button onClick={() => {checkAdminPassword()}} className="flex justify-center items-center text-slate-50 button bg-cyan-50 w-2/5 rounded-lg h-10 text-xl font-bold">
                {adminButtonLoading ? (
                  <TailSpin className="w-5 h-5" />
                ) : (
                  <div>Enter</div>
                )}
              </button>
              <div />
              <div />
            </div>
          )}
        </div>
      </div>
      {coords?.latitude && menuItem == 1 ? (
        <BagLogger authCode={authCode} /> 
      ) : menuItem == 3 ? (
        <DriverCodes />
      ) : menuItem == 4 ? (
        <ViewTable />
      ) : menuItem == 5 ? (
        <ManualEntry authCode={authCode}/>
      ) : menuItem == 6 ? (
        <DeleteData/>
      ): (
        <div className="flex flex-col items-center justify-center w-full h-screen">
          <p className="w-4/5 text-center ">Please Select "Allow" on the prompt.</p>
        </div>
      )}
    </div>
  );
}



