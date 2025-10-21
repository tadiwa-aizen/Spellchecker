import os
import sys
import kenlm


LANGS = [
    ("isiZulu", "isiZuluUModel.arpa", "isiZulu_test.txt"),
    ("isiXhosa", "isiXhosaUModel.arpa", "isiXhosa_test.txt"),
    ("isiNdebele", "isiNdebeleUModel.arpa", "isiNdebele_test.txt"),
    ("siSwati", "siSwatiUModel.arpa", "siSwati_test.txt"),
]


def char_score(model: kenlm.LanguageModel, word: str) -> float:
    seq = " ".join(list(word.strip()))
    return model.score(seq, bos=True, eos=True)


def run_language(tools_dir: str, name: str, model_file: str, test_file: str, margin: float = 1.5):
    model_path = os.path.join(tools_dir, model_file)
    test_path = os.path.join(tools_dir, test_file)

    if not os.path.exists(model_path):
        print(f"[WARN] {name}: Missing model {model_file}")
        return None
    if not os.path.exists(test_path):
        print(f"[WARN] {name}: Missing test file {test_file}")
        return None

    lm = kenlm.LanguageModel(model_path)

    total = 0
    correct = 0
    with open(test_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '-' not in line:
                continue
            wrong, correct_word = [w.strip() for w in line.split('-', 1)]
            s_wrong = char_score(lm, wrong)
            s_correct = char_score(lm, correct_word)
            if (s_correct - s_wrong) > margin:
                correct += 1
            total += 1

    acc = (correct / total * 100.0) if total else 0.0
    print(f"{name}: {correct}/{total} = {acc:.2f}%")
    return name, correct, total, acc


if __name__ == "__main__":
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    results = []
    print("=== Spell Detection Accuracy (Character-level LMs) ===")
    for name, model, test in LANGS:
        res = run_language(tools_dir, name, model, test)
        if res:
            results.append(res)

    if results:
        total_correct = sum(r[1] for r in results)
        total_total = sum(r[2] for r in results)
        overall = (total_correct / total_total * 100.0) if total_total else 0.0
        print(f"Overall: {total_correct}/{total_total} = {overall:.2f}%")
    else:
        print("No results to report.")

