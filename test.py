import pandas as pd

# Define the data
data = {
    "Name": ["Jaya", "Jaya", "Jaya"],
    "brand": ["Brand1", "Brand2", "Brand3"],
    "quantity": [10, 20, 30],
    "Status": [True, False, True],
    "entry Time": ["2023-01-01", "2023-02-01", "2023-03-01"],
    "location": [603, 603, 603],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file
df.to_excel("test.xlsx", index=False)
