import { useState, useRef, useEffect } from 'react';
import "./App.css";
import { TailSpin } from 'react-loading-icons';
import MenuIcon from '@mui/icons-material/Menu';
import { collection, query, where, getDocs } from "@firebase/firestore";
import { useGeolocated } from "react-geolocated";
import { MainMenu } from './MainMenu';
import { firestore } from "./firebase";

function App() {

  const [authenticated, setAuthenticated] = useState(false);
  const [authLoading, setAuthLoading] = useState(false);
  const [authCode, setAuthCode] = useState(0);
  const [error, setError] = useState('');

  const authRef = useRef();
  const ref = collection(firestore, "Authentication");

  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.key === 'Enter') {
        document.getElementById("enterButton").click(); // Trigger click event of Enter button
      }
    };

    document.addEventListener('keypress', handleKeyPress);

    return () => {
      document.removeEventListener('keypress', handleKeyPress);
    };
  }, []);

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
      setError('No matching auth codes exist. 41706')
    }
  };

  return (
    <div className="bag-logger-container" >
      {authenticated ? (
        <MainMenu authCode={authCode} />
      ) : (
        <div className="flex items-center flex-col flex items-center">
          <div className="text-slate-950 text-3xl font-bold mt-10">Welcome to ScoutScale!</div>
          <img alt="logo" src={require("./scout_scale_logo.jpeg")} className="w-50% h-50% mb-1 mt-1"/>
          {error !== '' && (
            <div className="font-bold text-md text-orange-500 mb-5">{error}</div>
          )}
          <input type="tel" className="rounded-xl input w-3/5 h-10 text-center placeholder:bold mb-5" ref={authRef} onChange={() => {if(error !== ''){setError('')}}}placeholder="Driver Code"/>
          <button id="enterButton" onClick={() => {enter()}} className="flex justify-center items-center   text-slate-50 button bg-cyan-50 mt-1 w-1/5 rounded-lg h-10 text-xl font-bold">
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
