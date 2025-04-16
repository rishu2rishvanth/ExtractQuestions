import json
from pathlib import Path

# Step 1: Get the current directory (where this script is located)
base_dir = Path(__file__).resolve().parent
data_dir = base_dir / 'data'

# Step 2: Define file paths relative to the script
input_file = data_dir / 'answers.txt'
output_file = data_dir / 'answer_dict.txt'

# Function to replace ABCD to 0123
def replace_answers_with_numbers(answer):
    answer_map = {'A': '0', 'B': '1', 'C': '2', 'D': '3'}
    return answer_map.get(answer.upper(), answer)  # Default to the original if not A, B, C, or D

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
        
        # Replace the answer letter with a number
        answer = replace_answers_with_numbers(answer)

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
