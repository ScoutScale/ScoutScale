// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "@firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAu8l3ivfZOgIvSv_-eNZdTmzuAKbbAIPw",
  authDomain: "scout-scale-1.firebaseapp.com",
  projectId: "scout-scale-1",
  storageBucket: "scout-scale-1.appspot.com",
  messagingSenderId: "440634508717",
  appId: "1:440634508717:web:8246708c8db2b60952cd24",
  measurementId: "G-H3TCVP430J"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const firestore = getFirestore(app);
export { firestore };