from openai import OpenAI
import os
from flask import Flask, render_template, url_for, request, redirect

# Read the API key from the text file
api_key_file = os.path.join(os.path.dirname(__file__), 'api_key.txt')
with open(api_key_file, 'r') as f:
    OPENAI_API_KEY = f.read().strip()

client = OpenAI(api_key=OPENAI_API_KEY)


# Function to ask the user a trivia topic
topic = ""
def ask_user_trivia_topic():
    # Prompt the AI to ask the user a trivia topic
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Adjust the model as needed
        prompt="Ask the user to choose a trivia topic. Speak like a tv show host.",
        max_tokens=100,
        temperature=0.5
    )

    return response.choices[0].text.strip()


# Function to ask the user a trivia question
def ask_user_trivia_question(user_topic):
    # Prompt the AI to ask the user a trivia question
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Adjust the model as needed
        prompt=f"Ask the user a random trivia question about this topic: {user_topic}. Speak like a tv show host. Don't give the answer.",
        max_tokens=100,
        temperature=0.5
    )

    return response.choices[0].text.strip()


# Function to check user's answer
def check_answer(user_answer, ai_question):
    # Prompt the AI to generate the correct answer to the trivia question
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Adjust the model as needed
        prompt=f"Tell the user if his answer ({user_answer}) is correct for this question: {ai_question}. Analyse the content of the answer. The answer is still correct even if mispelled or in a sentence. If the answer is incorrect, give him the right answer and a interesting information related to the answer.",
        max_tokens=100,
        temperature=0.5
    )

    return response.choices[0].text.strip()  # Return the response text


app = Flask(__name__)

# Page asks the user to enter a topic
state = 0
@app.route('/')
def index():
    topic = ask_user_trivia_topic()
    return render_template("index.html", ai_topic=topic)

# Page asks the user to answer a question
@app.route('/question', methods=['POST'])
def play():
    topic_input = request.form['user_topic']
    question = ask_user_trivia_question(topic_input)
    return render_template('question.html', ai_question=question)

# Page shows the user the answer
@app.route('/result', methods=['POST'])
def result():
    answer = request.form['user_answer']
    question = request.form['question']
    response = check_answer(answer, question)
    return render_template('result.html', ai_response=response)

if __name__ == "__main__":
    app.run(debug=True)








