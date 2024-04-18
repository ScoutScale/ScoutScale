import React, { useEffect, useState } from "react";
import { TileLayer, MapContainer } from "react-leaflet";
import { HeatmapLayer } from "react-leaflet-heatmap-layer-v3";
import "leaflet/dist/leaflet.css";
import { collection, onSnapshot } from "firebase/firestore";
import { firestore } from "./firebase";

const Heat = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const unsubscribe = onSnapshot(
      collection(firestore, "React App"),
      (snapshot) => {
        const newData = snapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
        }));
        setData(newData);
      }
    );

    return () => unsubscribe();
  }, []);

  const heatmapData = data
    .map((point) => {
      const { latitude, longitude } = point.location || {};
      const bags = point.bags;
      if (
        latitude !== undefined &&
        longitude !== undefined &&
        !isNaN(latitude) &&
        !isNaN(longitude) &&
        bags !== undefined
      ) {
        return [latitude, longitude, bags];
      } else {
        return null;
      }
    })
    .filter((point) => point !== null);

  // Calculate bounds for valid heatmapData points
  const validPoints = heatmapData.filter(
    (point) => !isNaN(point[0]) && !isNaN(point[1])
  );
  const bounds =
    validPoints.length > 0
      ? validPoints
      : [
          [0, 0],
          [0, 0],
        ];

  return (
    <div>
      <MapContainer
        style={{ height: "800px", width: "100%"}} // Adjust dimensions as needed
        bounds={bounds}
        zoom={5}
        key={Math.random()}
      >
        <HeatmapLayer
          fitBoundsOnLoad
          fitBoundsOnUpdate
          points={heatmapData}
          longitudeExtractor={(point) => point[1]}
          latitudeExtractor={(point) => point[0]}
          intensityExtractor={(point) => parseFloat(point[2])}
          radius={20}
          blur={20}
          maxZoom={18}
          minOpacity={0.5}
          maxOpacity={1}
          useLocalExtrema={true}
        />
        <TileLayer
          attribution="</a> ScoutScale"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
      </MapContainer>
    </div>
  );
};

export default Heat;
