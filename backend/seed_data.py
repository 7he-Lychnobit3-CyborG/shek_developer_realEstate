#!/usr/bin/env python3
"""
Script to seed the real estate database with sample data
"""

import asyncio
import os
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import uuid
from datetime import datetime

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

# Import environment variables
from dotenv import load_dotenv
load_dotenv(backend_dir / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Sample data
sample_users = [
    {
        "id": str(uuid.uuid4()),
        "email": "john.seller@example.com",
        "full_name": "John Seller",
        "phone": "555-0101",
        "role": "seller",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "hashed_password": get_password_hash("password123")
    },
    {
        "id": str(uuid.uuid4()),
        "email": "jane.agent@example.com",
        "full_name": "Jane Smith",
        "phone": "555-0102",
        "role": "agent",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "hashed_password": get_password_hash("password123")
    },
    {
        "id": str(uuid.uuid4()),
        "email": "bob.buyer@example.com",
        "full_name": "Bob Johnson",
        "phone": "555-0103",
        "role": "buyer",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "hashed_password": get_password_hash("password123")
    },
    {
        "id": str(uuid.uuid4()),
        "email": "sarah.agent@example.com",
        "full_name": "Sarah Williams",
        "phone": "555-0104",
        "role": "agent",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "hashed_password": get_password_hash("password123")
    },
    {
        "id": str(uuid.uuid4()),
        "email": "mike.seller@example.com",
        "full_name": "Mike Davis",
        "phone": "555-0105",
        "role": "seller",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "hashed_password": get_password_hash("password123")
    }
]

async def create_sample_properties():
    """Create sample properties"""
    
    # Insert users first
    await db.users.delete_many({})  # Clear existing users
    await db.users.insert_many(sample_users)
    
    # Get user IDs
    users = await db.users.find().to_list(None)
    seller1 = next(u for u in users if u["email"] == "john.seller@example.com")
    seller2 = next(u for u in users if u["email"] == "mike.seller@example.com")
    agent1 = next(u for u in users if u["email"] == "jane.agent@example.com")
    agent2 = next(u for u in users if u["email"] == "sarah.agent@example.com")
    
    sample_properties = [
        {
            "id": str(uuid.uuid4()),
            "title": "Luxury Waterfront Villa with Pool",
            "description": "Stunning waterfront villa featuring breathtaking ocean views, private pool, and luxurious amenities. Perfect for those seeking the ultimate in coastal living with direct water access and modern design elements throughout.",
            "property_type": "villa",
            "status": "for_sale",
            "price": 2850000.0,
            "bedrooms": 5,
            "bathrooms": 4,
            "area_sqft": 4200.0,
            "address": "123 Ocean Boulevard",
            "city": "Malibu",
            "state": "CA",
            "zip_code": "90265",
            "country": "USA",
            "latitude": 34.0259,
            "longitude": -118.7798,
            "images": [
                "https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
                "https://images.unsplash.com/photo-1580587771525-78b9dba3b914"
            ],
            "amenities": ["private_pool", "ocean_view", "private_dock", "wine_cellar", "home_theater", "guest_house"],
            "year_built": 2019,
            "parking_spaces": 3,
            "owner_id": seller1["id"],
            "agent_id": agent1["id"],
            "is_featured": True,
            "views": 245,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Modern Luxury Home with Contemporary Design",
            "description": "Architecturally stunning modern home with clean lines, floor-to-ceiling windows, and an open-concept design. Features a resort-style backyard with pool and outdoor entertainment area.",
            "property_type": "house",
            "status": "for_sale",
            "price": 1650000.0,
            "bedrooms": 4,
            "bathrooms": 3,
            "area_sqft": 3200.0,
            "address": "456 Modern Lane",
            "city": "Beverly Hills",
            "state": "CA",
            "zip_code": "90210",
            "country": "USA",
            "latitude": 34.0736,
            "longitude": -118.4004,
            "images": [
                "https://images.unsplash.com/photo-1580587771525-78b9dba3b914",
                "https://images.unsplash.com/photo-1613490493576-7fde63acd811"
            ],
            "amenities": ["pool", "outdoor_kitchen", "smart_home", "solar_panels", "three_car_garage"],
            "year_built": 2021,
            "parking_spaces": 3,
            "owner_id": seller2["id"],
            "agent_id": agent1["id"],
            "is_featured": True,
            "views": 189,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Contemporary Villa with Terrace Views",
            "description": "Exceptional contemporary villa offering panoramic city and mountain views from multiple terraces. Features high-end finishes, spacious living areas, and a gourmet kitchen perfect for entertaining.",
            "property_type": "villa",
            "status": "for_sale",
            "price": 2200000.0,
            "bedrooms": 5,
            "bathrooms": 4,
            "area_sqft": 3800.0,
            "address": "789 Hillside Drive",
            "city": "Los Angeles",
            "state": "CA",
            "zip_code": "90068",
            "country": "USA",
            "latitude": 34.1184,
            "longitude": -118.3004,
            "images": [
                "https://images.unsplash.com/photo-1613490493576-7fde63acd811",
                "https://images.pexels.com/photos/1396132/pexels-photo-1396132.jpeg"
            ],
            "amenities": ["city_views", "multiple_terraces", "gourmet_kitchen", "home_office", "wine_storage"],
            "year_built": 2020,
            "parking_spaces": 2,
            "owner_id": seller1["id"],
            "agent_id": agent2["id"],
            "is_featured": True,
            "views": 167,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Elegant Single-Family Home",
            "description": "Beautiful single-family home in a desirable neighborhood. Features traditional architecture with modern updates, spacious rooms, and a lovely backyard perfect for families.",
            "property_type": "house",
            "status": "for_sale",
            "price": 875000.0,
            "bedrooms": 4,
            "bathrooms": 3,
            "area_sqft": 2800.0,
            "address": "321 Family Street",
            "city": "Pasadena",
            "state": "CA",
            "zip_code": "91101",
            "country": "USA",
            "latitude": 34.1478,
            "longitude": -118.1445,
            "images": [
                "https://images.pexels.com/photos/1396132/pexels-photo-1396132.jpeg"
            ],
            "amenities": ["large_backyard", "updated_kitchen", "hardwood_floors", "family_room", "two_car_garage"],
            "year_built": 2005,
            "parking_spaces": 2,
            "owner_id": seller2["id"],
            "agent_id": agent1["id"],
            "is_featured": False,
            "views": 89,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Modern Apartment Building - Studio Units",
            "description": "Contemporary studio apartments in a vibrant urban setting. Perfect for young professionals seeking modern living with colorful architectural accents and convenient city access.",
            "property_type": "apartment",
            "status": "for_rent",
            "price": 2400.0,
            "bedrooms": 1,
            "bathrooms": 1,
            "area_sqft": 650.0,
            "address": "555 Urban Plaza, Unit 12A",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94102",
            "country": "USA",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "images": [
                "https://images.pexels.com/photos/439391/pexels-photo-439391.jpeg"
            ],
            "amenities": ["rooftop_deck", "fitness_center", "concierge", "bike_storage", "pet_friendly"],
            "year_built": 2022,
            "parking_spaces": 0,
            "owner_id": seller1["id"],
            "agent_id": agent2["id"],
            "is_featured": False,
            "views": 76,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Sleek Urban Apartment Complex",
            "description": "Modern apartment living in the heart of the city. These units feature contemporary design, large windows, and access to premium building amenities including fitness center and rooftop terrace.",
            "property_type": "apartment",
            "status": "for_rent",
            "price": 3200.0,
            "bedrooms": 2,
            "bathrooms": 2,
            "area_sqft": 1100.0,
            "address": "777 Downtown Circle, Unit 8B",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98101",
            "country": "USA",
            "latitude": 47.6062,
            "longitude": -122.3321,
            "images": [
                "https://images.pexels.com/photos/323705/pexels-photo-323705.jpeg"
            ],
            "amenities": ["city_views", "fitness_center", "rooftop_terrace", "in_unit_laundry", "doorman"],
            "year_built": 2021,
            "parking_spaces": 1,
            "owner_id": seller2["id"],
            "agent_id": agent1["id"],
            "is_featured": False,
            "views": 123,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Contemporary Multi-Unit Residential Building",
            "description": "Premium residential building offering luxury apartment living with modern architecture and high-end finishes. Located in a sought-after neighborhood with excellent walkability.",
            "property_type": "apartment",
            "status": "for_rent",
            "price": 2800.0,
            "bedrooms": 1,
            "bathrooms": 1,
            "area_sqft": 850.0,
            "address": "999 Residence Way, Unit 5C",
            "city": "Portland",
            "state": "OR",
            "zip_code": "97201",
            "country": "USA",
            "latitude": 45.5152,
            "longitude": -122.6784,
            "images": [
                "https://images.unsplash.com/photo-1612637968894-660373e23b03"
            ],
            "amenities": ["luxury_finishes", "walkable_location", "outdoor_space", "storage_unit", "bike_parking"],
            "year_built": 2023,
            "parking_spaces": 1,
            "owner_id": seller1["id"],
            "agent_id": agent2["id"],
            "is_featured": True,
            "views": 145,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Luxury Beachfront Property",
            "description": "Exclusive beachfront estate offering unparalleled ocean access and stunning sunset views. Features private beach access, expansive outdoor living spaces, and luxury amenities throughout.",
            "property_type": "villa",
            "status": "for_sale",
            "price": 4200000.0,
            "bedrooms": 6,
            "bathrooms": 5,
            "area_sqft": 5200.0,
            "address": "101 Oceanfront Drive",
            "city": "Newport Beach",
            "state": "CA",
            "zip_code": "92661",
            "country": "USA",
            "latitude": 33.6189,
            "longitude": -117.9298,
            "images": [
                "https://images.pexels.com/photos/1732414/pexels-photo-1732414.jpeg"
            ],
            "amenities": ["private_beach", "ocean_views", "infinity_pool", "outdoor_kitchen", "guest_quarters", "elevator"],
            "year_built": 2018,
            "parking_spaces": 4,
            "owner_id": seller2["id"],
            "agent_id": agent1["id"],
            "is_featured": True,
            "views": 289,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Modern Glass Office Tower",
            "description": "Premium commercial office space in a prestigious glass tower. Features state-of-the-art facilities, panoramic city views, and flexible floor plans suitable for businesses of all sizes.",
            "property_type": "commercial",
            "status": "for_rent",
            "price": 12000.0,
            "bedrooms": 0,
            "bathrooms": 3,
            "area_sqft": 3500.0,
            "address": "500 Business Plaza, Floor 15",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94111",
            "country": "USA",
            "latitude": 37.7946,
            "longitude": -122.3999,
            "images": [
                "https://images.pexels.com/photos/32802683/pexels-photo-32802683.png"
            ],
            "amenities": ["city_views", "high_speed_internet", "conference_rooms", "reception_area", "parking_garage"],
            "year_built": 2020,
            "parking_spaces": 15,
            "owner_id": seller1["id"],
            "agent_id": agent2["id"],
            "is_featured": False,
            "views": 67,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Contemporary Curved Glass Office Building",
            "description": "Striking curved glass office building offering premium commercial space with modern amenities. Perfect for companies seeking a prestigious address with flexible office configurations.",
            "property_type": "commercial",
            "status": "for_rent",
            "price": 8500.0,
            "bedrooms": 0,
            "bathrooms": 2,
            "area_sqft": 2200.0,
            "address": "750 Corporate Center, Suite 900",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701",
            "country": "USA",
            "latitude": 30.2672,
            "longitude": -97.7431,
            "images": [
                "https://images.pexels.com/photos/32763771/pexels-photo-32763771.jpeg"
            ],
            "amenities": ["modern_design", "elevator_access", "break_room", "IT_infrastructure", "visitor_parking"],
            "year_built": 2022,
            "parking_spaces": 8,
            "owner_id": seller2["id"],
            "agent_id": agent1["id"],
            "is_featured": False,
            "views": 43,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Cozy Lakeside Mountain Cabin",
            "description": "Charming wooden cabin nestled by a pristine mountain lake. Perfect for weekend getaways or year-round mountain living. Features rustic charm with modern conveniences and stunning natural views.",
            "property_type": "house",
            "status": "for_sale",
            "price": 485000.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "area_sqft": 1800.0,
            "address": "45 Lakeshore Trail",
            "city": "Lake Tahoe",
            "state": "CA",
            "zip_code": "96150",
            "country": "USA",
            "latitude": 39.0968,
            "longitude": -120.0324,
            "images": [
                "https://images.unsplash.com/photo-1482192505345-5655af888cc4"
            ],
            "amenities": ["lake_access", "mountain_views", "fireplace", "deck", "boat_dock", "hiking_trails"],
            "year_built": 1998,
            "parking_spaces": 2,
            "owner_id": seller1["id"],
            "agent_id": agent2["id"],
            "is_featured": True,
            "views": 156,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Rocky Mountain Log Cabin Retreat",
            "description": "Authentic log cabin retreat in the heart of the Rocky Mountains. Offers complete privacy and tranquility with access to world-class skiing, hiking, and outdoor recreation.",
            "property_type": "house",
            "status": "for_rent",
            "price": 450.0,  # Per night
            "bedrooms": 4,
            "bathrooms": 3,
            "area_sqft": 2200.0,
            "address": "789 Alpine Ridge Road",
            "city": "Aspen",
            "state": "CO",
            "zip_code": "81611",
            "country": "USA",
            "latitude": 39.1911,
            "longitude": -106.8175,
            "images": [
                "https://images.unsplash.com/photo-1583878594798-c31409c8ab4a"
            ],
            "amenities": ["hot_tub", "ski_access", "mountain_views", "wood_burning_stove", "game_room"],
            "year_built": 2010,
            "parking_spaces": 3,
            "owner_id": seller2["id"],
            "agent_id": agent1["id"],
            "is_featured": True,
            "views": 198,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Classic Historic Brownstone",
            "description": "Beautifully preserved historic brownstone with original architectural details and modern updates. Located in a tree-lined neighborhood with excellent walkability and charm.",
            "property_type": "house",
            "status": "for_sale",
            "price": 1350000.0,
            "bedrooms": 4,
            "bathrooms": 3,
            "area_sqft": 2600.0,
            "address": "234 Heritage Street",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02116",
            "country": "USA",
            "latitude": 42.3478,
            "longitude": -71.0755,
            "images": [
                "https://images.unsplash.com/photo-1728908636431-654c66cbe776"
            ],
            "amenities": ["historic_details", "original_hardwood", "exposed_brick", "roof_deck", "updated_kitchen"],
            "year_built": 1895,
            "parking_spaces": 1,
            "owner_id": seller1["id"],
            "agent_id": agent2["id"],
            "is_featured": True,
            "views": 112,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Traditional Brownstone Row Houses",
            "description": "Elegant row of traditional brownstone houses in a historic neighborhood. This unit features classic architecture with modern amenities and private outdoor space.",
            "property_type": "house",
            "status": "for_sale",
            "price": 980000.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "area_sqft": 2100.0,
            "address": "567 Historic Row",
            "city": "Philadelphia",
            "state": "PA",
            "zip_code": "19102",
            "country": "USA",
            "latitude": 39.9500,
            "longitude": -75.1667,
            "images": [
                "https://images.pexels.com/photos/5847592/pexels-photo-5847592.jpeg"
            ],
            "amenities": ["historic_charm", "private_garden", "original_molding", "updated_systems", "parking"],
            "year_built": 1910,
            "parking_spaces": 1,
            "owner_id": seller2["id"],
            "agent_id": agent1["id"],
            "is_featured": False,
            "views": 87,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Tropical Beachfront Vacation Home",
            "description": "Paradise found! This stunning beachfront vacation home offers direct beach access, tropical gardens, and panoramic ocean views. Perfect for vacation rentals or personal getaways.",
            "property_type": "villa",
            "status": "for_sale",
            "price": 1890000.0,
            "bedrooms": 4,
            "bathrooms": 3,
            "area_sqft": 2800.0,
            "address": "88 Paradise Beach Road",
            "city": "Key West",
            "state": "FL",
            "zip_code": "33040",
            "country": "USA",
            "latitude": 24.5557,
            "longitude": -81.7826,
            "images": [
                "https://images.unsplash.com/photo-1585544314038-a0d3769d0193"
            ],
            "amenities": ["beach_access", "tropical_garden", "outdoor_shower", "tiki_bar", "kayak_storage"],
            "year_built": 2016,
            "parking_spaces": 2,
            "owner_id": seller1["id"],
            "agent_id": agent2["id"],
            "is_featured": True,
            "views": 223,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Luxury Beachfront Vacation Property",
            "description": "Ultimate luxury beachfront estate perfect for vacation rentals or personal retreat. Features infinity pool, private beach access, and world-class amenities with stunning ocean views.",
            "property_type": "villa",
            "status": "for_rent",
            "price": 850.0,  # Per night
            "bedrooms": 5,
            "bathrooms": 4,
            "area_sqft": 3600.0,
            "address": "12 Oceanview Estates",
            "city": "Outer Banks",
            "state": "NC",
            "zip_code": "27959",
            "country": "USA",
            "latitude": 35.5582,
            "longitude": -75.4665,
            "images": [
                "https://images.pexels.com/photos/29334705/pexels-photo-29334705.jpeg"
            ],
            "amenities": ["infinity_pool", "private_beach", "gourmet_kitchen", "wine_cellar", "elevator", "chef_kitchen"],
            "year_built": 2019,
            "parking_spaces": 4,
            "owner_id": seller2["id"],
            "agent_id": agent1["id"],
            "is_featured": True,
            "views": 334,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ]
    
    # Clear existing properties and insert new ones
    await db.properties.delete_many({})
    await db.properties.insert_many(sample_properties)
    
    print(f"✅ Created {len(sample_properties)} sample properties with high-quality images")
    print(f"✅ Created {len(sample_users)} sample users")
    print("\nSample user credentials:")
    print("Seller 1: john.seller@example.com / password123")
    print("Seller 2: mike.seller@example.com / password123")
    print("Agent 1: jane.agent@example.com / password123")
    print("Agent 2: sarah.agent@example.com / password123")
    print("Buyer: bob.buyer@example.com / password123")

async def main():
    """Main function to seed the database"""
    try:
        print("🌱 Seeding Real Estate Database with High-Quality Images...")
        await create_sample_properties()
        print("✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())