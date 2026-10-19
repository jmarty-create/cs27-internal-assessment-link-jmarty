import sqlite3

def initialize_database():
    connection = sqlite3.connect("slopeguard.db") #This links the python and database file
    cursor = connection.cursor() #This is what executes the SQL

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    #Assesments table
    create_assessments_table = """
        CREATE TABLE IF NOT EXISTS assessments (
            assessment_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            location TEXT,
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

def get_all_user_evaluations(user_id):
    connection = sqlite3.connect("slopeguard.db")
    cursor = connection.cursor()
    # Query to get id, location, risk_score, and verdict
    cursor.execute("""
        SELECT assessment_id, location, risk_score, verdict 
        FROM assessments 
        WHERE user_id = :user_id
        ORDER BY assessment_id ASC
    """, {"user_id": user_id})
    # fetchall takes all matching rows as a list
    all_evaluations = cursor.fetchall()
    connection.close()
    return all_evaluations

def get_single_evaluation(assessment_id):
    connection = sqlite3.connect("slopeguard.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT risk_score, location 
        FROM assessments 
        WHERE assessment_id = :assessment_id
    """, {"assessment_id": assessment_id})
    #fetchone takes only one row
    single_evaluation = cursor.fetchone()
    connection.close()
    return single_evaluation

def create_user(username, password):
    #Check that both fields were actually filled out
    if username and password:
        connection = sqlite3.connect("slopeguard.db")
        cursor = connection.cursor()

        #Insert data in users table
        cursor.execute("""
            INSERT INTO users (username, password) 
            VALUES (?, ?)
        """, (username, password))

        connection.commit()
        connection.close()
        return True

def verify_user(username, password):
    connection = sqlite3.connect("slopeguard.db")
    cursor = connection.cursor()
    #SQL to isolate the specific user
    cursor.execute("""
        SELECT user_id FROM users 
        WHERE username = ? AND password = ?
    """, (username, password))
    user = cursor.fetchone()
    connection.close()

    if user:
        return user[0]  # Returns user_id
    return None

if __name__ == "__main__":
    initialize_database()