import re

def clean_text_for_kenlm(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        sentence = []  # List to accumulate words for a sentence
        
        for line in infile:
            line = line.strip()
            
            # Detecting new sentence start
            if line.startswith("<LINE"):  
                # Write the previous sentence (if any)
                if sentence:
                    outfile.write(" ".join(sentence) + " .\n")
                    sentence = []  # Reset for the new sentence
                continue  # Skip writing "<LINE X>"

            # Extract and clean words
            words = line.split("\t")  # Words are tab-separated
            if words:
                word = words[0]  # Extract the main word (ignoring annotations)
                word = re.sub(r"\[.*?\]", "", word)  # Remove anything inside square brackets
                word = re.sub(r"-\S+", "", word)  # Remove hyphen-separated suffixes
                word = word.strip()
                
                if word:
                    sentence.append(word)

        # Write the last sentence if any
        if sentence:
            outfile.write(" ".join(sentence) + " .\n")

# Example Usage
input_path = "siSwatiRawCorpus.txt"      # Change this to your input file
output_path = "siSwatiCorpus.txt"  # Output file for KenLM
clean_text_for_kenlm(input_path, output_path)
