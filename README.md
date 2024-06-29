# Quizzler App

This is a quiz application built with Python that fetches questions from the Open Trivia Database and presents them in a GUI. The application uses the `requests` library to get quiz data, the `tkinter` library for the GUI, and employs object-oriented programming principles.

## Files Overview

1. **main.py**:
    - The entry point of the application. It fetches quiz questions from the Open Trivia Database and initializes the quiz.

2. **question_model.py**:
    - Defines the `Question` class, which stores the text and answer of each quiz question.

3. **data.py**:
    - Contains the list of questions fetched from the Open Trivia Database.

4. **quiz_brain.py**:
    - Defines the `QuizBrain` class, which manages the quiz logic, including keeping track of the current question, checking answers, and updating the score.

5. **ui.py**:
    - Defines the `QuizInterface` class, which manages the graphical user interface using `tkinter`.

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install dependencies**:
    - Make sure you have Python installed.
    - Install the required Python libraries:
        ```bash
        pip install requests
        ```

3. **Run the application**:
    ```bash
    python main.py
    ```

## Detailed File Descriptions

### main.py

This file is responsible for fetching quiz questions from the Open Trivia Database and initializing the quiz application.

```python
import requests

question_data = []

response = requests.get("https://opentdb.com/api.php?amount=10&type=boolean")
response.raise_for_status()
for each_thing in response.json()["results"]:
    question_data.append(each_thing)

from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
from ui import QuizInterface

question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)

print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
```

### question_model.py

Defines the `Question` class, which is used to store the text and answer of each quiz question.

```python
class Question:
    def __init__(self, q_text, q_answer):
        self.text = q_text
        self.answer = q_answer
```

### data.py

Contains the list of questions fetched from the Open Trivia Database.

```python
question_data = [
    # Example question format
    # {"category": "Science: Computers", "type": "boolean", "difficulty": "easy", "question": "The programming language Python is based off a modified version of JavaScript.", "correct_answer": "False", "incorrect_answers": ["True"]}
]
```

### quiz_brain.py

Defines the `QuizBrain` class, which manages the quiz logic, including keeping track of the current question, checking answers, and updating the score.

```python
import html

class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {q_text} (True/False): "

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False
```

### ui.py

Defines the `QuizInterface` class, which manages the graphical user interface using `tkinter`.

```python
from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg= THEME_COLOR, padx= 20, pady= 20)
        
        self.canvas = Canvas(width= 300, height= 250, bg= "white", highlightthickness= 0)
        self.canvas.grid(row= 1, column= 0, columnspan= 2, padx= 20, pady= 20)
        self.question_text = self.canvas.create_text(150, 125, fill= "black",text= "Question", font= ("Arial", 20, "italic"), width= 280)
        
        self.score_label = Label(text= "Score: 0", padx= 20, pady= 20, bg= THEME_COLOR)
        self.score_label.grid(row=0, column= 1)
        
        true_image = PhotoImage(file= "images/true.png")
        self.true_button = Button(image= true_image, padx= 20, pady= 20, highlightthickness= 0, command= self.true_pressed)
        self.true_button.grid(row=2, column= 0)
        
        false_image = PhotoImage(file= "images/false.png")
        self.false_button = Button(image= false_image, padx= 20, pady= 20, highlightthickness= 0, command= self.false_pressed)
        self.false_button.grid(row=2, column= 1)
            
        self.get_next_question()
        
        self.window.mainloop()
        
    def get_next_question(self):
        self.canvas.config(bg= "white")
        if self.quiz.still_has_questions():
            self.score_label.config(text= f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text= q_text)
        else:
            self.canvas.itemconfig(self.question_text, text= "You've reached the end of the quiz.")
            self.true_button.config(state= "disabled")
            self.false_button.config(state= "disabled")
        
    def true_pressed(self):
        self.give_feedback(is_right= self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(is_right= self.quiz.check_answer("False"))
        
    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg= "green")
        else:
            self.canvas.config(bg= "red")
        self.window.after(1000, self.get_next_question)
```

### Images
- Place the true and false images in the `images` folder within the project directory.
  - `true.png`
  - `false.png`

## Running the Application
To run the application, simply execute `main.py`:
```bash
python main.py
```

You will see a GUI window where you can answer the quiz questions. The application will fetch questions from the Open Trivia Database and display them one by one. You can respond with True or False and see your score at the end.