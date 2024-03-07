import { useState, useRef } from 'react';
import "./App.css";
import { TailSpin } from 'react-loading-icons';
import MenuIcon from '@mui/icons-material/Menu';
import { firestore } from "./firebase";
import { collection, addDoc } from "@firebase/firestore";
import { useGeolocated } from "react-geolocated";
import { LogBags } from './LogBags';

function App() {

  const [authenticated, setAuthenticated] = useState(false);
  const [authLoading, setAuthLoading] = useState(false);

  const authCode = '12345';

  const authRef = useRef();

  const enter = () => {
    setAuthLoading(true);
    setTimeout(() => {
      if (authRef.current.value === authCode) {
        setAuthenticated(true);
      }else {
        authRef.current.value = '';
        alert("invalid auth code");
      }
      setAuthLoading(false);
    }, 500);

  }

  return (
    <div className="background w-full h-screen" >
      {authenticated ? (
        <LogBags />
      ) : (
        <div className="flex items-center flex-col flex items-center">
          <div className="text-slate-950 text-3xl font-bold mt-10">Welcome to ScoutScale!</div>
          <img alt="logo" src={require("./scout_scale_logo.jpeg")} className="w-2/5 h-2/5 mb-10 mt-10"/>
          <input className="rounded-xl input w-3/5 h-10 text-center placeholder:bold mb-20" ref={authRef} placeholder="auth code"/>
          <button onClick={() => {enter()}} className="flex justify-center items-center   text-slate-50 button bg-cyan-50 mt-20 w-1/5 rounded-lg h-10 text-xl font-bold">
            {authLoading ? (
              <TailSpin className="w-5 h-5" />
            ) : (
              <div>Enter</div>
            )}
          </button>
        </div>
      )}
    </div>

  );
}

export default App;
