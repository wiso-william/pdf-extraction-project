# PDF Extraction Project

Progetto incentrato sull'estrazione automatica di dati anagrafici da file PDF tramite Python. I dati vengono salvati su un database MongoDB grazie a un backend in Spring Boot, e visualizzati o modificati tramite un'interfaccia web sviluppata in React.

---

## Tecnologie utilizzate

- **Frontend**: React + Vite (JavaScript)
    
- **Backend REST API**: Spring Boot (Java 21)
    
- **Parsing PDF**: Flask (Python 3.11)
    
- **Database**: MongoDB Atlas
    

---

## Funzionalità principali

- Estrazione di dati anagrafici da PDF tramite espressioni regolari (regex)
    
- Caricamento automatico dei dati estratti su MongoDB
    
- Backend strutturato con architettura MVC in Spring Boot
    
- Visualizzazione e modifica dei dati tramite interfaccia React
    
- Comunicazione tra Flask → Spring Boot → MongoDB
    

---

## Esecuzione del progetto in locale

### 1. Clona le repository

```
git clone https://github.com/wiso-william/pdf-extraction-project
```

### 2. Configura l’ambiente

1. Crea un database MongoDB (locale o su Atlas)
    
2. Apri il progetto Spring Boot e installa le dipendenze (`pom.xml`)
    
3. **Lombok**: assicurati che sia installato nel tuo IDE (es. IntelliJ o STS4).
    
4. In `application.properties` troverai variabili come:
    
    ```
    spring.data.mongodb.database=${MONGO_DATABASE}
    spring.data.mongodb.username=${MONGO_USER}
    spring.data.mongodb.password=${MONGO_PASSWORD}
    spring.data.mongodb.uri=${MONGO_CLUSTER}
    ```
    
    Non modificarle direttamente. Configura le variabili d’ambiente nel tuo IDE (es. STS4: `Run > Run Configuration > Environment`).
    
5. Installa le dipendenze del frontend:
    
    ```
    cd visualizzazionePDF_frontend
    npm install
    ```
    
6. Installa le dipendenze Python:
    
    ```
    cd py_extraction
    pip install -r requirements.txt
    ```
    

### 3. Avvia i componenti

```
# Backend Spring Boot
./mvnw spring-boot:run

# Frontend React
cd visualizzazionePDF_frontend
npm run dev

# Server Flask
cd py_extraction
python pdf_extraction_service.py

# Invia i PDF da elaborare
python invio_pdf_a_flask.py
```

---

## Cosa accade una volta avviato il progetto

1. Flask legge i PDF dalla cartella `/pdf`, estrae i dati e li invia via HTTP al backend Spring Boot.
    
2. Spring Boot li salva su MongoDB.
    
3. I dati sono visibili nel frontend sotto forma di tabella.
    
4. È possibile modificarli tramite una modale. Le modifiche vengono salvate sia sul frontend che nel database.
    

---

## API disponibili

**URL Base**: `http://localhost:8080/api/v1`

|Metodo|Endpoint|Descrizione|
|---|---|---|
|GET|`/profiles`|Ottiene tutti i profili|
|GET|`/profiles/:id`|Ottiene un profilo per ID|
|POST|`/profiles`|Crea un nuovo profilo|
|PUT|`/profiles/:id`|Modifica un intero profilo|
|PATCH|`/profiles/:id`|Modifica un singolo campo|

> **Endpoint Flask (non usato ma funzionante)**  
> `POST http://127.0.0.1:5001/extract`  
> Permette a Flask di ricevere un PDF da analizzare.

> **Postman Collection**  

---

## Campi accettati nei profili

```
public class Profile {
  private String id;
  private String name;
  private String surname;
  private String codiceFiscale;
  private Date birthDate;
  private Integer age;
  private Integer height; // cm
  private Integer weight; // kg
  private String sex; // M, F o O
}
```

> Nessun campo è obbligatorio. Tuttavia, nome e cognome potrebbero essere resi required in futuro. Una possibile evoluzione prevede log automatici dei campi non estratti per facilitare la verifica manuale.

### Esempio di body POST

```
{
  "name": "Mario",
  "surname": "Rossi",
  "codiceFiscale": "RSSMRA80A01H501R",
  "birthDate": "1967-04-03",
  "sex": "M"
}
```

---

## Note tecniche

- Per evitare errori CORS:
    
    ```
    @CrossOrigin(origins = "*")
    ```
    
    _(Da limitare in produzione)_
    
- Il backend riceve dati da Flask via API e li salva nel DB.
    
- È possibile inviare PDF a Flask tramite API senza usare la cartella `/pdf`, utile per caricare file direttamente dal frontend (non ancora implementato).
    
- Il frontend React è basato su Vite per uno sviluppo più veloce.
    

---

## Considerazioni su miglioramenti futuri

### Utilizzo di spaCy per NER (Named Entity Recognition)

- **spaCy** è una libreria NLP Python in grado di estrarre entità da testi.
    
- Esempio:
    
    > _"Mario Rossi è nato il 4 luglio 1980 a Milano e lavora per Google"_
    
    spaCy può identificare:
    
    - `Mario Rossi` → PERSONA
        
    - `4 luglio 1980` → DATA
        
    - `Milano` → LUOGO
        
    - `Google` → ORGANIZZAZIONE
        
- Un modello NER sarebbe utile per rendere più flessibile l’estrazione dei dati da PDF non ancora esaminati o da strutture testuali diverse.
    

### Limiti attuali di spaCy (versione italiana `it_core_news_sm`)

- Non riconosce i codici fiscali
    
- A volte classifica erroneamente entità (es: "Auschwitz" come compagnia)
    
- Più lento delle regex (anche se comunque abbastanza veloce)
    

> Con abbastanza dati di addestramento, questi limiti possono essere superati. Per ora si è scelto un approccio a regex per semplicità ed efficacia.


