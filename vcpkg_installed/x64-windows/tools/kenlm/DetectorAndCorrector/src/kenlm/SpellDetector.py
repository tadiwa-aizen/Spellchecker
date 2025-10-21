import kenlm

class SpellDetector:
    def __init__(self, model_path):
        self.model = kenlm.LanguageModel(model_path)

    def score_word(self, word):
        char_sequence = " ".join(list(word.strip()))
        return self.model.score(char_sequence, bos=True, eos=True)
    
    #def check
    # make it rely on a threshold you can yet, expriement to find the correct value
    # tkae the 
    # get the wrcker from fridas code, tmdo th wrecking....
    # he wants to covnert to a jar file....
    # but look at the corrector and see if tis possible
    

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

        #error_detected = score_wrong < score_correct  # Lower score = less likely = error
        
        margin = 1.5
        error_detected = (score_correct - score_wrong) > margin

        total += 1

        print(f"✏️ {wrong} → ✅ {correct}")
        print(f"  ❌ Wrong word flagged: {'✓' if error_detected else '✗'} (Score: {score_wrong:.2f})")
        print(f"  ✅ Correct word accepted: {'✓' if score_correct >= score_wrong else '✗'} (Score: {score_correct:.2f})\n")

        if error_detected:
            correct_detections += 1
        else:
            failures.append((wrong, correct))

    print(f"\n=== Evaluation Summary ===")
    print(f"Total test cases: {total}")
    print(f"Correct detections: {correct_detections}")
    print(f"Accuracy: {correct_detections / total * 100:.2f}%")

    if failures:
        print("\n❌ Failed cases:")
        for wrong, correct in failures:
            print(f"  {wrong} → {correct}")

if __name__ == "__main__":
    MODEL_PATH = "isiZuluUModel.arpa"     # or isiZuluModel.bin
    TEST_FILE_PATH = "isiZulu_test.txt"           # file with "wrong - correct" pairs

    detector = SpellDetector(MODEL_PATH)
    evaluate_from_test_file(detector, TEST_FILE_PATH)
