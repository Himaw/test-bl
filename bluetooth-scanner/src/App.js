import React, { useState, useEffect } from "react";

function App() {
  const [devices, setDevices] = useState([]);
  const [status, setStatus] = useState("");

  // Function to scan devices by making an HTTP request to the backend
  const scanDevices = async () => {
    setDevices([]);
    try {
      const response = await fetch("http://127.0.0.1:8000/scan_bluetooth");
      const data = await response.json();
      setDevices(data); // Setting the devices data in the state
    } catch (error) {
      console.error("Error scanning devices:", error);
    }
  };

  // Function to connect to a device by making an HTTP request
  const connectDevice = async (address) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/connect_device/${address}`
      );
      const data = await response.json();
      setStatus(data.status); // Display the connection status
    } catch (error) {
      console.error("Error connecting to device:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Bluetooth Scanner</h2>
      <button
        onClick={scanDevices}
        style={{ padding: "10px", fontSize: "16px" }}
      >
        Scan for Devices
      </button>
      <h3>Devices:</h3>
      <ul>
        {devices.length > 0 ? (
          devices.map((device, index) => (
            <li key={index}>
              {device.name ? device.name : "Unnamed Device"} ({device.address})
              <button onClick={() => connectDevice(device.address)}>
                Connect
              </button>
            </li>
          ))
        ) : (
          <li>No devices found.</li>
        )}
      </ul>
      {status && <h3>Status: {status}</h3>}
    </div>
  );
}

export default App;
