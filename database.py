import sqlite3
import json

def create_tables():
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()
    
    # create chat_history 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        session_id INTEGER,
        user_msg TEXT,
        assistant_msg TEXT,
        master_schema NVARCHAR,
        incremental_update NVARCHAR,
        changelog NVARCHAR,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
    )
               
''')
    # create user_profiles
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        aggregated_tags TEXT,
        summary TEXT,
        engagement_metrics TEXT,
        last_interaction TIMESTAMP,
        total_interactions INTEGER
    );
    ''')
    
    #Submit changes and close database connection
    conn.commit()
    conn.close()
    
#Calling functions to create tables
create_tables()
    