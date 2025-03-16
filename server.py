from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from bleak import BleakScanner, BleakClient

app = FastAPI()

# Allow all origins for development (you can customize this for production)
origins = [
    "http://localhost",  # React app
    "http://localhost:3000",  # React app (default port)
    "http://127.0.0.1:3000",  # React app (127.0.0.1)
]

# Add CORSMiddleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow frontend to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Function to discover Bluetooth devices
async def discover_devices():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    return devices

# Endpoint to scan for BLE devices
@app.get("/scan_bluetooth")
async def scan_bluetooth():
    devices = await discover_devices()
    devices_info = [{"name": device.name or "Unknown", "address": device.address} for device in devices]
    return JSONResponse(content=devices_info)

# Endpoint to connect to a specific Bluetooth device by address
@app.get("/connect_device/{address}")
async def connect_device(address: str):
    try:
        async with BleakClient(address) as client:
            if await client.is_connected():
                status = f"Connected to {address} successfully!"
            else:
                status = f"Failed to connect to {address}"
    except Exception as e:
        status = f"Connection failed: {e}"
    
    return JSONResponse(content={"status": status})

# Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "FastAPI server is running!"}

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
