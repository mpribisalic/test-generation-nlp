import spacy
import pandas as pd
import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict

# Postavljanje logovanja za bolje pracenje toka izvrsavanja
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserStoryProcessor:
    """
    Klasa za obradu korisničkih priča: učitavanje, parsiranje i izdvajanje komponenti.
    """
    def __init__(self, model: str = "en_core_web_sm"):
        # Učitavanje SpaCy NLP modela
        self.nlp = spacy.load(model)

    def load_stories(self, path: Path) -> List[str]:
        """
        Učitavanje korisničkih priča iz tekstualnog fajla.
        """
        if not path.exists():
            logging.error(f"File not found: {path}")
            return []
        stories = path.read_text(encoding='utf-8').splitlines()
        return [s.strip() for s in stories if s.strip()]

    def parse_story(self, story: str) -> spacy.tokens.Doc:
        """
        Parsiranje korisničke priče pomoću NLP modela.
        """
        return self.nlp(story)

    def extract_components(self, doc: spacy.tokens.Doc) -> Tuple[Optional[str], str, str]:
        """
        Izdvajanje uloge (role), akcije (action) i cilja (goal) iz korisničke priče.
        """
        role, action, goal = None, [], []

        for token in doc:
            if token.dep_ == 'nsubj' and not role:
                role = token.text
            if token.dep_ == 'xcomp':
                action.extend([t.text for t in token.subtree if t.dep_ != 'punct'])
            if token.text in {"so", "that", "in", "order"}:
                goal = [t.text for t in doc[token.i+2:]]
                break

        return role, ' '.join(action), ' '.join(goal)

class TestCaseGenerator:
    """
    Klasa za generisanje pozitivnih i negativnih testnih slučajeva na osnovu komponenata.
    """
    def generate(self, role: Optional[str], action: str, goal: str) -> Tuple[List[str], List[str]]:
        pos, neg = [], []

        if role and action and goal:
            pos.extend([
                f"Ensure that {role} can {action}.",
                f"Validate that {role} can achieve {goal}.",
                f"Verify that {role} has access to features needed for {goal}.",
                f"Check that {action} leads to {goal} for {role}."
            ])
            neg.extend([
                f"Verify system behavior when {role} is unable to {action}.",
                f"Ensure system handles missing or incorrect data when {role} tries to {action}.",
                f"Verify that the system prevents {role} from accessing unauthorized features related to {goal}.",
                f"Check that failure in {action} does not result in inconsistent or incomplete data for {goal}."
            ])
        return pos, neg

class ReportManager:
    """
    Klasa za pravljenje i čuvanje izveštaja o generisanim testovima.
    """
    def __init__(self):
        self.data: List[Dict] = []

    def add_entry(self, uid: str, story: str, pos: List[str], neg: List[str]) -> None:
        self.data.append({
            "User Story ID": uid,
            "User Story": story,
            "Positive Test Cases": len(pos),
            "Negative Test Cases": len(neg)
        })

    def save(self, path: Path, cases: List[Dict]) -> None:
        """
        Čuva generisane testove i izveštaj u tekstualni fajl.
        """
        with path.open('w', encoding='utf-8') as f:
            for item in cases:
                f.write(f"User Story {item['User Story ID']}:\n")
                f.write(f"{item['User Story']}\n")
                f.write("Positive Test Cases:\n")
                for test in item['Positive Test Cases']:
                    f.write(f"- {test}\n")
                f.write("Negative Test Cases:\n")
                for test in item['Negative Test Cases']:
                    f.write(f"- {test}\n")
                f.write("\n")

            f.write("Test Case Generation Report:\n")
            df = pd.DataFrame(self.data)
            f.write(df.to_string(index=False))
            f.write("\n")

class StoryTestPipeline:
    """
    Glavna klasa za pokretanje celokupnog procesa: učitavanje, obrada, generisanje i čuvanje.
    """
    def __init__(self, input_path: str, output_path: str):
        # GENERIČKI PATH - OVDE POSTAVITI SVOJU PUTANJU DO ULAZNOG I IZLAZNOG FAJLA
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.processor = UserStoryProcessor()
        self.generator = TestCaseGenerator()
        self.report = ReportManager()
        self.results: List[Dict] = []

    def run(self) -> None:
        """
        Izvršava obradu svih koraka za sve korisničke priče.
        """
        stories = self.processor.load_stories(self.input_path)
        if not stories:
            logging.warning("No stories loaded.")
            return

        logging.info(f"Processing {len(stories)} user stories...")
        for idx, story in enumerate(stories):
            uid = f"US-{idx+1}"
            doc = self.processor.parse_story(story)
            role, action, goal = self.processor.extract_components(doc)
            pos, neg = self.generator.generate(role, action, goal)

            self.results.append({
                "User Story ID": uid,
                "User Story": story,
                "Positive Test Cases": pos,
                "Negative Test Cases": neg
            })

            self.report.add_entry(uid, story, pos, neg)

        self.report.save(self.output_path, self.results)
        logging.info(f"Results saved to {self.output_path}")

if __name__ == "__main__":
    # OVDE UNESI SVOJE PUTANJE DO FAJLA SA KORISNIČKIM PRIČAMA I IZLAZNOG REZULTATA
    pipeline = StoryTestPipeline(
        input_path="path/to/your/input/file.txt",  # <-- postavi stvarnu putanju do ulaznog fajla
        output_path="path/to/save/output_results.txt"  # <-- postavi željenu putanju za izlaz
    )
    pipeline.run()
	