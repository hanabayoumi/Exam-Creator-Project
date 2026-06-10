# Exam Creator Application

A digital exam system that allows users to create multiple-choice questions and lets students take the exam in a digital interface. This was a collaborative team project built as a desktop application.

---

## Project Overview
The application connects an Admin Mode for inputting questions with a Student Mode for taking the quiz and receiving a final grade. 

## My Role: Backend & Data Logic
While this was a group project, my responsibilities were strictly focused on the core backend logic, file processing, and input safety checking. I did not handle the user interface design. 

My specific contributions include:
* **Result Logging & File Operations:** Wrote the logic to automatically open, append, and save student results into a local text file (`exam_results.txt`).
* **Timestamp Integration:** Used Python's standard tracking tools to capture the exact date and time a student finishes their exam and format it cleanly alongside their score.
* **Input Validation & Error Handling:** Built conditional checks to make sure the program doesn't crash if a user leaves a field blank or types an invalid answer key.
* **Score & Percentage Calculations:** Programmed the math formulas that track the student's correct answers, calculate their final percentage grade, and safely pass those numbers to be saved.
