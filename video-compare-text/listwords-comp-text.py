from difflib import SequenceMatcher

def compare_text_files(file1, file2):
    # Read the contents of the first file
    with open(file1, 'r') as f1:
        text1 = f1.read()

    # Read the contents of the second file
    with open(file2, 'r') as f2:
        text2 = f2.read()

    # Split the texts into words
    words1 = text1.split()
    words2 = text2.split()

    # Find differing words
    differing_words = set(words1) ^ set(words2)

    # Save the differing words to a text file
    with open('differing_words.txt', 'w') as result_file:
        result_file.write('Differing words:\n')
        for word in differing_words:
            result_file.write('{}\n'.format(word))

    print('Differing words saved to differing_words.txt')

# Provide the paths to the two text files
file1_path = r'E:\Speechpy\simcomp-1\transcriptions\P-1463-71759_Trim.txt'
file2_path = r'E:\Speechpy\simcomp-1\transcriptions\P-1463-71760_Trim.txt'

# Compare the text files and save the differing words
compare_text_files(file1_path, file2_path)
