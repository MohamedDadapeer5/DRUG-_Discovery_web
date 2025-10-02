#!/usr/bin/env python3
"""
Database setup script for Medicine Search System
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the medicine_search database if it doesn't exist"""
    print("🔧 Setting up database...")
    
    # First, connect to PostgreSQL server (default 'postgres' database)
    try:
        conn = psycopg2.connect(
            dbname='postgres',  # Connect to default database first
            user=os.getenv("DB_USER", "postgres"),
            password=input("Enter your PostgreSQL password: "),  # Ask for password
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'medicine_search';")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE medicine_search;")
            print("✅ Database 'medicine_search' created successfully!")
        else:
            print("✅ Database 'medicine_search' already exists!")
            
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        print("\n💡 Make sure:")
        print("   - PostgreSQL is running")
        print("   - You entered the correct password")
        print("   - PostgreSQL is installed on port 5432")
        return False

def create_tables():
    """Create the medicines table"""
    print("📋 Creating tables...")
    
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "medicine_search"),
            user=os.getenv("DB_USER", "postgres"),
            password=input("Enter your PostgreSQL password again: "),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        cursor = conn.cursor()
        
        # Read and execute schema
        with open('schema.sql', 'r') as f:
            schema = f.read()
            cursor.execute(schema)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Tables created successfully!")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating tables: {e}")
        return False
    except FileNotFoundError:
        print("❌ schema.sql file not found!")
        return False

if __name__ == "__main__":
    print("🏥 Medicine Search System - Database Setup")
    print("=" * 50)
    
    # Step 1: Create database
    if create_database():
        # Step 2: Create tables
        if create_tables():
            print("\n🎉 Database setup completed!")
            print("\nNext steps:")
            print("1. Run: python import_data.py (to import medicine data)")
            print("2. Run: python app.py (to start the web server)")
        else:
            print("\n❌ Database setup failed at table creation step")
    else:
        print("\n❌ Database setup failed at database creation step")