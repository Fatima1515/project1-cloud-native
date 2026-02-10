import io
import json
import os
import pandas as pd
from azure.storage.blob import BlobServiceClient

# Shortcut for local Azurite emulator
CONN_STR = "UseDevelopmentStorage=true"

def process_data_optimized():
    try:
        # 1. Connect to Azurite
        blob_service_client = BlobServiceClient.from_connection_string(CONN_STR)
        blob_client = blob_service_client.get_blob_client(container="datasets", blob="All_Diets.csv")

        # 2. Download from emulator
        print("Downloading data from Azurite...")
        stream = blob_client.download_blob().readall()

        # Task 5 Optimization:
        # Only load the columns needed for calculation to save RAM
        required_columns = ['Diet_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)']
        df = pd.read_csv(io.BytesIO(stream), usecols=required_columns)

        # Data Cleaning
        df = df.rename(columns={"Protein(g)": "Protein", "Carbs(g)": "Carbs", "Fat(g)": "Fat"})
        
        # Fill missing values only for the numeric columns we are using
        numeric_cols = ["Protein", "Carbs", "Fat"]
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

        # Statistical Analysis
        avg_macros = df.groupby('Diet_type')[numeric_cols].mean()
        
        # Adding an extra metric: Protein-to-Carb Ratio
        avg_macros['P_to_C_Ratio'] = avg_macros['Protein'] / avg_macros['Carbs']

        # Save to Simulated NoSQL (JSON)
        os.makedirs('simulated_nosql', exist_ok=True)
        result = avg_macros.reset_index().to_dict(orient='records')
        with open('simulated_nosql/results.json', 'w') as f:
            json.dump(result, f, indent=4)

        return "Success: Task 5 Optimized processing complete."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print(process_data_optimized())