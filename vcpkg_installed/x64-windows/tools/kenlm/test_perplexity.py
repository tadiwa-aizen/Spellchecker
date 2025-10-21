import os
import subprocess
import kenlm


def ensure_binary_from_arpa(arpa_path):
    base, _ = os.path.splitext(arpa_path)
    bin_path = base + ".binary"
    if os.path.exists(bin_path):
        return bin_path

    tools_dir = os.path.dirname(os.path.abspath(__file__))
    build_binary = os.path.join(tools_dir, "build_binary.exe")
    if os.path.exists(build_binary):
        try:
            subprocess.check_call([build_binary, "-s", arpa_path, bin_path])
            return bin_path if os.path.exists(bin_path) else arpa_path
        except Exception as e:
            print(f"Warning: build_binary failed: {e}")
            return arpa_path
    return arpa_path


def test_perplexity(model_path, sentence):
    # Prefer binary for kenlm.Model; fall back to ARPA if needed
    model_try = ensure_binary_from_arpa(model_path)
    try:
        m = kenlm.Model(model_try)
        return m.perplexity(sentence)
    except Exception as e:
        # Fallback: use LanguageModel and compare scores if perplexity isn't available
        print(f"Info: Falling back to LanguageModel due to: {e}")
        lm = kenlm.LanguageModel(model_path)
        # Perplexity isn't directly available; return negative total score as a proxy (for comparison only)
        return -lm.score(sentence, bos=True, eos=True)


if __name__ == "__main__":
    # Use an existing isiZulu ARPA model located in this tools folder
    zulu_model = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'isiZuluModel.arpa')

    correct_sentence = "Lo mntwana uyahamba endlini kodwa akafuni ukudla"
    wrecked_sentence = "Lo umntwana uyahmaba endlini kodwa akfuni ukudla"

    p_correct = test_perplexity(zulu_model, correct_sentence)
    p_wrecked = test_perplexity(zulu_model, wrecked_sentence)

    print("=== Zulu Sentence Perplexity Check ===")
    print(f"Correct sentence perplexity (lower is better): {p_correct}")
    print(f"Wrecked sentence perplexity (lower is better): {p_wrecked}")
    if p_correct < p_wrecked:
        print("Result: PASS — Correct sentence is more probable.")
    else:
        print("Result: WARN — Model did not prefer the correct sentence.")

