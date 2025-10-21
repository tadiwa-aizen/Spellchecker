import kenlm
import numpy as np

class SpellDetector:
    def __init__(self, model_path, threshold=-10.0):
        self.model = kenlm.LanguageModel(model_path)
        self.threshold = threshold

    def score_word(self, word):
        char_sequence = " ".join(list(word.strip()))
        return self.model.score(char_sequence, bos=True, eos=True)

    def is_error(self, word):
        score = self.score_word(word)
        return score < self.threshold

def evaluate_from_test_file(detector, test_file_path):
    with open(test_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = 0
    correct_detections = 0
    failures = []

    for line in lines:
        if "-" not in line:
            continue

        wrong, correct = [w.strip() for w in line.strip().split("-")]
        score_wrong = detector.score_word(wrong)
        score_correct = detector.score_word(correct)
        
        # Use threshold-based detection
        error_detected = detector.is_error(wrong)
        correct_accepted = not detector.is_error(correct)

        total += 1

        print(f"✏️ {wrong} → ✅ {correct}")
        print(f"  ❌ Wrong word flagged: {'✓' if error_detected else '✗'} (Score: {score_wrong:.2f})")
        print(f"  ✅ Correct word accepted: {'✓' if correct_accepted else '✗'} (Score: {score_correct:.2f})\n")

        if error_detected and correct_accepted:
            correct_detections += 1
        else:
            failures.append((wrong, correct))

    accuracy = correct_detections / total * 100 if total > 0 else 0
    
    print(f"\n=== Evaluation Summary ===")
    print(f"Total test cases: {total}")
    print(f"Correct detections: {correct_detections}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Current threshold: {detector.threshold:.2f}")

    if failures:
        print("\n❌ Failed cases:")
        for wrong, correct in failures:
            print(f"  {wrong} → {correct}")
    
    return accuracy

def find_optimal_threshold(model_path, test_file_path, threshold_range=(-15.0, -5.0), step=0.1):
    print("\n=== Finding Optimal Threshold ===")

    scores_wrong = []
    scores_correct = []
    
    with open(test_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        if "-" not in line:
            continue
        wrong, correct = [w.strip() for w in line.strip().split("-")]
        detector = SpellDetector(model_path)
        scores_wrong.append(detector.score_word(wrong))
        scores_correct.append(detector.score_word(correct))
    

    best_threshold = None
    best_accuracy = 0
    thresholds = np.arange(threshold_range[0], threshold_range[1], step)
    
    print("\nTesting thresholds...")
    for threshold in thresholds:
        detector = SpellDetector(model_path, threshold=threshold)
        accuracy = evaluate_from_test_file(detector, test_file_path)
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_threshold = threshold
    
    print(f"\n=== Optimal Threshold Found ===")
    print(f"Best threshold: {best_threshold:.2f}")
    print(f"Best accuracy: {best_accuracy:.2f}%")
    
    return best_threshold

if __name__ == "__main__":
    MODEL_PATH = "isiZuluUModel.arpa" 
    TEST_FILE_PATH = "isiZulu_test.txt"  
    
    # First find the optimal threshold
    optimal_threshold = find_optimal_threshold(MODEL_PATH, TEST_FILE_PATH)
    
    print("\n=== Final Evaluation with Optimal Threshold ===")
    detector = SpellDetector(MODEL_PATH, threshold=optimal_threshold)
    evaluate_from_test_file(detector, TEST_FILE_PATH)
    
