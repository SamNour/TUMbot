import csv
import pprint
subject =[]
questions = []
answers = []
full_text = []
with open('questions_answers.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    
    for row in reader:
        subject.append(f"\"subject\": \"{row[0]}\",")
        questions.append(f"\"question\": \"{row[1]}\",")
        answers.append(f"\"answer\": \"{row[2]}\"")

for i in range(len(subject)):
    full_text.append(f"{{{subject[i]} {questions[i]} {answers[i]}}}")

lst = open("output", "r").read().replace("', '", "\n")
print(lst)