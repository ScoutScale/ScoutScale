import { useState, useEffect } from 'react';
import { collection, addDoc, query, getDocs, deleteDoc, limit, orderBy, where } from "@firebase/firestore";
import { firestore } from "./firebase";
import { TailSpin } from 'react-loading-icons';


export const DriverCodes = () => {

    const ref = collection(firestore, "Authentication");

    const [driverCodes, setDriverCodes] = useState(null);
    const [alreadyLoaded, setAlreadyLoaded] = useState(false);

    useEffect(() => {
        async function getData(){
            const q = query(ref, where("code", ">", 0 ));
            const querySnapshot = await getDocs(q);
            let tempDriverCodes = [];
            querySnapshot.forEach((doc) => {
                tempDriverCodes.push(doc.data().code)
            });
            setDriverCodes(tempDriverCodes);
        }
        if (!alreadyLoaded) {
            getData()
            setAlreadyLoaded(true)
        }
    },[])

    return driverCodes == null ? (
        <div className="flex justify-center items-center h-screen w-full">
            <TailSpin className="w-5 h-5" />
        </div>
    ) : (
        <div className="flex justify-center items-center h-3/5 w-full flex-col overflow-y-hidden">
            <div className="font-bold text-xl mb-5 mt-10">All Driver Codes:</div>
            {driverCodes.map((code) => {
                return (
                    <div className="font-bold text-lg mb-2">
                        {code}
                    </div>
                )
            })}
        </div>
    )
}