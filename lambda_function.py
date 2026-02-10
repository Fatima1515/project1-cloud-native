import io
import json
import os
import pandas as pd
from azure.storage.blob import BlobServiceClient

# Using the built-in shortcut for Azurite
CONN_STR = "UseDevelopmentStorage=true"

def process_data():
    try:
        # Connect to Azurite
        print("Connecting to Azurite...")
        blob_service_client = BlobServiceClient.from_connection_string(CONN_STR)
        blob_client = blob_service_client.get_blob_client(container="datasets", blob="All_Diets.csv")
        
        # Download from the emulator
        print("Downloading All_Diets.csv...")
        stream = blob_client.download_blob().readall()
        
        df = pd.read_csv(io.BytesIO(stream))
        df = df.rename(columns={"Protein(g)": "Protein", "Carbs(g)": "Carbs", "Fat(g)": "Fat"})
        df[["Protein", "Carbs", "Fat"]] = df[["Protein", "Carbs", "Fat"]].fillna(df[["Protein", "Carbs", "Fat"]].mean())

        # Calculate Averages
        avg_macros = df.groupby("Diet_type")[["Protein", "Carbs", "Fat"]].mean()
        highest_protein_diet = avg_macros["Protein"].idxmax()

        # Save to NoSQL Simulation (JSON)
        os.makedirs('simulated_nosql', exist_ok=True)
        result_data = {
            "average_macros": avg_macros.reset_index().to_dict(orient='records'),
            "highest_protein_diet": highest_protein_diet
        }
        
        with open('simulated_nosql/results.json', 'w') as f:
            json.dump(result_data, f, indent=4)

        return f"Success! Task 3 complete.\nWinner: {highest_protein_diet}."

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print(process_data())