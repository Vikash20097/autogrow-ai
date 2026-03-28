#!/usr/bin/env python3
"""
Database Migration Script for AutoGrow-AI
Fixes the AutoReply table schema mismatch
"""

import os
import sqlite3
from datetime import datetime

def backup_database():
    """Create a backup of the current database"""
    if os.path.exists('instance/autogrow.db'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'instance/autogrow_backup_{timestamp}.db'
        os.rename('instance/autogrow.db', backup_name)
        print(f"✅ Database backed up to: {backup_name}")
        return backup_name
    return None

def create_new_database():
    """Create a new database with correct schema"""
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    conn = sqlite3.connect('instance/autogrow.db')
    cursor = conn.cursor()
    
    # Create tables with correct schema
    cursor.execute('''
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) NOT NULL UNIQUE,
            email VARCHAR(120) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_path VARCHAR(200) NOT NULL,
            caption TEXT NOT NULL,
            scheduled_time DATETIME NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE auto_reply (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword VARCHAR(200) NOT NULL,
            reply_text TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL DEFAULT 1,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE chat_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_reply TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE auto_mode (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            is_enabled BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    # Create default user (user_id = 1)
    cursor.execute('''
        INSERT INTO user (username, email, password_hash, created_at)
        VALUES ('admin', 'admin@autogrow.ai', 'default_hash', CURRENT_TIMESTAMP)
    ''')
    
    # Create default auto mode record
    cursor.execute('''
        INSERT INTO auto_mode (user_id, is_enabled, created_at, updated_at)
        VALUES (1, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ New database created with correct schema")
    print("✅ Default user (admin) created with user_id = 1")
    print("✅ Default auto_mode record created")

def migrate_data(backup_file):
    """Migrate existing auto_reply data to new schema"""
    if not backup_file or not os.path.exists(backup_file):
        print("⚠️  No backup file found, skipping data migration")
        return
    
    # Connect to old and new databases
    old_conn = sqlite3.connect(backup_file)
    new_conn = sqlite3.connect('instance/autogrow.db')
    
    old_cursor = old_conn.cursor()
    new_cursor = new_conn.cursor()
    
    try:
        # Get existing auto_reply data
        old_cursor.execute('SELECT keyword, reply_text, created_at FROM auto_reply')
        old_data = old_cursor.fetchall()
        
        if old_data:
            # Insert data into new table with default user_id=1 and is_active=True
            for keyword, reply_text, created_at in old_data:
                new_cursor.execute('''
                    INSERT INTO auto_reply (keyword, reply_text, created_at, user_id, is_active)
                    VALUES (?, ?, ?, 1, 1)
                ''', (keyword, reply_text, created_at))
            
            new_conn.commit()
            print(f"✅ Migrated {len(old_data)} auto_reply records to new schema")
        else:
            print("ℹ️  No existing auto_reply data to migrate")
            
    except Exception as e:
        print(f"⚠️  Error during data migration: {e}")
        new_conn.rollback()
    finally:
        old_conn.close()
        new_conn.close()

def main():
    """Main migration function"""
    print("🔧 AutoGrow-AI Database Migration Tool")
    print("=" * 50)
    
    # Step 1: Backup existing database
    print("Step 1: Creating backup...")
    backup_file = backup_database()
    
    # Step 2: Create new database with correct schema
    print("\nStep 2: Creating new database...")
    create_new_database()
    
    # Step 3: Migrate existing data
    print("\nStep 3: Migrating data...")
    migrate_data(backup_file)
    
    print("\n" + "=" * 50)
    print("🎉 Database migration completed successfully!")
    print("\nNext steps:")
    print("1. Run your Flask application")
    print("2. Test the Auto Reply functionality")
    print("3. Verify all features work correctly")
    
    if backup_file:
        print(f"\n⚠️  Old database backed up to: {backup_file}")
        print("You can delete it after confirming everything works.")

if __name__ == '__main__':
    main()