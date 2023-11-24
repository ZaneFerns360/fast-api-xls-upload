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

    # Exclude the first row
    df = df.iloc[1:]

    # Iterate over the rows
    for index, row in df.iterrows():
        # Prepare the data
        data = {
            "item_name": row["name"],
            "brand": row["brand"],
            "quantity": row["quantity"],
            "Status": row["Status"],
            "date": row["date"],
        }

        # Send the POST request
        response = requests.post(
            "http://127.0.0.1:8090/api/collections/equipment_test/records", json=data
        )

        # Print the response
        print(response.json())

    return {"filename": file.filename}
