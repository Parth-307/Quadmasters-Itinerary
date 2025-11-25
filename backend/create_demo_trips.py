#!/usr/bin/env python3
"""
Demo Trip Creator for Trip Management System
Creates sample trips that users can join for testing
"""

import sys
import os
sys.path.append('.')

from database import SessionLocal, create_tables
import models
from auth_system import AuthSystem
from datetime import datetime, timedelta
import uuid

def check_database():
    db = SessionLocal()
    auth = AuthSystem()

    print('=== CHECKING EXISTING TRIPS ===')
    trips = db.query(models.Trip).all()
    print(f'Total trips in database: {len(trips)}')

    for trip in trips:
        print(f'Trip ID: {trip.id}')
        print(f'Trip Name: {trip.name}')
        print(f'Join Code: {trip.join_code}')
        print(f'Created: {trip.created_at}')
        print('---')

    print('\n=== CHECKING USERS ===')
    users = db.query(models.User).all()
    print(f'Total users: {len(users)}')

    for user in users:
        print(f'User ID: {user.id}')
        print(f'Username: {user.username}')
        print(f'Trip ID: {user.trip_id}')
        print(f'Is Admin: {user.is_admin}')
        print('---')

    db.close()
    return trips

def create_demo_trip(trip_name, admin_username):
    """Create a demo trip with admin user"""
    db = SessionLocal()
    auth = AuthSystem()
    
    try:
        # Create trip admin
        trip, admin_user = auth.create_trip_admin(
            admin_username, 
            "demo123", 
            trip_name
        )
        
        print(f"✅ Created demo trip: {trip_name}")
        print(f"   Join Code: {trip.join_code}")
        print(f"   Admin Username: {admin_username}")
        print(f"   Trip ID: {trip.id}")
        print()
        
        return trip
    except Exception as e:
        print(f"❌ Failed to create trip '{trip_name}': {str(e)}")
        return None
    finally:
        db.close()

def create_sample_activities(trip_id):
    """Create sample activities for a trip"""
    db = SessionLocal()
    
    # Create activities with proper start_time and end_time
    from datetime import datetime, timedelta
    
    base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    activities = [
        {
            'title': 'Welcome Breakfast',
            'type': 'meal',
            'description': 'Morning breakfast with group introductions',
            'estimated_cost': 25.0,
            'capacity': 20,
            'start_time': base_date,
            'end_time': base_date + timedelta(hours=1)
        },
        {
            'title': 'City Walking Tour',
            'type': 'sightseeing',
            'description': 'Guided walking tour of city landmarks',
            'estimated_cost': 30.0,
            'capacity': 15,
            'start_time': base_date + timedelta(hours=2),
            'end_time': base_date + timedelta(hours=4)
        },
        {
            'title': 'Lunch at Local Restaurant',
            'type': 'meal',
            'description': 'Traditional local cuisine experience',
            'estimated_cost': 40.0,
            'capacity': 20,
            'start_time': base_date + timedelta(hours=5),
            'end_time': base_date + timedelta(hours=6, minutes=30)
        },
        {
            'title': 'Museum Visit',
            'type': 'cultural',
            'description': 'Explore local history and art',
            'estimated_cost': 15.0,
            'capacity': 25,
            'start_time': base_date + timedelta(hours=7),
            'end_time': base_date + timedelta(hours=8, minutes=30)
        },
        {
            'title': 'Sunset Dinner Cruise',
            'type': 'entertainment',
            'description': 'Evening dinner cruise with city views',
            'estimated_cost': 80.0,
            'capacity': 20,
            'start_time': base_date + timedelta(hours=18),
            'end_time': base_date + timedelta(hours=21)
        }
    ]
    
    for activity_data in activities:
        activity = models.Activity(
            trip_id=trip_id,
            created_by_user_id=None,  # Will be set when user creates activities
            title=activity_data['title'],
            type=activity_data['type'],
            start_time=activity_data['start_time'],
            end_time=activity_data['end_time'],
            description=activity_data['description'],
            estimated_cost=activity_data['estimated_cost'],
            capacity=activity_data['capacity'],
            status='pending'
        )
        db.add(activity)
    
    db.commit()
    print(f"✅ Created {len(activities)} sample activities for trip {trip_id}")
    db.close()

def main():
    """Main demo setup function"""
    print("🎒 Trip Management System - Demo Setup")
    print("=" * 50)
    
    # Check existing data
    existing_trips = check_database()
    
    if existing_trips:
        print(f"\n📝 Found {len(existing_trips)} existing trips. Demo trips can still be created.")
        print("\n🔑 EXISTING TRIPS JOIN CODES:")
        for trip in existing_trips:
            print(f"   • {trip.name} → Join Code: {trip.join_code}")
    
    # Create demo trips
    demo_trips = [
        ("Europe Adventure 2025", "europe_admin"),
        ("Asia Discovery Tour", "asia_admin"),
        ("American Road Trip", "america_admin"),
        ("Backpacking Adventure", "backpack_admin"),
        ("Luxury Vacation", "luxury_admin")
    ]
    
    print(f"\n🚀 Creating {len(demo_trips)} demo trips...")
    print("-" * 50)
    
    created_trips = []
    for trip_name, admin_username in demo_trips:
        trip = create_demo_trip(trip_name, admin_username)
        if trip:
            created_trips.append(trip)
            # Create sample activities for the trip
            create_sample_activities(trip.id)
    
    print("\n" + "=" * 50)
    print("🎉 DEMO SETUP COMPLETE!")
    print("=" * 50)
    
    if created_trips:
        print("\n🔑 DEMO TRIPS - JOIN CODES:")
        for trip in created_trips:
            print(f"   📍 {trip.name}")
            print(f"      Join Code: {trip.join_code}")
            print(f"      Admin: {trip.name.split()[0].lower()}_admin")
            print(f"      Password: demo123")
            print()
    
    print("\n📋 HOW TO JOIN A TRIP:")
    print("1. Go to Dashboard → 'Join Group Trip'")
    print("2. Enter any of the join codes above")
    print("3. Use the admin username and 'demo123' as password")
    print("4. Start exploring trip features!")
    
    print(f"\n💾 Total trips in database: {len(existing_trips) + len(created_trips)}")

if __name__ == "__main__":
    main()