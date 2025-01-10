# Quiz Application

This is a fully-featured quiz application built using Django, deployed via Render.

## Getting Started

### Application Link
Access the application here: [Quiz Application](https://quiz-app-django-taty.onrender.com/)

### Superuser Credentials
For administrative access, use the following credentials:
- **Username:** teacher1
- **Password:** super1234

## Features

### Features for Students
- **Take Quizzes:** Attempt quizzes directly from your dashboard.
- **Coding Questions:** Solve technical assessments with an embedded code editor supporting 3+ programming languages.
- **View Quiz History:** Access past quiz attempts, scores, and detailed performance reports.
- **Performance Metrics:** Analyze your progress with key metrics like:
  - Overall scores
  - Rankings
  - Performance trends
  - Profile details

### Features for Admins
- **Quiz Management:**
  - Create, edit, and delete quizzes.
  - Upload quizzes via `.csv` files to streamline quiz creation (reduces setup time by 75%).
- **Question Types:**
  - Multiple-choice questions
  - Coding questions with real-time code execution
- **User Management:**
  - Manage student accounts
  - Hide/unhide students
- **Advanced Analytics:** Access performance trends and quiz insights.

## Database Structure
The application uses PostgreSQL to store data. Below is an overview of key tables:

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
   - Stores questions related to each quiz, including multiple-choice options and coding assessments.
   - **Fields:** `id`, `quiz_id` (Foreign Key to `admins_quiz`), `text`, `choice1`, `choice2`, `choice3`, `choice4`, `correct_answer`

5. **`students_quizresult`**
   - Stores results of quizzes taken by students, including the score and timestamp.
   - **Fields:** `id`, `student_id` (Foreign Key to `students_student`), `quiz_id` (Foreign Key to `admins_quiz`), `score`, `taken_at`

## Installation (For Local Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/quiz-app.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a PostgreSQL database and update the `DATABASES` settings in `settings.py`.
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Load the database dump (if available):
   ```bash
   python manage.py loaddata db_dump.json
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Access the application locally at `http://localhost:8000`

## Deployment
This application is deployed on Render using the following steps:

1. Push the project to a Git repository.
2. Link the repository to Render.
3. Configure environment variables (e.g., `DATABASE_URL` for PostgreSQL).
4. Deploy the application via Render's web service.

## Testing

Use the following credentials to test the application:

### Admin Access
- **Username:** teacher1
- **Password:** super1234

### Student Access
- **Username:** baba_yaga
- **Password:** student1234

---

Enjoy using the Quiz Application for seamless quiz management and performance tracking!

