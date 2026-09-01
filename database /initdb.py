import sqlite3

def initinterviewdatabase():
    conn = sqlite3.connect("interviewapp.db")
    cursor = conn.cursor()
    conn.execute("PRAGMA journal_mode=WAL;")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluations (
            evaluationid TEXT PRIMARY KEY,
            questionid TEXT NOT NULL,
            techscore REAL,
            commscore REAL,
            wpm INTEGER,
            verifierscore REAL,
            perfectedphrase TEXT,
            quizpassed BOOLEAN DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized safely with individual score columns and WAL mode!")

initinterviewdatabase()
