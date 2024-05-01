import React, { useState, useRef, useEffect } from 'react';
import "./App.css";
import { firestore } from "./firebase";
import { collection, addDoc, deleteDoc, getDocs} from "@firebase/firestore";




const DeleteData = () => {
    const [delString, setDelString] = useState('');
    const handleDeleteData = async () => {
      if(delString == "adminpassword123"){
        if(window.confirm("WARNING: This will delete all data in the database.")){
          try {
            const collectionScale = collection(firestore, 'Scale App');
            const collectionApp = collection(firestore, 'React App');
            const querySnapshotApp = await getDocs(collectionApp);
            querySnapshotApp.forEach(async (doc) => {
              await deleteDoc(doc.ref);
            });

            const querySnapshotScale = await getDocs(collectionScale);
            querySnapshotScale.forEach(async (doc) => {
              await deleteDoc(doc.ref);
            });
            alert('All data successfully deleted!');
          } catch (error) {
            alert('Error removing data: ', error);
          }
        }

      }
    };
    
    return (
        <div className="flex flex-col items-center justify-center w-full mt-15">
          <div className="text-3xl font-bold mb-6 mt-20">Delete all items in Firebase</div>
          <div className="flex flex-col items-center justify-center w-full">
          <div className="text-1x1 mb-6 mt-10">Type the admin password to delete all data in the firebase</div>
            <div className="flex justify-center mb-4">
              <input
                type="password"
                value={delString}
                onChange={(e) => setDelString(e.target.value)}
                className="rounded-lg w-4/5 h-10 border border-black px-4 py-2 mr-1 text-center"
              />
            </div>
            <button onClick={handleDeleteData } className="flex items-center justify-center bg-green-800 text-white rounded-lg px-6 py-3 mt-10"> Confirm
            </button>
          </div>
        </div>
    );
};

export default DeleteData;