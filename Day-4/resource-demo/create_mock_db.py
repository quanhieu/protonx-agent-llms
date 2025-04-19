import sqlite3
def create_mock_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
    ''')
    
    # Create tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        priority INTEGER DEFAULT 1,
        due_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # Create categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    ''')
    
    # Create task_categories junction table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_categories (
        task_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        PRIMARY KEY (task_id, category_id),
        FOREIGN KEY (task_id) REFERENCES tasks(id),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    ''')
    
    # Insert some sample data
    cursor.execute("INSERT OR IGNORE INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
                  ("admin", "admin@example.com", "hashed_password_here"))
    cursor.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", 
                  ("Work", "Work-related tasks"))
    cursor.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", 
                  ("Personal", "Personal tasks"))
    
    conn.commit()
    conn.close()