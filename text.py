import random

def generate_custom_wordlist(input_file, output_file, output_count=2048, min_word_length=3, max_word_length=8):
    # Load the words from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        words = [word.strip() for word in file.readlines()]
    
    # Filter words based on the length constraints
    filtered_words = [word for word in words if min_word_length <= len(word) <= max_word_length]
    
    # Ensure there are enough unique words to choose from
    if len(filtered_words) < output_count:
        raise ValueError("Not enough words to generate the required wordlist.")
    
    # Randomly sample the required number of words without repetition
    wordlist = random.sample(filtered_words, output_count)
    
    # Write the generated wordlist to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(wordlist))
    
    return output_file

# File paths
input_file = 'wordlist.txt'
output_file = 'out_wordlist.txt'

# Generate the wordlist
generate_custom_wordlist(input_file, output_file)
