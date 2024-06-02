import sys
from dotenv import load_dotenv
load_dotenv()
from database.database import create_tables, drop_tables

def main():
    try:
        print("Starting database setup...")
        drop_tables()
        print("Dropped existing tables.")
        create_tables()
        print("Created new tables.")
    except Exception as e:
        print(f"An error occurred during database setup: {e}")
        sys.exit(1)
    else:
        print("Database setup completed successfully.")

if __name__ == "__main__":
    main()
