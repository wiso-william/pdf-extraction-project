from flask import Flask, request, jsonify
import pdfplumber
import re
import os
import requests
from datetime import datetime
import shutil

app = Flask(__name__)

# Configurazione delle cartelle
INPUT_FOLDER = "../pdf/input"
PROCESSED_FOLDER = "../pdf/processed"
ERROR_FOLDER = "../pdf/error"

# Crea le cartelle se non esistono
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(ERROR_FOLDER, exist_ok=True)

# Espressioni regolari per l'estrazione dei dati
patterns = {
    "Nome": r"(?:Nome|Nominativo)[:\s]+([A-Z][a-z]+\s[A-Z][a-z]+)",
    "Data di nascita": r"(?:Data di nascita)\s*:?\s*([\d]{2}/[\d]{2}/([\d]{4}|[\d]{2}))",
    "Età": r"Età\s*:\s*(\d+)\s*(?:anni)?",
    "Sesso": r"(?:Sesso)[:\s]+(Maschio|Femmina|Uomo|Donna|M|F)",
    "Codice Fiscale": r"(?:Cd fiscale|Codice Fiscale)[:\s]+([A-Z0-9]{16})"
}

def move_file(src_path, success=True):
    """Sposta il file nella cartella processed o error"""
    filename = os.path.basename(src_path)
    dest_folder = PROCESSED_FOLDER if success else ERROR_FOLDER
    dest_path = os.path.join(dest_folder, filename)
    
    try:
        shutil.move(src_path, dest_path)
        print(f"File spostato in {dest_folder}")
    except Exception as e:
        print(f"Errore nello spostamento del file: {e}")

def format_surname(surname):
    """Formatta il cognome con prima lettera maiuscola e resto minuscolo"""
    if not surname or surname == "Non trovato":
        return ""
    return surname[0].upper() + surname[1:].lower()

def extract_first_page_text(pdf_path, char_limit=380):
    """Estrae il testo dalla prima pagina del PDF"""
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0] if pdf.pages else None
        text = first_page.extract_text() if first_page else ""
        return text[:char_limit]

def extract_info(text):
    """Estrae i dati grezzi dal testo"""
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if key == "Età":
                extracted[key] = int(match.group(1))
            else:
                extracted[key] = match.group(1)
        else:
            extracted[key] = None if key == "Età" else "Non trovato"
    
    if extracted.get("Codice Fiscale") and extracted["Codice Fiscale"] != "Non trovato":
        extracted["Codice Fiscale"] = extracted["Codice Fiscale"].upper()
    
    return extracted

def convert_date(date_str):
    """Converte la data da formato italiano a ISO (yyyy-MM-dd)"""
    if date_str == "Non trovato":
        return ""
    
    try:
        day, month, year = date_str.split('/')
        if len(year) == 2:
            year = f"19{year}"
        iso_date = f"{year}-{month}-{day}"
        datetime.strptime(iso_date, "%Y-%m-%d")
        return iso_date
    except Exception as e:
        print(f"⚠️ Errore nella conversione della data '{date_str}': {e}")
        return ""

def normalize_sex(sex_value):
    """Normalizza il sesso in 'M' o 'F'"""
    if not sex_value:
        return ""
    if sex_value.lower() in ["maschio", "uomo", "m"]:
        return "M"
    if sex_value.lower() in ["femmina", "donna", "f"]:
        return "F"
    return ""

@app.route("/extract", methods=["POST"])
def upload_pdf():
    """Gestisce l'upload del PDF, estrae i dati e li invia a Spring Boot"""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["file"]
    
    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Salva il file nella cartella input prima di processarlo
    input_path = os.path.join(INPUT_FOLDER, pdf_file.filename)
    pdf_file.save(input_path)
    
    try:
        text = extract_first_page_text(input_path)
        raw_data = extract_info(text)

        # Adatto i campi al backend Spring Boot
        nome_completo = raw_data["Nome"] if raw_data["Nome"] != "Non trovato" else ""
        nome_parts = nome_completo.split()
        name = nome_parts[0] if len(nome_parts) >= 1 else ""
        surname = format_surname(nome_parts[1] if len(nome_parts) >= 2 else "")

        extracted_data = {
            "name": name,
            "surname": surname,
            "codiceFiscale": raw_data["Codice Fiscale"] if raw_data["Codice Fiscale"] != "Non trovato" else "",
            "birthDate": convert_date(raw_data["Data di nascita"]),
            "sex": normalize_sex(raw_data["Sesso"]),
            "age": raw_data["Età"],
            "height": None,
            "weight": None
        }

        springboot_api_url = "http://localhost:8080/api/v1/profiles"
        spring_response = requests.post(
            springboot_api_url,
            json=extracted_data,
            headers={"Content-Type": "application/json"}
        )

        if spring_response.status_code in [200, 201]:
            print("✅ Dati inviati con successo a Spring Boot")
            move_file(input_path, success=True)
        else:
            print(f"⚠️ Errore nell'invio a Spring Boot: {spring_response.status_code} - {spring_response.text}")
            move_file(input_path, success=False)

        return jsonify({
            "filename": pdf_file.filename,
            "estratti": extracted_data,
            "spring_response": spring_response.status_code
        })

    except Exception as e:
        print(f"❌ Errore durante l'elaborazione del file: {e}")
        move_file(input_path, success=False)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)