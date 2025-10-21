import kenlm

def test_perplexity(model_path, sentence):
    model = kenlm.Model(model_path)
    perplexity = model.perplexity(sentence)
    return perplexity

# Load isiZulu model
zulu_model = 'isiZuluLapaceModel.klm'

correct_sentence = "Lo mntwana uyahamba endlini kodwa akafuni ukudla"
wrecked_sentence = "Lo umntwana uyahmaba endlini kodwa akfuni ukudla"

# Compute Perplexity
print(f"Perplexity (correct sentence): {test_perplexity(zulu_model, correct_sentence)}")
print(f"Perplexity (wrecked sentence): {test_perplexity(zulu_model, wrecked_sentence)}")
