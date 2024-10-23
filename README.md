Quiz Application
================

This is a quiz application built using Django.

Getting Started
---------------

### Installation

1. Clone the repository: `git clone https://github.com/your-username/quiz-app.git`
2. Create a database: `python manage.py migrate`
3. Load the database dump: `python manage.py loaddata db_dump.json`

### Running the Application

1. Run the development server: `python manage.py runserver`
2. Open the application in your web browser: `http://localhost:8000`

### Features

#### Features for Students

* Take quizzes
* View quiz history
* View available quizzes

#### Features for Admins

* Create quizzes
* Edit/delete quizzes
* Hide/unhide students

### Database Structure

The application uses MySQL to store data for the following tables:

1. **`students_student`**
   - Stores student information.
   - **Fields:** `id`, `user_id` (Foreign Key to `auth_user`), `enrollment`, `contact`, `city`, `state`, `gender`, `profile_picture`

2. **`students_profile`**
   - Stores additional profile information related to students.
   - **Fields:** `id`, `student_id` (Foreign Key to `students_student`), `academic_records`

3. **`admins_quiz`**
   - Stores details about quizzes, such as title, description, and availability.
   - **Fields:** `id`, `title`, `description`, `created_at`, `updated_at`, `due_date`, `is_available_to_students`

4. **`admins_question`**
   - Stores questions related to each quiz, along with multiple-choice options.
   - **Fields:** `id`, `quiz_id` (Foreign Key to `admins_quiz`), `text`, `choice1`, `choice2`, `choice3`, `choice4`, `correct_answer`

5. **`students_quizresult`**
   - Stores results of quizzes taken by students, including the score and timestamp.
   - **Fields:** `id`, `student_id` (Foreign Key to `students_student`), `quiz_id` (Foreign Key to `admins_quiz`), `score`, `taken_at`

### Testing Functionality

To test the application, use the following credentials:

#### For Admin

- **Username:** teacher
- **Password:** testpass12

#### For Student

- **Username:** baba_yaga
- **Password:** student1234
