import pandas as pd

# Define the data
data = {
    "name": ["Item1", "Item2", "Item3"],
    "brand": ["Brand1", "Brand2", "Brand3"],
    "quantity": [10, 20, 30],
    "Status": [True, False, True],
    "date": ["2023-01-01", "2023-02-01", "2023-03-01"],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file
df.to_excel("test.xlsx", index=False)
