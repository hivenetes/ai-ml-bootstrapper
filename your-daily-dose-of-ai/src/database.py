import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.db_name = "custom_urls.db"
        self.init_database()

    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                u_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create daily_updates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_daily_updates (
                udu_id INTEGER PRIMARY KEY AUTOINCREMENT,
                u_id INTEGER REFERENCES users(u_id),
                reference_urls TEXT,
                audio_filename TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


        # Create daily_updates scrapes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_daily_updates_scrapes (
                udus_id INTEGER PRIMARY KEY AUTOINCREMENT,
                udu_id INTEGER REFERENCES user_daily_updates(udu_id),
                title TEXT,
                summary TEXT,
                source_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create user_custom_urls table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_custom_urls (
                ucu_id INTEGER PRIMARY KEY AUTOINCREMENT,
                u_id INTEGER REFERENCES users(u_id),
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()

    def add_user(self, username):
        """Add a new user to the database if they don't already exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Check if user exists
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            
            if not existing_user:
                # User doesn't exist, insert new user
                cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
                conn.commit()
                return True
            return False  # User already exists
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        finally:
            conn.close()

    def get_user_id(self, username):
        """Get the user id for a username"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT u_id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0]


    def create_daily_update(self, u_id, reference_urls=None):
        """Add a daily update to the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        urls_str = ','.join(reference_urls) if reference_urls else None
        cursor.execute("""
            INSERT INTO user_daily_updates (u_id, reference_urls)
            VALUES (?, ?)
        """, (u_id, urls_str))
        update_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return update_id
    
    def update_audio_filename(self, udu_id, audio_filename=None):
        """Update the audio filename for a daily update"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_daily_updates SET audio_filename = ? WHERE udu_id = ?
        """, (audio_filename, udu_id))
        conn.commit()
        conn.close()
    
    def create_daily_update_scrapes(self, udu_id, title=None, summary=None, source_url=None):
        """Add a daily update scrape to the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_daily_updates_scrapes (udu_id, title, summary, source_url)
            VALUES (?, ?, ?, ?)
        """, (udu_id, title, summary, source_url))
        update_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return update_id

    def get_user_daily_updates(self, u_id):
        """Get all daily updates for a user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT udu_id, reference_urls, audio_filename, created_at 
                FROM user_daily_updates 
                WHERE u_id = ? 
                ORDER BY created_at DESC
            """, (u_id,))
            updates = cursor.fetchall()
            
            # Convert string dates to datetime objects
            formatted_updates = []
            for update in updates:
                udu_id, reference_urls, audio_filename, created_at = update
                # Convert string to datetime object
                if isinstance(created_at, str):
                    created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                formatted_updates.append((udu_id, reference_urls, audio_filename, created_at))
            
            return formatted_updates
        except Exception as e:
            print(f"Error getting user daily updates: {e}")
            return []
        finally:
            conn.close()
    
    def get_user_daily_updates_scrapes(self, udu_id):
        """Get all daily updates scrapes for a user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT udu_id, title, summary, source_url, created_at
            FROM user_daily_updates_scrapes
            WHERE udu_id = ?
            ORDER BY created_at DESC
        """, (udu_id,))
        updates = cursor.fetchall()
        conn.close()
        return updates




    def get_user_custom_urls(self, u_id):
        """Get all custom URLs for a user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM user_custom_urls WHERE u_id = ?", (u_id,))
        urls = cursor.fetchall()
        conn.close()
        return urls

    def add_user_custom_urls(self, u_id, url):
        """Add a custom URL for a user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_custom_urls (u_id, url) VALUES (?, ?)", (u_id, url))
        conn.commit()
        conn.close()

    def delete_user_custom_urls(self, u_id, url):
        """Delete a custom URL for a user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_custom_urls WHERE u_id = ? AND url = ?", (u_id, url))
        conn.commit()
        conn.close()

    def delete_daily_update(self, udu_id, u_id):
        """Delete daily update and related records"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Start a transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # First, verify this update belongs to the user
            cursor.execute("""
                SELECT udu_id FROM user_daily_updates 
                WHERE udu_id = ? AND u_id = ?
            """, (udu_id, u_id))
            result = cursor.fetchone()
            
            if result:
                # Delete from user_daily_update_scrapes
                cursor.execute("""
                    DELETE FROM user_daily_updates_scrapes 
                    WHERE udu_id = ?
                """, (udu_id,))
                
                # Delete from user_daily_updates
                cursor.execute("""
                    DELETE FROM user_daily_updates 
                    WHERE udu_id = ? AND u_id = ?
                """, (udu_id, u_id))
                
                # Commit the transaction
                conn.commit()
                return True
            return False
            
        except Exception as e:
            # Rollback in case of error
            cursor.execute("ROLLBACK")
            print(f"Error deleting daily update: {e}")
            return False
        finally:
            conn.close()

    
    def delete_incomplete_daily_update(self, udu_id, u_id):
        """Delete daily update and related records"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:            
            cursor.execute("""
                DELETE FROM user_daily_updates 
                WHERE udu_id = ? AND u_id = ?
            """, (udu_id, u_id))
            
            conn.commit()
        except Exception as e:
            print(f"Error deleting daily update: {e}")
            return False
        finally:
            conn.close()

    
    
    def close(self):
        """No need to explicitly close for SQLite, but keeping for compatibility"""
        pass 