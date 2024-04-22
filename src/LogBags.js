import { useState, useRef, useEffect } from 'react';
import "./App.css";
import Heat from './Heat';
import ViewTable from './ViewTable';
import ManualEntry from './ManualEntry';
import { TailSpin } from 'react-loading-icons';
import MenuIcon from '@mui/icons-material/Menu';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { firestore } from "./firebase";
import { GeoPoint } from 'firebase/firestore';
import { collection, addDoc, query, getDocs, deleteDoc, limit, orderBy, where } from "@firebase/firestore";
import { DriverCodes } from './DriverCodes';

export const LogBags = ({ authCode }) => {
  const [authLoading, setAuthLoading] = useState(false);
  const [isChecked, setChecked] = useState(false);
  const [numBags, setnumBags] = useState('');
  const [zoneNum, setzoneNum] = useState('');
  const [newLocation, setNewLocation] = useState(0);
  const [coords, setCoords] = useState(null);
  const [adminAuthenticated, setAdminAuthenticated] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [adminPassword, setAdminPassword] = useState('');
  const [menuItem, setMenuItem] = useState(1);
  const [adminButtonLoading, setAdminButtonLoading] = useState(false);
  const [error, setError] = useState('');
  const [showHeatMap, setShowHeatMap] = useState(false);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      setCoords({longitude: position.coords.longitude, latitude: position.coords.latitude});
    })
  },[])

  const bagRef = useRef();
  const zoneRef = useRef();
  const ref = collection(firestore, "React App");
  const adminPasswordRef = useRef();
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

  const toggleHeatMap = () => {
    setShowHeatMap(prev => !prev);
  };

  const checkAdminPassword = () => {
    let password = 'adminpassword123'
    setAdminButtonLoading(true);
    setTimeout(() => {
      setAdminButtonLoading(false);
      if (adminPassword.trim() === password) {
        setAdminAuthenticated(true)
      }else {
        setError('incorrect password');
        adminPasswordRef.current.value = '';
      }
    }, Math.floor((Math.random() * 1000) + 100))

  }

  return (
      <div style={{overflow: 'hidden'}}> {/* Apply CSS to hide overflow */}
        {/*Dont move this menu item 2 down. Makes things go BOOM. remove this comment later*/}
        {coords?.latitude && menuItem === 2 ? (
            <div className="absolute z-0 w-full h-full">
              <div className="text-center text-3xl font-bold m-5 mt-20">ScoutScale Heatmap</div>
              <div>
                <Heat />
              </div>
            </div>
        ) : null}
        <div className="relative">
          <button onClick={() => {setMenuOpen(true)}} className= "relative left-3 top-10" >
            <MenuIcon className="text-sm ml-5"/>
          </button>
          <div className={`absolute w-3/5 z-10 top-0 h-screen bg-[#fff8e8] border border-r-1 left-0 ${menuOpen ? 'translate-x-0 transition ease-in-out duration-300' : '-translate-x-[100%] transition ease-in-out duration-300'}`}>
            <button onClick={() => {setMenuOpen(false)}}>
              <ArrowBackIcon className="text-sm ml-5 mt-10" />
            </button>
            {adminAuthenticated ? (
                <div className="w-full h-full flex items-center flex-col pt-0">
                  <button onClick={() => {setMenuItem(1)}} className={`border-b-1  border-blue-300 w-full flex items-center justify-center h-12 font-bold ${menuItem === 1 ? 'text-green-700' : 'text-black'}`}>
                    Log Bags
                  </button>
                  <button onClick={() => { setMenuItem(2); setShowHeatMap(true); }} className={`w-full flex items-center justify-center h-12 font-bold ${menuItem === 2 ? 'text-green-700' : 'text-black'}`}>
                    Heat Map
                  </button>
                  <button onClick={() => {setMenuItem(3)}} className={`w-full flex items-center justify-center h-12 font-bold ${menuItem === 3 ? 'text-green-700' : 'text-black'}`}>
                    Driver Codes
                  </button>
                  <button onClick={() => {setMenuItem(4)}} className={`w-full flex items-center justify-center h-12 font-bold ${menuItem === 4 ? 'text-green-700' : 'text-black'}`}>
                    View Data
                  </button>
                  <button onClick={() => {setMenuItem(5)}} className={`w-full flex items-center justify-center h-12 font-bold ${menuItem === 5 ? 'text-green-700' : 'text-black'}`}>
                    Manual Entry
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
        {coords?.latitude && menuItem === 1 ? (
            <div>
              <div className="flex flex-row items-center justify-between w-full">
                <div />
                <div className="w-1/5 h-1/5 self-end">
                  <img alt="logo" src={require("./scout_scale_logo.jpeg")} className=""/>
                </div>
              </div>
              <div className="flex items-center flex-col flex items-center mt-10">
                <div className="text-slate-950 text-3xl font-bold  mb-10">Log Bag Pickup</div>
                <input type="tel" className="rounded-xl input w-2/5 h-10 text-center placeholder:bold mb-10" ref={zoneRef}
                       placeholder="zone" onChange={handleZoneChange}
                       value={zoneNum}/>
                <div className="text-center w-full">
                  <button onClick={() => setnumBags(1)}
                          className="justify-center items-center rounded-xl w-1/6 h-10 m-1 mb-2 button text-xl font-bold">1
                  </button>
                  <button onClick={() => setnumBags(2)}
                          className="justify-center items-center rounded-xl w-1/6 h-10 m-1 mb-2 button text-xl font-bold">2
                  </button>
                  <button onClick={() => setnumBags(3)}
                          className="justify-center items-center rounded-xl w-1/6 h-10 m-1 mb-2 button text-xl font-bold">3
                  </button>
                  <button onClick={() => setnumBags(4)}
                          className="justify-center items-center rounded-xl w-1/6 h-10 m-1 mb-10 button text-xl font-bold">4+
                  </button>
                  <br></br>

                  <button onClick={decrementCount} className="rounded-xl button w-1/6 h-10 mr-2 text-xl font-bold">-
                  </button>
                  <input type="tel" className="rounded-xl input w-2/5 h-10 text-center placeholder:bold mb-2" ref={bagRef}
                         placeholder="bags"
                         value={numBags} onChange={handleNumBagChange}/>
                  <button onClick={incrementCount} className="rounded-xl button w-1/6 h-10 ml-2 text-xl font-bold">+
                  </button>

                </div>

                <div className="text-center">
                  <label>
                    Is this a correction to the previous entry?&nbsp;&nbsp;
                    <input type="checkbox" checked={isChecked} onChange={valueChange}/>
                  </label>
                </div>
                <button onClick={() => {
                  logBags()
                }}
                        className="flex justify-center items-center text-slate-50 button bg-cyan-50 mt-10 w-1/5 rounded-lg h-10 text-xl font-bold">
                  {authLoading ? (
                      <TailSpin className="w-5 h-5"/>
                  ) : (
                      <div>Log</div>
                  )}
                </button>
              </div>
            </div>
        ) : menuItem === 3 ? (
            <DriverCodes/>
        ) : menuItem === 4 ? (
            <ViewTable/>
        ) : menuItem === 5 ? (
            <ManualEntry authCode={authCode}/>
        ) : (
            <div className="flex flex-col items-center justify-center w-full h-screen">
              <p className="w-4/5 text-center ">Please Select "Allow" on the prompt.</p>
            </div>
        )}
      </div>
  );
}

