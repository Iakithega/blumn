#!/usr/bin/env python3
"""
SQL Learning Practice with Real Plant Care Data

This file contains progressive SQL exercises using your actual plant database.
Each section builds on the previous one, from basic queries to advanced joins.

Run this file: uv run python backend/app/database/sql_practice.py
"""

import os
from datetime import date, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Import your models
from models import Plant, DailyCare
from connection import db_manager

load_dotenv()

class SQLPracticeSession:
    """Interactive SQL learning session with your plant data."""
    
    def __init__(self):
        self.db = db_manager
        print("🌱 SQL Learning Session with Your Plant Care Data")
        print("=" * 50)
    
    def section_1_basic_queries(self):
        """
        SECTION 1: Basic SELECT Queries
        Learn: SELECT, FROM, basic syntax
        """
        print("\n📚 SECTION 1: Basic SELECT Queries")
        print("-" * 40)
        
        # Exercise 1.1: Test connection
        print("🔍 Exercise 1.1: Test database connection")
        sql = "SELECT 1 as test_value"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        print(f"Result: {result}")
        
        # Exercise 1.2: See all plants
        print("\n🔍 Exercise 1.2: Show all plants")
        sql = "SELECT * FROM plants"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        print(f"Found {len(result)} plants:")
        for plant in result[:5]:  # Show first 5
            print(f"  - {plant}")
        
        # Exercise 1.3: Select specific columns
        print("\n🔍 Exercise 1.3: Show only plant names")
        sql = "SELECT name FROM plants"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        plant_names = [row[0] for row in result]
        print(f"Plant names: {plant_names[:10]}")  # Show first 10
        
        # Exercise 1.4: Count records
        print("\n🔍 Exercise 1.4: Count total plants")
        sql = "SELECT COUNT(*) FROM plants"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        print(f"Total plants: {result[0][0]}")
        
        input("\n⏸️  Press Enter to continue to Section 2...")
    
    def section_2_filtering(self):
        """
        SECTION 2: WHERE Clauses (Filtering)
        Learn: WHERE, comparison operators, LIKE, IS NULL/IS NOT NULL
        """
        print("\n📚 SECTION 2: Filtering with WHERE")
        print("-" * 40)
        
        # Exercise 2.1: Filter by plant name
        print("🔍 Exercise 2.1: Find specific plant")
        sql = "SELECT * FROM plants WHERE name = 'Monstera Deliciosa'"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        print(f"Result: {result}")
        
        # Exercise 2.2: Pattern matching with LIKE
        print("\n🔍 Exercise 2.2: Find plants with 'monstera' in name")
        sql = "SELECT name FROM plants WHERE name ILIKE '%monstera%'"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        for row in result:
            print(f"  - {row[0]}")
        
        # Exercise 2.3: Filter care records by date
        print("\n🔍 Exercise 2.3: Care records from last 7 days")
        week_ago = date.today() - timedelta(days=7)
        sql = f"SELECT * FROM daily_care WHERE care_date >= '{week_ago}'"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        print(f"Found {len(result)} care records from last week")
        
        # Exercise 2.4: Find plants that were watered (not NULL)
        print("\n🔍 Exercise 2.4: Records where plants were actually watered")
        sql = "SELECT plant_id, care_date, water_ml FROM daily_care WHERE water_ml IS NOT NULL"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        print(f"Found {len(result)} watering records")
        for row in result[:5]:
            print(f"  Plant {row[0]}: {row[2]}ml on {row[1]}")
        
        input("\n⏸️  Press Enter to continue to Section 3...")
    
    def section_3_sorting_limiting(self):
        """
        SECTION 3: Sorting and Limiting Results  
        Learn: ORDER BY, LIMIT, ASC/DESC
        """
        print("\n📚 SECTION 3: Sorting and Limiting")
        print("-" * 40)
        
        # Exercise 3.1: Sort plants alphabetically
        print("🔍 Exercise 3.1: Plants in alphabetical order")
        sql = "SELECT name FROM plants ORDER BY name ASC"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        for row in result[:10]:
            print(f"  - {row[0]}")
        
        # Exercise 3.2: Most recent care records
        print("\n🔍 Exercise 3.2: 5 most recent care activities")
        sql = "SELECT plant_id, care_date, water_ml FROM daily_care ORDER BY care_date DESC LIMIT 5"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        for row in result:
            print(f"  Plant {row[0]}: {row[2]}ml on {row[1]}")
        
        # Exercise 3.3: Largest watering amounts
        print("\n🔍 Exercise 3.3: Top 5 largest watering amounts")
        sql = "SELECT plant_id, care_date, water_ml FROM daily_care WHERE water_ml IS NOT NULL ORDER BY water_ml DESC LIMIT 5"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        for row in result:
            print(f"  Plant {row[0]}: {row[2]}ml on {row[1]}")
        
        input("\n⏸️  Press Enter to continue to Section 4...")
    
    def section_4_aggregations(self):
        """
        SECTION 4: Aggregate Functions
        Learn: COUNT, SUM, AVG, MIN, MAX
        """
        print("\n📚 SECTION 4: Aggregate Functions")
        print("-" * 40)
        
        # Exercise 4.1: Count care records per plant
        print("🔍 Exercise 4.1: Total care records per plant")
        sql = """
        SELECT plant_id, COUNT(*) as total_records 
        FROM daily_care 
        GROUP BY plant_id 
        ORDER BY total_records DESC
        """
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        for row in result[:5]:
            print(f"  Plant {row[0]}: {row[1]} care records")
        
        # Exercise 4.2: Total water given to each plant
        print("\n🔍 Exercise 4.2: Total water given to each plant")
        sql = """
        SELECT plant_id, SUM(water_ml) as total_water_ml 
        FROM daily_care 
        WHERE water_ml IS NOT NULL 
        GROUP BY plant_id 
        ORDER BY total_water_ml DESC
        """
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        for row in result[:5]:
            print(f"  Plant {row[0]}: {row[1]}ml total")
        
        # Exercise 4.3: Average water amount
        print("\n🔍 Exercise 4.3: Average water amount per watering")
        sql = "SELECT AVG(water_ml) as avg_water FROM daily_care WHERE water_ml IS NOT NULL"
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        print(f"Average water per watering: {result[0][0]:.1f}ml")
        
        # Exercise 4.4: Date ranges
        print("\n🔍 Exercise 4.4: Date range of your care data")
        sql = """
        SELECT 
            MIN(care_date) as first_record,
            MAX(care_date) as last_record,
            COUNT(DISTINCT care_date) as total_days
        FROM daily_care
        """
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        row = result[0]
        print(f"Data spans from {row[0]} to {row[1]} ({row[2]} days)")
        
        input("\n⏸️  Press Enter to continue to Section 5...")
    
    def section_5_joins(self):
        """
        SECTION 5: JOINs - The Most Important SQL Concept!
        Learn: INNER JOIN, LEFT JOIN, foreign keys
        """
        print("\n📚 SECTION 5: JOINs - Connecting Tables")
        print("-" * 40)
        
        # Exercise 5.1: Basic INNER JOIN
        print("🔍 Exercise 5.1: Plant names with their care records")
        sql = """
        SELECT p.name, dc.care_date, dc.water_ml 
        FROM plants p 
        INNER JOIN daily_care dc ON p.id = dc.plant_id 
        WHERE dc.water_ml IS NOT NULL 
        ORDER BY dc.care_date DESC 
        LIMIT 10
        """
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        for row in result:
            print(f"  {row[0]}: {row[2]}ml on {row[1]}")
        
        # Exercise 5.2: LEFT JOIN to see all plants
        print("\n🔍 Exercise 5.2: All plants, even those without care records")
        sql = """
        SELECT p.name, COUNT(dc.id) as care_records
        FROM plants p 
        LEFT JOIN daily_care dc ON p.id = dc.plant_id 
        GROUP BY p.id, p.name
        ORDER BY care_records DESC
        """
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        for row in result[:10]:
            print(f"  {row[0]}: {row[1]} care records")
        
        # Exercise 5.3: Complex join with conditions
        print("\n🔍 Exercise 5.3: Plants watered in last 30 days")
        month_ago = date.today() - timedelta(days=30)
        sql = f"""
        SELECT DISTINCT p.name 
        FROM plants p 
        INNER JOIN daily_care dc ON p.id = dc.plant_id 
        WHERE dc.water_ml IS NOT NULL 
        AND dc.care_date >= '{month_ago}'
        ORDER BY p.name
        """
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        print(f"Plants watered in last 30 days:")
        for row in result:
            print(f"  - {row[0]}")
        
        input("\n⏸️  Press Enter to continue to Section 6...")
    
    def section_6_advanced(self):
        """
        SECTION 6: Advanced Queries
        Learn: Subqueries, HAVING, complex conditions
        """
        print("\n📚 SECTION 6: Advanced SQL")
        print("-" * 40)
        
        # Exercise 6.1: Subquery - plants never watered
        print("🔍 Exercise 6.1: Plants that have NEVER been watered")
        sql = """
        SELECT name 
        FROM plants 
        WHERE id NOT IN (
            SELECT DISTINCT plant_id 
            FROM daily_care 
            WHERE water_ml IS NOT NULL
        )
        """
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        if result:
            print("Plants never watered:")
            for row in result:
                print(f"  - {row[0]}")
        else:
            print("Great! All plants have been watered at least once.")
        
        # Exercise 6.2: HAVING clause
        print("\n🔍 Exercise 6.2: Plants with more than 5 care records")
        sql = """
        SELECT p.name, COUNT(dc.id) as care_count
        FROM plants p 
        INNER JOIN daily_care dc ON p.id = dc.plant_id 
        GROUP BY p.id, p.name
        HAVING COUNT(dc.id) > 5
        ORDER BY care_count DESC
        """
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        for row in result:
            print(f"  {row[0]}: {row[1]} records")
        
        # Exercise 6.3: Complex date query
        print("\n🔍 Exercise 6.3: Plants not watered in last 7 days")
        week_ago = date.today() - timedelta(days=7)
        sql = f"""
        SELECT p.name, MAX(dc.care_date) as last_watered
        FROM plants p 
        LEFT JOIN daily_care dc ON p.id = dc.plant_id AND dc.water_ml IS NOT NULL
        GROUP BY p.id, p.name
        HAVING MAX(dc.care_date) < '{week_ago}' OR MAX(dc.care_date) IS NULL
        ORDER BY last_watered ASC NULLS FIRST
        """
        result = self.db.execute_raw_sql(sql)
        print(f"Query: {sql}")
        print("Plants needing water:")
        for row in result[:10]:
            last_watered = row[1] if row[1] else "Never"
            print(f"  {row[0]}: last watered {last_watered}")
        
        print("\n🎉 Congratulations! You've completed the SQL basics!")
    
    def run_all_sections(self):
        """Run all SQL learning sections."""
        print("Starting complete SQL learning session...")
        self.section_1_basic_queries()
        self.section_2_filtering()
        self.section_3_sorting_limiting()
        self.section_4_aggregations()
        self.section_5_joins()
        self.section_6_advanced()
        print("\n🏆 SQL Learning Complete! You're ready to work with databases!")

def main():
    """Main learning session."""
    practice = SQLPracticeSession()
    
    print("\nChoose your learning path:")
    print("1. Run all sections (full course)")
    print("2. Run specific section")
    print("3. Interactive mode (section by section)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        practice.run_all_sections()
    elif choice == "2":
        print("\nSections available:")
        print("1. Basic Queries")
        print("2. Filtering (WHERE)")
        print("3. Sorting and Limiting")
        print("4. Aggregate Functions")
        print("5. JOINs")
        print("6. Advanced Queries")
        
        section = input("Enter section number (1-6): ").strip()
        sections = {
            "1": practice.section_1_basic_queries,
            "2": practice.section_2_filtering,
            "3": practice.section_3_sorting_limiting,
            "4": practice.section_4_aggregations,
            "5": practice.section_5_joins,
            "6": practice.section_6_advanced
        }
        
        if section in sections:
            sections[section]()
        else:
            print("Invalid section number!")
    
    elif choice == "3":
        practice.run_all_sections()
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()