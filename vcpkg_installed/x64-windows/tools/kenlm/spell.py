import kenlm


class SpellErrorDetector:
    def __init__(self, model_path, threshold=-10):
        self.model = kenlm.LanguageModel(model_path)
        self.threshold = threshold

    def detect_error(self, word):
        score = self.model.score(word, bos=True, eos=True)
        return score < self.threshold


if __name__ == "__main__":
    MODEL_PATH = "isiZuluModel.arpa"
    THRESHOLD = -10

    detector = SpellErrorDetector(MODEL_PATH, THRESHOLD)

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
        ("oykusabalalisa", "yokusabalalisa"),
    ]

    correct_detections = 0
    total_cases = len(test_cases)

    for wrong, correct in test_cases:
        wrong_score = detector.model.score(wrong, bos=True, eos=True)
        correct_score = detector.model.score(correct, bos=True, eos=True)

        print(f"Pair: '{wrong}' vs '{correct}'")
        print(f"  Wrong word score:   {wrong_score:.2f}")
        print(f"  Correct word score: {correct_score:.2f}")
        detected = wrong_score < correct_score
        print(f"  Decision: {'PASS (wrong flagged)' if detected else 'FAIL (not flagged)'}\n")

        if detected:
            correct_detections += 1

    print("\n=== Evaluation Summary ===")
    print(f"Total test cases: {total_cases}")
    print(f"Correct detections: {correct_detections}")
    print(f"Accuracy: {correct_detections / total_cases * 100:.2f}%")

