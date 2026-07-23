import sqlite3

def initialize_database():
    connection = sqlite3.connect("slopeguard.db") #This links the python and database file
    cursor = connection.cursor() #This is what executes the SQL

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    #Assesments table
    create_assessments_table = """
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            location TEXT,
            slope_angle INTEGER,
            eaws_danger INTEGER,
            risk_score REAL,
            verdict TEXT,
            color TEXT,
            reason TEXT
        );
        """
    cursor.execute(create_assessments_table)
    connection.commit()
    connection.close()

def save_assessment(user_id, location, eaws_danger, risk_score, verdict, color, reason):
    connection = sqlite3.connect("slopeguard.db")
    cursor = connection.cursor()
    #Puts data into the database that was created

    sql_query = """
        INSERT INTO assessments (user_id, location, eaws_danger, risk_score, verdict, color, reason)
        VALUES (:user_id, :location, :eaws_danger, :risk_score, :verdict, :color, :reason) 
    """
    #The values section above act as placeholders
    #Using a dictionary to match the keys to the sql names
    data = {"user_id": user_id, "location": location,"eaws_danger": eaws_danger,"risk_score": risk_score,"verdict": verdict,"color": color,"reason": reason}
    cursor.execute(sql_query, data)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()