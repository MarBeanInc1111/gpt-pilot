from .database import database\_exists, create\_database, save\_app

def establish\_database\_connection():
    if not database\_exists():
        create\_database()
    # any additional setup or connection code can be added here

# optionally, you can also include a function to close the database connection
def close\_database\_connection():
    # code to close the database connection goes here
    pass

