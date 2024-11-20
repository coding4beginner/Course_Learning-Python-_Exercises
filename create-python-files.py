import os

# Define states for the FSM
class State:
    IDLE = "IDLE"
    QUESTION_START = "QUESTION_START"
    QUESTION_BODY = "QUESTION_BODY"
    HINTS = "HINTS"
    SOLUTION = "SOLUTION"
    SOLUTION_IN_CODE = "SOLUTION IN CODE"
    

def process_markdown_with_fsm(markdown_file):
    current_state = State.IDLE
    question_number = None
    question_text = ""
    solution_code = ""

    with open(markdown_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("### Question"):
            current_state = State.QUESTION_START
            question_number = line.strip().split(" ")[2]  # Extract the question number
            question_text = ""
            solution_code = ""
        elif line.startswith("Question:"):
            current_state = State.QUESTION_BODY
        elif line.startswith("Hints:"):
            current_state = State.HINTS
        elif line.startswith("Solution:"):
            current_state = State.SOLUTION
        elif line.startswith("```") and current_state == State.SOLUTION:
            current_state = State.SOLUTION_IN_CODE
        elif line.startswith("```") and current_state == State.SOLUTION_IN_CODE:
            current_state = State.IDLE

            # Save the question and solution to respective files
            exercise_file = f"exercises/{question_number.zfill(2)}.md"
            solution_file = f"solutions/{question_number.zfill(2)}.py"

            with open(exercise_file, "w") as ex_file:
                ex_file.write(f"# Exercise {question_number}\n")
                ex_file.write(f"# {question_text}\n")
                ex_file.write("\n# Write your solution below:\n")

            with open(solution_file, "w") as sol_file:
                sol_file.write(f"# Solution {question_number}\n")
                sol_file.write(solution_code + "\n")

            print(f"Created: {exercise_file} and {solution_file}")
        elif (line == "# Write your solution below:"):
            pass
        else:
            # Handle content for each state
            if current_state in [ State.QUESTION_BODY, State.HINTS ]:
                question_text += line

            elif current_state == State.SOLUTION_IN_CODE:
                solution_code += line

# Example usage
markdown_file_path = "100+ Python challenging programming exercises.md"  # Replace with your actual file path
if os.path.exists(markdown_file_path):
    process_markdown_with_fsm(markdown_file_path)
else:
    print(f"File not found: {markdown_file_path}")
