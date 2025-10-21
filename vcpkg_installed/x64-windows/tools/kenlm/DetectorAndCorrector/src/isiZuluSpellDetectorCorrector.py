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
        
        # Compile Java files if needed
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

    def detect_error(self, word):
        score = self.model.score(word, bos=True, eos=True)
        print(f"Word: {word}, Score: {score}, Threshold: {self.threshold}")
        return score < self.threshold

    def get_corrections(self, word):
        try:
            print(f"Attempting to get corrections for: {word}")
            # Run Java with correct classpath
            result = subprocess.run(
                ['javac', 'SpellCorrectorMain.java'],  # Compile the new class
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__)
            )
            
            if result.returncode != 0:
                print(f"Compilation Error: {result.stderr}")
                return None
                
            result = subprocess.run(
                ['java', 
                 '-cp', '.',  # Use current directory for classpath
                 'SpellCorrectorMain'],
                input=word,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__)  # Set working directory to script location
            )
            
            print(f"Java return code: {result.returncode}")
            print(f"Java stdout: {result.stdout}")
            print(f"Java stderr: {result.stderr}")
            
            if result.returncode != 0:
                print(f"Java Error: {result.stderr}")
                return None
                
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

def process_text(text, model_path="isiZuluModel.arpa"):
    # Convert model path to absolute
    abs_model_path = os.path.abspath(model_path)
    
    detector = SpellErrorDetector(abs_model_path, threshold=-5)
    words = text.split()
    
    for word in words:
        if detector.detect_error(word):
            print(f"\nFound potential error: {word}")
            corrections = detector.get_corrections(word)
            
            if corrections:
                print(f"Most likely correction: {corrections['most_likely']}")
                print("Other possible corrections:")
                # Show only top 3 corrections
                for i, candidate in enumerate(corrections['candidates'][:3], 1):
                    print(f"{i}. {candidate}")
                return corrections
            else:
                print("No corrections found")
                return None
        return None

if __name__ == "__main__":
    # Test cases with expected corrections
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
    model_path = os.path.join(os.path.dirname(__file__), 'kenlm', 'isiZuluModel.arpa')
    
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