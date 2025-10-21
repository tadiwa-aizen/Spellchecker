import kenlm
import subprocess
import json
import os

class SpellErrorDetector:
    def __init__(self, model_path, threshold=-10):
        # Convert to absolute path
        self.model_path = os.path.abspath(model_path)
        self.model = kenlm.LanguageModel(self.model_path)
        self.threshold = threshold
        
        # Set up Java classpath
        self.java_classpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        self._compile_java()

    def _compile_java(self):
        """Compile Java files if needed"""
        java_files = [
            'ErrorCorrector.java',
            'DamerauLevenshtein.java',
            'BinarySearch.java',
            'Probabilities.java',
            'TriFreq.java',
            'TriNext.java'
        ]
        
        # Check if compilation is needed
        need_compile = False
        for file in java_files:
            java_path = os.path.join(self.java_classpath, 'src', file)
            class_path = os.path.join(self.java_classpath, 'src', file.replace('.java', '.class'))
            if not os.path.exists(class_path) or \
               os.path.getmtime(java_path) > os.path.getmtime(class_path):
                need_compile = True
                break
        
        if need_compile:
            print("Compiling Java files...")
            compile_cmd = ['javac', '-d', os.path.join(self.java_classpath, 'src')]
            compile_cmd.extend([os.path.join(self.java_classpath, 'src', f) for f in java_files])
            subprocess.run(compile_cmd, check=True)

    def score_word(self, word):
        """Score a word by breaking it into individual characters"""
        char_sequence = " ".join(list(word.strip()))
        return self.model.score(char_sequence, bos=True, eos=True)

    def detect_error(self, word):
        """Detect if a word is likely incorrect based on its score"""
        score = self.score_word(word)
        print(f"Word: {word}, Score: {score}, Threshold: {self.threshold}")
        return score < self.threshold

    def get_corrections(self, word):
        try:
            print(f"Attempting to get corrections for: {word}")

            result = subprocess.run(
                ['javac', 'SpellCorrectorMain.java'], 
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__)
            )
            
            if result.returncode != 0:
                print(f"Compilation Error: {result.stderr}")
                return None
                
            result = subprocess.run(
                ['java', 
                 '-cp', '.', 
                 'SpellCorrectorMain'],
                input=word,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__)  
            )
                
            # Find the JSON array in the output
            json_start = result.stdout.find('[')
            json_end = result.stdout.rfind(']') + 1
            if json_start == -1 or json_end == 0:
                print("No JSON array found in output")
                return None
                
            json_str = result.stdout[json_start:json_end]
            corrections = json.loads(json_str)
            
            if corrections:
                return {
                    'most_likely': corrections[0],
                    'candidates': corrections
                }
            return None
            
        except Exception as e:
            print(f"Error getting corrections: {e}")
            return None

def process_text(text, model_path="isiZuluUModel.arpa"):

    abs_model_path = os.path.abspath(model_path)
    
    detector = SpellErrorDetector(abs_model_path, threshold=-11)
    words = text.split()
    
    for word in words:

        score = detector.score_word(word)
        is_incorrect = detector.detect_error(word)
        
        print(f"\nChecking word: {word}")
        print(f"Score: {score:.2f}")
        print(f"Threshold: {detector.threshold}")
        print(f"Status: {'Incorrect' if is_incorrect else 'Correct'} spelling")
        
        if is_incorrect:
            print(f"\nFound incorrect spelling: {word}")
            corrections = detector.get_corrections(word)
            
            if corrections:
                print(f"Most likely correction: {corrections['most_likely']}")
                print("Other possible corrections:")

                for i, candidate in enumerate(corrections['candidates'][:3], 1):
                    print(f"{i}. {candidate}")
                return corrections
            else:
                print("No corrections found")
                return None
        else:
            print(f"Word '{word}' is correctly spelled")
            return None

if __name__ == "__main__":
    test_cases = [
        ("babeqgokise", "babegqokise"),
        ("wayesebezna", "wayesebenza"),
        ("yokuhkulunywayo", "yokukhulunywayo"),
        ("izizahtu", "izizathu"),
        ("abasesthenziswe", "abasetshenziswe"),
        ("zawkaZulu", "zakwaZulu"),
        ("suebuyela", "usebuyela"),
        ("ayyiqinisekisa", "yayiqinisekisa"),
        ("yivmelaphi", "yimvelaphi"),
        ("esalihbuqa", "esalibhuqa"),
        ("aWmema", "Wamema"),
        ("yayilugnile", "yayilungile"),
        ("eselhubuka", "esehlubuka"),
        ("abezohtakatha", "abezothakatha"),
        ("yadniswe", "yandiswe"),
        ("alehte", "alethe"),
        ("ayqoma", "yaqoma"),
        ("azzivele", "zazivele"),
        ("wahkulelwa", "wakhulelwa"),
        ("oykusabalalisa", "yokusabalalisa")
        
    ]
    
    # Get the absolute path to the model
    model_path = os.path.join(os.path.dirname(__file__), 'kenlm', 'isiZuluUModel.arpa')
    
    print("\nRunning spell checker on test cases:")
    print("=" * 80)
    
    total_cases = len(test_cases)
    successful_cases = 0
    
    for incorrect, expected in test_cases:
        print(f"\nChecking: {incorrect}")
        print(f"Expected correction: {expected}")
        corrections = process_text(incorrect, model_path)
        
        if corrections:
            most_likely = corrections['most_likely']
            print(f"\nMost likely correction: {most_likely}")
            print("Other possible corrections:")
            # Show only top 3 corrections
            for i, correction in enumerate(corrections['candidates'][:3], 1):
                print(f"{i}. {correction}")
            
            if most_likely == expected:
                print(f"\n✓ Most likely correction '{most_likely}' matches expected '{expected}'")
                successful_cases += 1
            else:
                print(f"\n✗ Most likely correction '{most_likely}' does not match expected '{expected}'")
        else:
            print("No corrections found")
    
    # Calculate and display success rate
    success_rate = (successful_cases / total_cases) * 100
    print("\n" + "=" * 80)
    print(f"Spell Checker Performance Summary:")
    print(f"Total test cases: {total_cases}")
    print(f"Successful first-choice corrections: {successful_cases}")
    print(f"Success rate: {success_rate:.2f}%")