import os
import requests
import shutil

# Configurazione cartelle
PDF_INPUT_FOLDER = "../pdf/input"
PDF_PROCESSED_FOLDER = "../pdf/processed"
PDF_ERROR_FOLDER = "../pdf/error"
FLASK_API_URL = "http://127.0.0.1:5001/extract"

# Crea le cartelle se non esistono
for folder in [PDF_INPUT_FOLDER, PDF_PROCESSED_FOLDER, PDF_ERROR_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def move_file(file_path, success):
    """Sposta il file nella cartella appropriata dopo l'elaborazione"""
    filename = os.path.basename(file_path)
    try:
        if success:
            dest_folder = PDF_PROCESSED_FOLDER
        else:
            dest_folder = PDF_ERROR_FOLDER
        
        dest_path = os.path.join(dest_folder, filename)
        
        # Rimuovi se esiste già
        if os.path.exists(dest_path):
            os.remove(dest_path)
        
        shutil.move(file_path, dest_path)
        print(f"File spostato in {dest_path}")
        return True
    except Exception as e:
        print(f"Errore nello spostamento del file {filename}: {str(e)}")
        try:
            os.remove(file_path)
            print(f"File {filename} eliminato dalla cartella input")
            return True
        except Exception as e:
            print(f"Impossibile eliminare il file {filename}: {str(e)}")
            return False

def send_pdfs():
    """Invia tutti i PDF dalla cartella input al servizio Flask"""
    for filename in os.listdir(PDF_INPUT_FOLDER):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(PDF_INPUT_FOLDER, filename)
            print(f"\nInvio file: {filename}")

            try:
                with open(file_path, "rb") as f:
                    files = {"file": (filename, f, "application/pdf")}
                    response = requests.post(FLASK_API_URL, files=files)

                if response.ok:
                    print(f"✔️ Successo - {filename}")
                    print("Dati estratti:", response.json().get('estratti', 'N/A'))
                    move_file(file_path, success=True)
                else:
                    print(f"❌ Errore - {filename}: {response.status_code}")
                    print("Errore:", response.json().get('error', 'N/A'))
                    move_file(file_path, success=False)

            except Exception as e:
                print(f"❌ Eccezione durante l'invio di {filename}: {str(e)}")
                move_file(file_path, success=False)

if __name__ == "__main__":
    send_pdfs()