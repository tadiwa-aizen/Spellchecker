import re

def process_text_file(input_file, output_file):
    unique_words = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            for word in words:
                # Clean punctuation
                cleaned_word = re.sub(r'[^\w\s]', '', word)
                # Skip words with numbers
                if any(char.isdigit() for char in cleaned_word):
                    continue
                if cleaned_word and cleaned_word not in unique_words:
                    unique_words.add(cleaned_word)

    with open(output_file, 'w', encoding='utf-8') as f:
        for word in sorted(unique_words):
            spaced_word = ' '.join(list(word))
            f.write(spaced_word + '\n')

# Example usage
process_text_file('siSwatiCorpus.txt', 'siSwatiUCorpus.txt')
