# -------------------------------------------------------------------
# PostgreSQL CRUD Application for Students Table
# -------------------------------------------------------------------
# Author: Prisca Love

# Importing required libraries
import argparse          
import os                
from datetime import datetime  
import psycopg2          
from psycopg2.extras import RealDictCursor  
from dotenv import load_dotenv  

# Load environment variables from the .env file
load_dotenv()

# Database Configuration

# This helps keep credentials secure and flexible for deployment.
DB_CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": int(os.getenv("PGPORT", 5432)),
    "dbname": os.getenv("PGDATABASE", "university"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "postgres"),
}

#Establishes a connection to the PostgreSQL database
def get_conn():
    return psycopg2.connect(**DB_CONFIG)

#Retrieves and displays all student records from the database
def getAllStudents():
    """Retrieves and displays all records from the students table."""
    # Use context managers to ensure connections are closed automatically
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # SQL query to fetch all students
            cur.execute("""
                SELECT student_id, first_name, last_name, email, enrollment_date
                FROM students
                ORDER BY student_id;
            """)
            rows = cur.fetchall()
            
            # If no records found, notify user
            if not rows:
                print("No students found.")
                return []
            
            # Print each record in a readable format
            for r in rows:
                print(f"{r['student_id']}: {r['first_name']} {r['last_name']} ({r['email']}) — {r['enrollment_date']}")
            return rows

#Inserts a new student record into the students table
def addStudent(first_name, last_name, email, enrollment_date):
    """Inserts a new student record into the students table."""
    # Validate that the enrollment date is in the correct YYYY-MM-DD format
    try:
        datetime.strptime(enrollment_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("enrollment_date must be YYYY-MM-DD")

    with get_conn() as conn:
        with conn.cursor() as cur:
            # Insert a new record and return the new student_id
            cur.execute("""
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id;
            """, (first_name, last_name, email, enrollment_date))
            
            new_id = cur.fetchone()[0]  # Retrieve new student ID
            conn.commit()  # Save the transaction
            print(f"Added student with ID {new_id}")

#Updates the email address for a student by their ID
def updateStudentEmail(student_id, new_email):
    """Updates the email address for a student with the specified student_id."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE students
                SET email = %s
                WHERE student_id = %s
                RETURNING student_id;
            """, (new_email, student_id))
            
            row = cur.fetchone()
            if not row:
                print(f"No student found with id {student_id}")
                return
            conn.commit()
            print(f"Updated email for student {student_id}")

#Deletes a student record based on student_id
def deleteStudent(student_id):
    """Deletes the record of the student with the specified student_id."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM students
                WHERE student_id = %s
                RETURNING student_id;
            """, (student_id,))
            
            row = cur.fetchone()
            if not row:
                print(f"No student found with id {student_id}")
                return
            conn.commit()
            print(f"Deleted student {student_id}")

#Command-line interface to interact with the CRUD functions
def main():
    # ArgumentParser allows us to run functions via command line
    parser = argparse.ArgumentParser(description="Students CRUD demo")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Subcommand: list
    sub.add_parser("list", help="List all students")

    # Subcommand: add
    p_add = sub.add_parser("add", help="Add a student")
    p_add.add_argument("first_name")
    p_add.add_argument("last_name")
    p_add.add_argument("email")
    p_add.add_argument("enrollment_date", help="YYYY-MM-DD")

    # Subcommand: update-email
    p_upd = sub.add_parser("update-email", help="Update a student's email")
    p_upd.add_argument("student_id", type=int)
    p_upd.add_argument("new_email")

    # Subcommand: delete
    p_del = sub.add_parser("delete", help="Delete a student by id")
    p_del.add_argument("student_id", type=int)

    # Parse command-line input and call appropriate function
    args = parser.parse_args()
    if args.cmd == "list":
        getAllStudents()
    elif args.cmd == "add":
        addStudent(args.first_name, args.last_name, args.email, args.enrollment_date)
    elif args.cmd == "update-email":
        updateStudentEmail(args.student_id, args.new_email)
    elif args.cmd == "delete":
        deleteStudent(args.student_id)


# This ensures the main() function only runs when the script is executed directly, not when it’s imported as a module.

if __name__ == "__main__":
    main()
