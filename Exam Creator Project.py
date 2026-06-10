import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

# --- Constants for File Names ---
EXAM_DATA_FILENAME = "exam_data.json"
EXAM_RESULTS_FILENAME = "exam_results.txt"
APPLICATION_ICON_FILENAME = "exam_icon.ico"
# --------------------------------

class ExamCreatorApplication:
    
    # This function initializes the main application window, sets the title, geometry, icon, and main menu buttons.
    def __init__(self, main_window_root):
        self.main_window_root = main_window_root
        self.main_window_root.title("Exam Creator Application")
        self.main_window_root.geometry("400x350")
        
        # Check and set the application icon if it exists
        if os.path.exists(APPLICATION_ICON_FILENAME):
            try:
                self.main_window_root.iconbitmap(APPLICATION_ICON_FILENAME)
            except:
                pass 

        # Main Menu Welcome Label
        self.welcome_label = tk.Label(main_window_root, text="Welcome to Exam System", font=("Arial", 18, "bold"))
        self.welcome_label.pack(pady=20)

        # Button to open Admin Mode
        self.admin_mode_button = tk.Button(main_window_root, text="Admin Mode (Create Exam)", width=25, height=2, command=self.open_admin_dashboard_window)
        self.admin_mode_button.pack(pady=10)

        # Button to open Student Mode
        self.student_mode_button = tk.Button(main_window_root, text="Student Mode (Take Exam)", width=25, height=2, command=self.initiate_student_login_process)
        self.student_mode_button.pack(pady=10)

        # Button to Exit the application
        self.exit_application_button = tk.Button(main_window_root, text="Exit", width=25, command=main_window_root.quit)
        self.exit_application_button.pack(pady=10)

    # ================= ADMIN SECTION =================

    # This function opens a new window for the administrator to input new questions and options.
    def open_admin_dashboard_window(self):
        self.admin_dashboard_window = tk.Toplevel(self.main_window_root)
        self.admin_dashboard_window.title("Admin Panel - Add Questions")
        self.admin_dashboard_window.geometry("450x550")
        
        if os.path.exists(APPLICATION_ICON_FILENAME):
            try:
                self.admin_dashboard_window.iconbitmap(APPLICATION_ICON_FILENAME)
            except:
                pass

        # Input field for the Question Text
        tk.Label(self.admin_dashboard_window, text="Question:", font=("Arial", 10, "bold")).pack(pady=5)
        self.question_text_entry = tk.Entry(self.admin_dashboard_window, width=60)
        self.question_text_entry.pack(pady=5)

        # Input field for Option A
        tk.Label(self.admin_dashboard_window, text="Option A:", font=("Arial", 9)).pack()
        self.option_a_entry = tk.Entry(self.admin_dashboard_window, width=50)
        self.option_a_entry.pack()

        # Input field for Option B
        tk.Label(self.admin_dashboard_window, text="Option B:", font=("Arial", 9)).pack()
        self.option_b_entry = tk.Entry(self.admin_dashboard_window, width=50)
        self.option_b_entry.pack()

        # Input field for Option C
        tk.Label(self.admin_dashboard_window, text="Option C:", font=("Arial", 9)).pack()
        self.option_c_entry = tk.Entry(self.admin_dashboard_window, width=50)
        self.option_c_entry.pack()

        # Input field for Option D
        tk.Label(self.admin_dashboard_window, text="Option D:", font=("Arial", 9)).pack()
        self.option_d_entry = tk.Entry(self.admin_dashboard_window, width=50)
        self.option_d_entry.pack()

        # Input field for the Correct Answer
        tk.Label(self.admin_dashboard_window, text="Correct Answer (a/b/c/d):", font=("Arial", 10, "bold")).pack(pady=10)
        self.correct_answer_entry = tk.Entry(self.admin_dashboard_window, width=10)
        self.correct_answer_entry.pack()

        # Button to save the question
        self.save_question_button = tk.Button(self.admin_dashboard_window, text="Save Question", bg="#4CAF50", fg="white", command=self.save_new_question_to_file)
        self.save_question_button.pack(pady=20)
        
        tk.Label(self.admin_dashboard_window, text="After adding, the data is saved in 'exam_data.json'", fg="gray").pack()

    # This function collects data from the input fields, validates it, and saves it to the JSON file.
    def save_new_question_to_file(self):
        question_text = self.question_text_entry.get()
        option_a_text = self.option_a_entry.get()
        option_b_text = self.option_b_entry.get()
        option_c_text = self.option_c_entry.get()
        option_d_text = self.option_d_entry.get()
        correct_answer_text = self.correct_answer_entry.get().lower().strip()

        # Validate that all fields are filled and the answer is valid
        if not all([question_text, option_a_text, option_b_text, option_c_text, option_d_text]) or correct_answer_text not in ['a', 'b', 'c', 'd']:
            messagebox.showerror("Error", "Please fill all fields and ensure correct answer is a, b, c, or d.")
            return

        new_question_data = {
            "question": question_text,
            "options": {"a": option_a_text, "b": option_b_text, "c": option_c_text, "d": option_d_text},
            "answer": correct_answer_text
        }

        existing_exam_data = []
        if os.path.exists(EXAM_DATA_FILENAME):
            try:
                with open(EXAM_DATA_FILENAME, 'r') as file_object:
                    existing_exam_data = json.load(file_object)
            except:
                existing_exam_data = []

        existing_exam_data.append(new_question_data)

        with open(EXAM_DATA_FILENAME, 'w') as file_object:
            json.dump(existing_exam_data, file_object, indent=4)

        messagebox.showinfo("Success", "Question added successfully! You can add another or close this window.")
        
        # Clear the input fields for the next entry
        self.question_text_entry.delete(0, tk.END)
        self.option_a_entry.delete(0, tk.END)
        self.option_b_entry.delete(0, tk.END)
        self.option_c_entry.delete(0, tk.END)
        self.option_d_entry.delete(0, tk.END)
        self.correct_answer_entry.delete(0, tk.END)


    # ================= STUDENT SECTION =================

    # This function asks for the student's name and checks if there are questions available to start the exam.
    def initiate_student_login_process(self):
        if not os.path.exists(EXAM_DATA_FILENAME) or os.path.getsize(EXAM_DATA_FILENAME) == 0:
            messagebox.showwarning("Warning", "No exams available! Ask Admin to create questions first.")
            return

        self.current_student_name = simpledialog.askstring("Student Login", "Enter your name:")
        if self.current_student_name and self.current_student_name.strip():
            self.start_exam_session()
        else:
            messagebox.showwarning("Warning", "Name cannot be empty.")

    # This function loads the questions from the file and opens the exam window.
    def start_exam_session(self):
        try:
            with open(EXAM_DATA_FILENAME, 'r') as file_object:
                self.exam_questions_list = json.load(file_object)
        except:
            messagebox.showwarning("Warning", "Error loading exam data.")
            return

        self.current_student_score = 0
        self.current_question_index = 0
        
        self.exam_session_window = tk.Toplevel(self.main_window_root)
        self.exam_session_window.title(f"Exam - {self.current_student_name}")
        self.exam_session_window.geometry("600x450")
        
        if os.path.exists(APPLICATION_ICON_FILENAME):
            try:
                self.exam_session_window.iconbitmap(APPLICATION_ICON_FILENAME)
            except:
                pass

        self.exam_session_window.protocol("WM_DELETE_WINDOW", lambda: messagebox.showwarning("Warning", "Please complete the exam."))

        # Label to show question number
        self.question_counter_label = tk.Label(self.exam_session_window, text="", font=("Arial", 10))
        self.question_counter_label.pack(pady=5)
        
        # Label to show the question text
        self.question_text_label = tk.Label(self.exam_session_window, text="", font=("Arial", 14, "bold"), wraplength=550, justify=tk.LEFT)
        self.question_text_label.pack(pady=10)

        self.selected_answer_variable = tk.StringVar(value="x")

        # Radio buttons for options
        self.option_a_radiobutton = tk.Radiobutton(self.exam_session_window, text="", variable=self.selected_answer_variable, value="a", font=("Arial", 12))
        self.option_a_radiobutton.pack(anchor="w", padx=30, pady=5)
        
        self.option_b_radiobutton = tk.Radiobutton(self.exam_session_window, text="", variable=self.selected_answer_variable, value="b", font=("Arial", 12))
        self.option_b_radiobutton.pack(anchor="w", padx=30, pady=5)
        
        self.option_c_radiobutton = tk.Radiobutton(self.exam_session_window, text="", variable=self.selected_answer_variable, value="c", font=("Arial", 12))
        self.option_c_radiobutton.pack(anchor="w", padx=30, pady=5)
        
        self.option_d_radiobutton = tk.Radiobutton(self.exam_session_window, text="", variable=self.selected_answer_variable, value="d", font=("Arial", 12))
        self.option_d_radiobutton.pack(anchor="w", padx=30, pady=5)

        # Button to move to the next question
        self.next_question_button = tk.Button(self.exam_session_window, text="Next Question", bg="blue", fg="white", width=20, command=self.process_answer_and_next_question)
        self.next_question_button.pack(pady=20)

        self.load_current_question_interface()

    # This function updates the UI with the text and options for the current question.
    def load_current_question_interface(self):
        if self.current_question_index < len(self.exam_questions_list):
            current_question_data = self.exam_questions_list[self.current_question_index]
            
            self.question_counter_label.config(text=f"Question {self.current_question_index+1} of {len(self.exam_questions_list)}")
            self.question_text_label.config(text=current_question_data['question'])
            
            self.option_a_radiobutton.config(text=f"A) {current_question_data['options']['a']}")
            self.option_b_radiobutton.config(text=f"B) {current_question_data['options']['b']}")
            self.option_c_radiobutton.config(text=f"C) {current_question_data['options']['c']}")
            self.option_d_radiobutton.config(text=f"D) {current_question_data['options']['d']}")
            
            self.selected_answer_variable.set("x") # Reset selection
            
            if self.current_question_index == len(self.exam_questions_list) - 1:
                self.next_question_button.config(text="Finish Exam")
                
        else:
            self.finalize_exam_session()

    # This function checks the selected answer, updates the score, and calls the function to load the next question.
    def process_answer_and_next_question(self):
        selected_option = self.selected_answer_variable.get()
        if selected_option == "x":
            messagebox.showwarning("Wait", "Please select an answer!")
            return

        correct_answer = self.exam_questions_list[self.current_question_index]['answer']
        if selected_option == correct_answer:
            self.current_student_score += 1

        self.current_question_index += 1
        self.load_current_question_interface()

    # This function calculates the final percentage, shows a message box with results, and saves the result to a file.
    def finalize_exam_session(self):
        total_questions_count = len(self.exam_questions_list)
        score_percentage = (self.current_student_score / total_questions_count) * 100
        result_message = (
            f"Exam Finished!\n\n"
            f"Student: {self.current_student_name}\n"
            f"Final Score: {self.current_student_score}/{total_questions_count}\n"
            f"Percentage: {score_percentage:.1f}%"
        )
        
        messagebox.showinfo("Exam Result", result_message)
        self.save_exam_result_to_file(total_questions_count)
        self.exam_session_window.destroy()

    # This function appends the student's name, timestamp, and score to the results text file.
    def save_exam_result_to_file(self, total_questions_count):
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_record_string = f"[{current_timestamp}] Student: {self.current_student_name} | Score: {self.current_student_score}/{total_questions_count}\n"
        
        with open(EXAM_RESULTS_FILENAME, "a") as file_object:
            file_object.write(result_record_string)
        
        print(f"Result saved to {EXAM_RESULTS_FILENAME}")

# --- Main Execution Block ---
if __name__ == "__main__":
    main_window_root = tk.Tk()
    app_instance = ExamCreatorApplication(main_window_root)
    main_window_root.mainloop()