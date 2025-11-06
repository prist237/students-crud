
Steps to Compile and Run the Application

1. Open Terminal and go to the project directory containing app.py:
   cd ~/Documents/students-crud

2. Activate the virtual environment (if not already active):
   source .venv/bin/activate

3. Ensure PostgreSQL is running on your system.
   If installed via Homebrew:
   brew services start postgresql@14

4. Verify the database setup:
   - The database should be named 'university'.
   - The 'students' table must exist (from the provided schema.sql file).
   - The table should already contain three initial records.

5. Make sure your .env file is configured correctly:
   PGHOST=localhost
   PGPORT=5432
   PGDATABASE=university
   PGUSER=postgres
   PGPASSWORD=your_password_here

6. Run the application from Terminal using the commands below:

   - List all students
     python app.py list

   - Add a new student
     python app.py add "Alice" "Johnson" "alice.johnson@example.com" 2024-09-03

   - Update a student’s email
     python app.py update-email 1 johnny.doe@example.com

   - Delete a student
     python app.py delete 3

7. Check the results in pgAdmin by running:
   SELECT * FROM students ORDER BY student_id;

   The records displayed in pgAdmin should match the console output.
