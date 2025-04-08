import os
import requests

# Configurazione delle cartelle
PDF_INPUT_FOLDER = "../pdf/input"
flask_url = "http://127.0.0.1:5001/extract"

# Cicla su tutti i PDF nella cartella input
for filename in os.listdir(PDF_INPUT_FOLDER):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(PDF_INPUT_FOLDER, filename)
        print(f"Inviando: {filename}")

        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "application/pdf")}
            response = requests.post(flask_url, files=files)

        if response.ok:
            print(f"✔️ {filename} processato con successo")
            print("Risposta del server:", response.json())
        else:
            print(f"❌ Errore nell'elaborazione di {filename}: {response.status_code} - {response.text}")