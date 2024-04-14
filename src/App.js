import { useState, useRef } from 'react';
import "./App.css";
import { TailSpin } from 'react-loading-icons';
import MenuIcon from '@mui/icons-material/Menu';
import { collection, query, where, getDocs } from "@firebase/firestore";
import { useGeolocated } from "react-geolocated";
import { LogBags } from './LogBags';
import { firestore } from "./firebase";

function App() {

  const [authenticated, setAuthenticated] = useState(false);
  const [authLoading, setAuthLoading] = useState(false);
  const [authCode, setAuthCode] = useState(0);
  const [error, setError] = useState('');

  const authRef = useRef();
  const ref = collection(firestore, "Authentication");

  const enter = async () => {
    setAuthLoading(true);
    const q = query(ref, where("code", "==", parseInt(authRef.current.value)));
    
    const querySnapshot = await getDocs(q);
    if (querySnapshot.size > 0) {
      setAuthenticated(true);
      setAuthCode(parseInt(authRef.current.value));
      setAuthLoading(false);
    }else{
      authRef.current.value = "";
      setAuthenticated(false);
      setAuthLoading(false);
      setError('No matching auth codes exist.')
    }

  }

  return (
    <div className="background w-full h-screen" >
      {authenticated ? (
        <LogBags authCode={authCode} />
      ) : (
        <div className="flex items-center flex-col flex items-center">
          <div className="text-slate-950 text-3xl font-bold mt-10">Welcome to ScoutScale!</div>
          <img alt="logo" src={require("./scout_scale_logo.jpeg")} className="w-2/5 h-2/5 mb-10 mt-10"/>
          {error !== '' && (
            <div className="font-bold text-md text-orange-500 mb-5">{error}</div>
          )}
          <input type="tel" className="rounded-xl input w-3/5 h-10 text-center placeholder:bold mb-20" ref={authRef} onChange={() => {if(error !== ''){setError('')}}}placeholder="auth code"/>
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
