import csv  # This brings in Python's built-in CSV tools

# Ask the user to type a question and an answer
question = input("Enter the question asked: ")
ai_answer = input("Enter the AI's answer: ")

# Ask the user to enter scores
accuracy_score = int(input("Enter accuracy score (1-5): "))
relevance_score = int(input("Enter relevance score (1-5): "))
clarity_score = int(input("Enter clarity score (1-5): "))
instruction_following_score = int(input("Enter instruction following score (1-5): "))

# Calculate the total and average score
total_score = accuracy_score + relevance_score + clarity_score + instruction_following_score
average_score = total_score / 4

# Print a neat summary report
print("\n=== EVALUATION REPORT ===")
print("Question:", question)
print("AI Answer:", ai_answer)
print("Average Score:", average_score)
print("=========================")

# --- NEW: Save this evaluation to a CSV file ---
# 'a' means "append" (add new rows to the file without deleting old ones)
with open("eval_reports.csv", mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the data as a row in our CSV spreadsheet
    writer.writerow([question, ai_answer, accuracy_score, relevance_score, clarity_score, instruction_following_score, average_score])

print("\n[Success! Evaluation saved to eval_reports.csv]")