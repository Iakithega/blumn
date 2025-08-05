#!/usr/bin/env python3
"""
Example queries for the plant care database.

This demonstrates SQL concepts and SQLAlchemy usage:
- Basic queries (SELECT, WHERE, ORDER BY)
- Joins between plants and daily_care tables
- Aggregations (COUNT, MAX, MIN)
- Calculated fields (days without water)
- Complex filtering
"""

import sys
from pathlib import Path
from datetime import datetime, date, timedelta
from sqlalchemy import func, desc, and_, or_

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from backend.app.database.connection import db_manager, test_connection
from backend.app.database.models import Plant, DailyCare, get_plant_status, get_days_without_water


def show_all_plants():
    """Query 1: Show all plants (like 'SELECT * FROM plants')"""
    print("🌱 All Plants in Database")
    print("-" * 30)
    
    with db_manager.get_session() as session:
        plants = session.query(Plant).order_by(Plant.name).all()
        
        for plant in plants:
            print(f"ID: {plant.id:2d} | {plant.name}")
        
        print(f"\nTotal plants: {len(plants)}")


def show_recent_care_activities():
    """Query 2: Show recent care activities (JOIN example)"""
    print("\n📅 Recent Care Activities (Last 7 Days)")
    print("-" * 50)
    
    seven_days_ago = date.today() - timedelta(days=7)
    
    with db_manager.get_session() as session:
        # This is a JOIN query in SQLAlchemy
        recent_care = session.query(DailyCare, Plant.name)\
            .join(Plant)\
            .filter(DailyCare.care_date >= seven_days_ago)\
            .order_by(desc(DailyCare.care_date))\
            .limit(10)\
            .all()
        
        for care, plant_name in recent_care:
            activities = []
            if care.water_ml:
                activities.append(f"💧{care.water_ml}ml")
            if care.fertilizer:
                activities.append(f"🌿{care.fertilizer}")
            if care.treatment:
                activities.append(f"🧴{care.treatment}")
            
            activity_str = " + ".join(activities) if activities else "📝 condition only"
            print(f"{care.care_date} | {plant_name:25} | {activity_str}")


def show_watering_summary():
    """Query 3: Watering summary with aggregation"""
    print("\n💧 Watering Summary by Plant")
    print("-" * 40)
    
    with db_manager.get_session() as session:
        # Complex query with JOIN and aggregation
        watering_stats = session.query(
            Plant.name,
            func.count(DailyCare.id).label('total_waterings'),
            func.max(DailyCare.care_date).label('last_watered'),
            func.sum(DailyCare.water_ml).label('total_water_ml')
        )\
        .join(DailyCare)\
        .filter(DailyCare.water_ml.isnot(None))\
        .group_by(Plant.id, Plant.name)\
        .order_by(desc('last_watered'))\
        .all()
        
        for name, count, last_date, total_ml in watering_stats:
            days_ago = (date.today() - last_date).days if last_date else "Never"
            print(f"{name:25} | {count:2d} waterings | Last: {last_date} ({days_ago} days ago) | Total: {total_ml or 0}ml")


def show_plants_needing_water():
    """Query 4: Plants that need water (calculated field example)"""
    print("\n🚨 Plants Needing Water (7+ days)")
    print("-" * 35)
    
    with db_manager.get_session() as session:
        plants = session.query(Plant).all()
        
        plants_needing_water = []
        
        for plant in plants:
            days_without = get_days_without_water(session, plant.id)
            if days_without is not None and days_without >= 7:
                plants_needing_water.append((plant, days_without))
        
        # Sort by days without water (most urgent first)
        plants_needing_water.sort(key=lambda x: x[1], reverse=True)
        
        if plants_needing_water:
            for plant, days in plants_needing_water:
                urgency = "🔥" if days >= 10 else "⚠️"
                print(f"{urgency} {plant.name:25} | {days} days without water")
        else:
            print("✅ All plants are well watered!")


def show_fertilizer_schedule():
    """Query 5: Fertilizer schedule (complex date filtering)"""
    print("\n🌿 Fertilizer Schedule")
    print("-" * 25)
    
    with db_manager.get_session() as session:
        plants = session.query(Plant).all()
        
        for plant in plants:
            # Get last fertilizer date
            last_fertilizer = session.query(DailyCare.care_date)\
                .filter(DailyCare.plant_id == plant.id)\
                .filter(DailyCare.fertilizer.isnot(None))\
                .order_by(desc(DailyCare.care_date))\
                .first()
            
            if last_fertilizer:
                days_since = (date.today() - last_fertilizer[0]).days
                status = "🔥 Overdue" if days_since > 21 else "✅ OK" if days_since < 14 else "⚠️ Soon"
                print(f"{plant.name:25} | Last: {last_fertilizer[0]} ({days_since} days) | {status}")
            else:
                print(f"{plant.name:25} | Never fertilized | 🔥 Needs fertilizer")


def show_plant_history(plant_name: str):
    """Query 6: Complete history for one plant"""
    print(f"\n📖 Complete History: {plant_name}")
    print("-" * 50)
    
    with db_manager.get_session() as session:
        plant = session.query(Plant).filter(Plant.name == plant_name).first()
        
        if not plant:
            print(f"❌ Plant '{plant_name}' not found")
            return
        
        # Get all care records for this plant
        history = session.query(DailyCare)\
            .filter(DailyCare.plant_id == plant.id)\
            .order_by(DailyCare.care_date)\
            .all()
        
        print(f"Plant ID: {plant.id}")
        print(f"Total care records: {len(history)}")
        print("\nCare History:")
        
        for record in history[-10:]:  # Show last 10 records
            activities = []
            if record.water_ml:
                activities.append(f"💧{record.water_ml}ml")
            if record.fertilizer:
                activities.append(f"🌿{record.fertilizer}")
            if record.treatment:
                activities.append(f"🧴{record.treatment}")
            if record.condition:
                activities.append(f"📝{record.condition}")
            
            activity_str = " + ".join(activities) if activities else "No care"
            print(f"  {record.care_date} | {activity_str}")


def show_database_statistics():
    """Query 7: Overall database statistics"""
    print("\n📊 Database Statistics")
    print("-" * 25)
    
    with db_manager.get_session() as session:
        # Basic counts
        plant_count = session.query(Plant).count()
        care_count = session.query(DailyCare).count()
        
        # Date range
        date_range = session.query(
            func.min(DailyCare.care_date).label('first_date'),
            func.max(DailyCare.care_date).label('last_date')
        ).first()
        
        # Activity counts
        water_count = session.query(DailyCare).filter(DailyCare.water_ml.isnot(None)).count()
        fertilizer_count = session.query(DailyCare).filter(DailyCare.fertilizer.isnot(None)).count()
        treatment_count = session.query(DailyCare).filter(DailyCare.treatment.isnot(None)).count()
        
        print(f"Total plants: {plant_count}")
        print(f"Total care records: {care_count}")
        print(f"Date range: {date_range.first_date} to {date_range.last_date}")
        print(f"Watering events: {water_count}")
        print(f"Fertilizer events: {fertilizer_count}")
        print(f"Treatment events: {treatment_count}")
        
        if plant_count > 0 and care_count > 0:
            avg_records = care_count / plant_count
            print(f"Average records per plant: {avg_records:.1f}")


def interactive_plant_lookup():
    """Interactive plant status lookup"""
    print("\n🔍 Interactive Plant Lookup")
    print("-" * 30)
    
    with db_manager.get_session() as session:
        plants = session.query(Plant).order_by(Plant.name).all()
        
        print("Available plants:")
        for i, plant in enumerate(plants, 1):
            print(f"{i:2d}. {plant.name}")
        
        try:
            choice = input("\nEnter plant number (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return
            
            plant_idx = int(choice) - 1
            if 0 <= plant_idx < len(plants):
                selected_plant = plants[plant_idx]
                
                # Show detailed status
                status = get_plant_status(session, selected_plant.id)
                print(f"\n🌱 {status['plant_name']} Status:")
                print(f"   Last watered: {status['last_watered']} ({status['days_without_water']} days ago)")
                print(f"   Last fertilized: {status['last_fertilized']}")
                
                if status['last_treatment']:
                    print(f"   Last treatment: {status['last_treatment']['type']} on {status['last_treatment']['date']}")
                
        except (ValueError, IndexError):
            print("Invalid selection")


def main():
    """Run all example queries."""
    
    # Test connection
    if not test_connection():
        print("❌ Cannot connect to database!")
        sys.exit(1)
    
    print("🔍 Plant Care Database Queries")
    print("=" * 40)
    
    # Run example queries
    show_all_plants()
    show_recent_care_activities()
    show_watering_summary()
    show_plants_needing_water()
    show_fertilizer_schedule()
    show_database_statistics()
    
    # Example of specific plant history
    print("\n" + "="*50)
    show_plant_history("Monstera Deliciosa")
    
    # Interactive demo
    print("\n" + "="*50)
    try:
        interactive_plant_lookup()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()