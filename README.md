# Generisanje testnih slučajeva iz korisničkih priča

Automatizovani sistem za generisanje pozitivnih i negativnih testnih slučajeva iz korisničkih priča korišćenjem tehnika obrade prirodnog jezika i SpaCy biblioteke.

## 🌍 Opis projekta
Cilj ovog projekta je razvoj modela koji automatski generiše testne slučajeve na osnovu korisničkih priča. Korisničke priče se analiziraju pomoću NLP tehnika kako bi se izdvojile ključne komponente: uloga, radnja i cilj. Na osnovu tih komponenti kreiraju se pozitivni i negativni testovi.

## 📊 NLP tehnike koje se koriste
- **Tokenizacija**
- **Označavanje vrste riječi (PoS tagging)**
- **Parsiranje zavisnosti (Dependency parsing)**
- **Analiza sentimenta (za identifikaciju pozitivnih/negativnih izraza)**

Koristi se unaprijed trenirani SpaCy model `en_core_web_sm` za engleski jezik.

## 🔗 Zavisnosti

Instalacija potrebnih paketa:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Sadržaj `requirements.txt`:
```
spacy==3.7.2
pandas==2.2.2
```

## 📁 Struktura projekta
```
test-generation-nlp/
├── README.md                  # ovaj fajl
├── requirements.txt           # zavisnosti projekta
├── user_story_test_generator.py  # glavna skripta
├── data/
│   └── sample_user_stories.txt   # ulazne korisničke priče
├── output/
│   └── sample_results.txt     # generisani testovi i izvještaj
```

## ▶️ Pokretanje projekta
U fajlu `user_story_test_generator.py` potrebno je podesiti ulaznu i izlaznu putanju:
```python
pipeline = StoryTestPipeline(
    input_path="data/sample_user_stories.txt",
    output_path="output/Test_Case_Results.txt"
)
pipeline.run()
```

Pokretanje skripte:
```bash
python user_story_test_generator.py
```

## 📝 Primjer korisničke priče
```
As a manager, I want to understand my colleagues' progress, so that I can report our successes and failures.
```

## 🧪 Primjer generisanih testnih slučajeva
- **Pozitivni test:** Ensure that manager can understand my colleagues' progress.
- **Negativni test:** Verify system behavior when manager is unable to understand my colleagues' progress.

## 📑 Izvještaj o testiranju
| ID korisničke priče | Pozitivni testovi | Negativni testovi |
|---------------------|-------------------|-------------------|
| US-1                | 4                 | 4                 |

## 🧩 Detaljan opis rada funkcije `main()`

**Evo pregleda što razvijena funkcija zapravo radi:**

### Glavna funkcija `main()`:
Ova funkcija predstavlja centralno mjesto izvršavanja koda. Njena uloga je da:
- Učita korisničke priče iz fajla.
- Ekstrahuje ključne komponente iz priča (ulogu, akciju, cilj).
- Generiše test slučajeve na osnovu tih komponenti.
- Sačuva generisane rezultate u izlazni fajl.

### Varijable `file_path` i `output_file`:
- `file_path`: Putanja do tekstualnog fajla koji sadrži korisničke priče (npr. "User_Story.txt").
- `output_file`: Naziv fajla u koji će biti sačuvani rezultati (npr. "Test_Case_Results.txt").

### Funkcija `load_user_stories(file_path)`:
Ova funkcija čita korisničke priče iz fajla i vraća ih kao listu rečenica.

### Varijable `report_data` i `test_case_data`:
- `report_data`: Lista podataka za izvještaj po priči (ID, broj pozitivnih/negativnih testova).
- `test_case_data`: Detalji test slučajeva (ID, tekst priče, sadržaj testova).

### Petlja kroz korisničke priče:
- Uz pomoć `enumerate()` svaka priča dobija identifikator (npr. "US-1").
- Ispisuje se ID i sadržaj priče.

### Korišćenje SpaCy modela:
- `nlp(user_story)`: Parsira priču i priprema za ekstrakciju.

### Ekstrakcija komponenti:
- `extract_components(doc)`: Izdvaja `ulogu`, `akciju`, `cilj` iz rečenice.

### Generisanje testova:
- `generate_test_cases(role, action, goal)`: Kreira pozitivne i negativne testove.

### Pohrana podataka:
- Podaci o testovima i izvještaju čuvaju se u odgovarajuće liste.

### Funkcija `save_results_to_file(...)`:
- Rezultati se upisuju u tekstualni fajl (Test_Case_Results.txt).

### Izvršenje programa:
- Funkcija `main()` se poziva samo ako je skripta direktno pokrenuta (`if __name__ == "__main__":`).

**Zaključno:**
Ovaj kod koristi SpaCy-eve NLP tehnike za obradu korisničkih priča, izdvajanje ključnih komponenti i automatsko generisanje funkcionalnih testova. Time značajno unapređuje brzinu i konzistentnost QA procesa u razvoju softvera.

## ✍️ Autor
Ime i prezime autora: Marko Pribisalić
Kontakt: marko.pribisalic@gmail.com
