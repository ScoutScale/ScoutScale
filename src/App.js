import { useState, useRef } from 'react';
import "./App.css";
import { TailSpin } from 'react-loading-icons';
import MenuIcon from '@mui/icons-material/Menu';

function App() {

  const [authenticated, setAuthenticated] = useState(false);
  const [authLoading, setAuthLoading] = useState(false);

  const authCode = '12345';

  const authRef = useRef();
  const bagRef = useRef();
  const zoneRef = useRef();

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

  const logBags = () => {
    if(bagRef.current.value !== "" && zoneRef.current.value !== "") {
      setAuthLoading(true);
      setTimeout(() => {
        alert(`Bag ${bagRef.current.value} has been added to Zone ${zoneRef.current.value}`);
        bagRef.current.value = '';
        zoneRef.current.value = '';
        setAuthLoading(false);
      }, 500);
    }else {
      alert("Please enter all fields");
    }
  }

  return (
    <div className="background w-full h-screen" >
      {authenticated ? (
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
        <div className="flex items-center flex-col flex items-center">
          <div className="text-slate-950 text-3xl font-bold mt-10">Welcome to Scout Scale!</div>
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
