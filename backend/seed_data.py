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
    }
]

async def create_sample_properties():
    """Create sample properties"""
    
    # Insert users first
    await db.users.delete_many({})  # Clear existing users
    await db.users.insert_many(sample_users)
    
    # Get user IDs
    seller = await db.users.find_one({"role": "seller"})
    agent = await db.users.find_one({"role": "agent"})
    
    sample_properties = [
        {
            "id": str(uuid.uuid4()),
            "title": "Luxury Downtown Condo",
            "description": "Stunning downtown condo with city views, modern amenities, and prime location. Perfect for professionals.",
            "property_type": "apartment",
            "status": "for_sale",
            "price": 450000.0,
            "bedrooms": 2,
            "bathrooms": 2,
            "area_sqft": 1200.0,
            "address": "123 Main Street, Unit 15A",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "country": "USA",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "images": [
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5OTkiPkx1eHVyeSBDb25kbzwvdGV4dD48L3N2Zz4="
            ],
            "amenities": ["gym", "pool", "concierge", "parking", "balcony"],
            "year_built": 2018,
            "parking_spaces": 1,
            "owner_id": seller["id"],
            "agent_id": agent["id"],
            "is_featured": True,
            "views": 45,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Family Home in Suburban Paradise",
            "description": "Beautiful 4-bedroom family home in quiet neighborhood with excellent schools and parks nearby.",
            "property_type": "house",
            "status": "for_sale",
            "price": 675000.0,
            "bedrooms": 4,
            "bathrooms": 3,
            "area_sqft": 2800.0,
            "address": "456 Oak Avenue",
            "city": "Los Angeles",
            "state": "CA",
            "zip_code": "90210",
            "country": "USA",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "images": [
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5OTkiPkZhbWlseSBIb21lPC90ZXh0Pjwvc3ZnPg=="
            ],
            "amenities": ["garden", "garage", "fireplace", "deck", "basement"],
            "year_built": 2010,
            "parking_spaces": 2,
            "owner_id": seller["id"],
            "agent_id": agent["id"],
            "is_featured": True,
            "views": 78,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Modern Studio Apartment",
            "description": "Sleek studio apartment perfect for young professionals. Open floor plan with modern fixtures.",
            "property_type": "apartment",
            "status": "for_rent",
            "price": 2200.0,
            "bedrooms": 1,
            "bathrooms": 1,
            "area_sqft": 650.0,
            "address": "789 Urban Street, Unit 3B",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94102",
            "country": "USA",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "images": [
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5OTkiPk1vZGVybiBTdHVkaW88L3RleHQ+PC9zdmc+"
            ],
            "amenities": ["wifi", "laundry", "elevator", "security"],
            "year_built": 2020,
            "parking_spaces": 0,
            "owner_id": seller["id"],
            "agent_id": agent["id"],
            "is_featured": False,
            "views": 32,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Luxury Villa with Ocean View",
            "description": "Stunning oceanfront villa with panoramic views, private beach access, and luxury amenities throughout.",
            "property_type": "villa",
            "status": "for_sale",
            "price": 2500000.0,
            "bedrooms": 6,
            "bathrooms": 5,
            "area_sqft": 5200.0,
            "address": "321 Ocean Drive",
            "city": "Miami",
            "state": "FL",
            "zip_code": "33139",
            "country": "USA",
            "latitude": 25.7617,
            "longitude": -80.1918,
            "images": [
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5OTkiPk9jZWFuIFZpbGxhPC90ZXh0Pjwvc3ZnPg=="
            ],
            "amenities": ["pool", "spa", "wine_cellar", "home_theater", "guest_house", "private_beach"],
            "year_built": 2015,
            "parking_spaces": 4,
            "owner_id": seller["id"],
            "agent_id": agent["id"],
            "is_featured": True,
            "views": 156,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Cozy Mountain Cabin",
            "description": "Charming mountain retreat perfect for weekend getaways. Rustic charm with modern conveniences.",
            "property_type": "house",
            "status": "for_rent",
            "price": 150.0,  # Per night
            "bedrooms": 2,
            "bathrooms": 1,
            "area_sqft": 900.0,
            "address": "654 Pine Ridge Road",
            "city": "Aspen",
            "state": "CO",
            "zip_code": "81611",
            "country": "USA",
            "latitude": 39.1911,
            "longitude": -106.8175,
            "images": [
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5OTkiPk1vdW50YWluIENhYmluPC90ZXh0Pjwvc3ZnPg=="
            ],
            "amenities": ["fireplace", "hot_tub", "ski_storage", "mountain_view"],
            "year_built": 1995,
            "parking_spaces": 2,
            "owner_id": seller["id"],
            "agent_id": agent["id"],
            "is_featured": False,
            "views": 89,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Commercial Office Space",
            "description": "Prime commercial office space in the business district. Perfect for startups and established companies.",
            "property_type": "commercial",
            "status": "for_rent",
            "price": 5000.0,
            "bedrooms": 0,
            "bathrooms": 2,
            "area_sqft": 2000.0,
            "address": "888 Business Boulevard, Suite 200",
            "city": "Austin",
            "state": "TX",
            "zip_code": "73301",
            "country": "USA",
            "latitude": 30.2672,
            "longitude": -97.7431,
            "images": [
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5OTkiPk9mZmljZSBTcGFjZTwvdGV4dD48L3N2Zz4="
            ],
            "amenities": ["conference_room", "kitchen", "parking", "security", "elevator"],
            "year_built": 2008,
            "parking_spaces": 10,
            "owner_id": seller["id"],
            "agent_id": agent["id"],
            "is_featured": False,
            "views": 23,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Historic Brownstone",
            "description": "Beautifully restored historic brownstone with original details and modern updates. A rare find!",
            "property_type": "house",
            "status": "for_sale",
            "price": 1200000.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "area_sqft": 2200.0,
            "address": "147 Heritage Lane",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02101",
            "country": "USA",
            "latitude": 42.3601,
            "longitude": -71.0589,
            "images": [
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5OTkiPkJyb3duc3RvbmU8L3RleHQ+PC9zdmc+"
            ],
            "amenities": ["hardwood_floors", "exposed_brick", "rooftop_deck", "original_details"],
            "year_built": 1890,
            "parking_spaces": 1,
            "owner_id": seller["id"],
            "agent_id": agent["id"],
            "is_featured": True,
            "views": 67,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Lakefront Property",
            "description": "Serene lakefront property with private dock and swimming area. Perfect for nature lovers and water enthusiasts.",
            "property_type": "house",
            "status": "for_sale",
            "price": 850000.0,
            "bedrooms": 4,
            "bathrooms": 3,
            "area_sqft": 3200.0,
            "address": "99 Lakeshore Drive",
            "city": "Lake Tahoe",
            "state": "CA",
            "zip_code": "96150",
            "country": "USA",
            "latitude": 39.0968,
            "longitude": -120.0324,
            "images": [
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5OTkiPkxha2Vmcm9udDwvdGV4dD48L3N2Zz4="
            ],
            "amenities": ["private_dock", "beach_access", "boat_storage", "lake_view", "deck"],
            "year_built": 2005,
            "parking_spaces": 3,
            "owner_id": seller["id"],
            "agent_id": agent["id"],
            "is_featured": True,
            "views": 134,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ]
    
    # Clear existing properties and insert new ones
    await db.properties.delete_many({})
    await db.properties.insert_many(sample_properties)
    
    print(f"✅ Created {len(sample_properties)} sample properties")
    print(f"✅ Created {len(sample_users)} sample users")
    print("\nSample user credentials:")
    print("Seller: john.seller@example.com / password123")
    print("Agent: jane.agent@example.com / password123")
    print("Buyer: bob.buyer@example.com / password123")

async def main():
    """Main function to seed the database"""
    try:
        print("🌱 Seeding Real Estate Database...")
        await create_sample_properties()
        print("✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())