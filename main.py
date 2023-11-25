from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import io

app = FastAPI()

origins = [
    "http://localhost:3000",  # Allow localhost for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    # Store the contents in a variable
    data = io.BytesIO(contents)

    # Read the Excel file
    df = pd.read_excel(data)

    # First, validate all items
    for index, row in df.iterrows():
        # Convert the date and time format
        date = pd.to_datetime(row["entry Time"]).strftime("%Y-%m-%d %H:%M:%S")

        # Check if the employee name matches a specific value in the database
        response = requests.get(
            f"http://127.0.0.1:8090/api/collections/staff/records?filter=(name='{row['Name']}')"
        )

        # If the employee name does not match, return an error
        if response.json()["totalItems"] == 0:
            return {
                "error": f"Employee name {row['Name']} does not match any record in the database"
            }

        # Check if the location matches a specific value in the database
        response = requests.get(
            f"http://127.0.0.1:8090/api/collections/room/records?filter=(room_id='{row['location']}')"
        )

        # If the location does not match, return an error
        if response.json()["totalItems"] == 0:
            return {
                "error": f"Location {row['location']} does not match any record in the database"
            }

    # If all items are valid, send the POST requests
    for index, row in df.iterrows():
        # Get the staff ID and room ID
        staff_id = requests.get(
            f"http://127.0.0.1:8090/api/collections/staff/records?filter=(name='{row['Name']}')"
        ).json()["items"][0]["id"]
        room_id = requests.get(
            f"http://127.0.0.1:8090/api/collections/room/records?filter=(room_id='{row['location']}')"
        ).json()["items"][0]["id"]

        # Prepare the data
        data = {
            "staff": staff_id,
            "brand": row["brand"],
            "quantity": row["quantity"],
            "Status": row["Status"],
            "date": date,
            "room": room_id,
        }

        # Send the POST request
        response = requests.post(
            "http://127.0.0.1:8090/api/collections/equipment_test/records", json=data
        )

        # Print the response
        print(response.json())

    return {"filename": file.filename}
