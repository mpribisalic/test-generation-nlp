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

## ✍️ Autor
Ime i prezime autora: Marko Pribisalić
Kontakt: marko.pribisalic@gmail.com
