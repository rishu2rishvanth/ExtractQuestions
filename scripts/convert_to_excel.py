import subprocess
import pandas as pd
import re
import os
import json
from pathlib import Path

# Step 1: Get the current directory (where this script is located)
base_dir = Path(__file__).resolve().parent
data_dir = base_dir / 'data'

# Step 2: Define file paths relative to the script
input_file = data_dir / 'rawQuestions.txt'
output_file = data_dir / 'rawQuestions.xlsx'
answers_file = data_dir / 'answer_dict.txt'

# Step 3: Run convert_answers.py (assumed to be in the same directory)
subprocess.run(['python', str(base_dir / 'convert_answers.py')], check=True)

# Function to read correct answers from a JSON file
def read_correct_answers(file_path):
    correct_answers = {}
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                correct_answers = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error reading JSON file: {e}")
    else:
        print(f"Answers file does not exist or is empty: {file_path}")
    return correct_answers

# Function to parse the question text
def parse_questions(text):
    questions = []
    current_question = {}
    
    # Split text into lines
    lines = text.splitlines()
    
    # Regex patterns to identify questions and options
    question_pattern = re.compile(r'^\d+\. ')
    option_pattern = re.compile(r'\([A-D]\)')
    
    question_text = []
    options = []
    
    for line in lines:
        line = line.strip()
        
        # Check for question number
        if question_pattern.match(line):
            if current_question:
                # Assign the accumulated question text and options
                current_question['Question'] = " ".join(question_text).strip()
                # Join all options into a single line for proper assignment
                for i, option in enumerate(options):
                    current_question[f'Option {chr(65+i)}'] = option.strip()
                questions.append(current_question)
                current_question = {}
                question_text = []
                options = []
            
            # Start new question
            question_number = line.split('.')[0].strip()
            current_question['Question Number'] = question_number
            question_text = [line[len(question_number) + 1:].strip()]
        
        # Check for options on the same line
        elif option_pattern.search(line):
            # Extract options
            parts = re.split(r'\s+(?=\([A-D]\))', line)
            for part in parts:
                match = re.match(r'\(([A-D])\)\s*(.*)', part)
                if match:
                    option_key = 'Option ' + match.group(1)
                    option_value = match.group(2).strip()
                    options.append(option_value)
        
        else:
            # Collect the question text
            question_text.append(line)
    
    # Handle any remaining question at the end of the text
    if current_question:
        current_question['Question'] = " ".join(question_text).strip()
        # Join all options into a single line for proper assignment
        for i, option in enumerate(options):
            current_question[f'Option {chr(65+i)}'] = option.strip()
        questions.append(current_question)
    
    return questions

# Read the correct answers from the file
correct_answers = read_correct_answers(answers_file)

# Check if the input file exists and is not empty
if os.path.exists(input_file) and os.path.getsize(input_file) > 0:
    try:
        # Read the input text file
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Parse the questions
        questions = parse_questions(text)
        
        # Convert the questions list into a DataFrame
        df = pd.DataFrame(questions)
        
        # Add the correct answers to the DataFrame
        df['Correct Answer'] = df['Question Number'].map(correct_answers)
        
        # Reorder the columns as specified
        df = df[['Question Number', 'Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Answer']]
        
        # Write the DataFrame to an Excel file
        df.to_excel(output_file, index=False)

        print("Questions and options have been successfully written to Excel!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print(f"Input file does not exist or is empty: {input_file}")
