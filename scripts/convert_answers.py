import json

# Paths to input and output files
input_file = "D:/website/ExtractQuestions-1/data/answers.txt"
output_file = "D:/website/ExtractQuestions-1/data/answer_dict.txt"

# Function to convert answers string into a dictionary
def convert_to_dict(input_string):
    # Split the string into parts based on spaces
    parts = input_string.split()
    
    # Initialize an empty dictionary
    result_dict = {}
    
    # Process each part
    for i in range(0, len(parts), 2):
        # Extract question number and answer
        question_number = parts[i].strip('.')
        answer = parts[i + 1]
        
        # Add to dictionary
        result_dict[question_number] = answer
    
    return result_dict

# Read answers from the input file
with open(input_file, 'r', encoding='utf-8') as file:
    input_str = file.read().strip()

# Convert the input string into a dictionary
answers_dict = convert_to_dict(input_str)

# Write the dictionary to the output file in JSON format
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(answers_dict, file, indent=4)

print(f"Dictionary has been successfully written to {output_file}!")
