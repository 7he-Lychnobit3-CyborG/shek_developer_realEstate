from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app without a prefix
app = FastAPI(title="Real Estate API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enums
class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    VILLA = "villa"
    COMMERCIAL = "commercial"
    LAND = "land"

class PropertyStatus(str, Enum):
    FOR_SALE = "for_sale"
    FOR_RENT = "for_rent"
    SOLD = "sold"
    RENTED = "rented"

class UserRole(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"
    AGENT = "agent"

# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.BUYER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.BUYER

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class Property(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    property_type: PropertyType
    status: PropertyStatus
    price: float
    bedrooms: int
    bathrooms: int
    area_sqft: float
    address: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    images: List[str] = []
    amenities: List[str] = []
    year_built: Optional[int] = None
    parking_spaces: Optional[int] = None
    owner_id: str
    agent_id: Optional[str] = None
    is_featured: bool = False
    views: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PropertyCreate(BaseModel):
    title: str
    description: str
    property_type: PropertyType
    status: PropertyStatus
    price: float
    bedrooms: int
    bathrooms: int
    area_sqft: float
    address: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    images: List[str] = []
    amenities: List[str] = []
    year_built: Optional[int] = None
    parking_spaces: Optional[int] = None
    agent_id: Optional[str] = None
    is_featured: bool = False

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    property_type: Optional[PropertyType] = None
    status: Optional[PropertyStatus] = None
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    images: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    year_built: Optional[int] = None
    parking_spaces: Optional[int] = None
    is_featured: Optional[bool] = None

class Inquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    property_id: str
    user_id: str
    message: str
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    status: str = "new"  # new, contacted, closed
    created_at: datetime = Field(default_factory=datetime.utcnow)

class InquiryCreate(BaseModel):
    property_id: str
    message: str
    contact_email: EmailStr
    contact_phone: Optional[str] = None

class Favorite(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    property_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PropertySearch(BaseModel):
    query: Optional[str] = None
    property_type: Optional[PropertyType] = None
    status: Optional[PropertyStatus] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_bedrooms: Optional[int] = None
    max_bedrooms: Optional[int] = None
    min_bathrooms: Optional[int] = None
    max_bathrooms: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    is_featured: Optional[bool] = None
    page: int = 1
    limit: int = 20

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(**user)

# Authentication Routes
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.dict()
    del user_dict["password"]
    
    user = User(**user_dict)
    user_doc = user.dict()
    user_doc["hashed_password"] = hashed_password
    
    await db.users.insert_one(user_doc)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user_doc = await db.users.find_one({"email": user_credentials.email})
    if not user_doc or not verify_password(user_credentials.password, user_doc["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    user = User(**user_doc)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.get("/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# Property Routes
@api_router.post("/properties", response_model=Property)
async def create_property(property_data: PropertyCreate, current_user: User = Depends(get_current_user)):
    property_dict = property_data.dict()
    property_dict["owner_id"] = current_user.id
    
    property_obj = Property(**property_dict)
    await db.properties.insert_one(property_obj.dict())
    
    return property_obj

@api_router.get("/properties", response_model=List[Property])
async def get_properties(
    page: int = 1,
    limit: int = 20,
    property_type: Optional[PropertyType] = None,
    status: Optional[PropertyStatus] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    city: Optional[str] = None,
    is_featured: Optional[bool] = None
):
    skip = (page - 1) * limit
    filter_dict = {}
    
    if property_type:
        filter_dict["property_type"] = property_type
    if status:
        filter_dict["status"] = status
    if min_price is not None or max_price is not None:
        filter_dict["price"] = {}
        if min_price is not None:
            filter_dict["price"]["$gte"] = min_price
        if max_price is not None:
            filter_dict["price"]["$lte"] = max_price
    if city:
        filter_dict["city"] = {"$regex": city, "$options": "i"}
    if is_featured is not None:
        filter_dict["is_featured"] = is_featured
    
    properties = await db.properties.find(filter_dict).skip(skip).limit(limit).to_list(limit)
    return [Property(**prop) for prop in properties]

@api_router.get("/properties/{property_id}", response_model=Property)
async def get_property(property_id: str):
    property_doc = await db.properties.find_one({"id": property_id})
    if not property_doc:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Increment views
    await db.properties.update_one({"id": property_id}, {"$inc": {"views": 1}})
    property_doc["views"] += 1
    
    return Property(**property_doc)

@api_router.put("/properties/{property_id}", response_model=Property)
async def update_property(
    property_id: str, 
    property_update: PropertyUpdate, 
    current_user: User = Depends(get_current_user)
):
    property_doc = await db.properties.find_one({"id": property_id})
    if not property_doc:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if property_doc["owner_id"] != current_user.id and current_user.role != UserRole.AGENT:
        raise HTTPException(status_code=403, detail="Not authorized to update this property")
    
    update_dict = {k: v for k, v in property_update.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    await db.properties.update_one({"id": property_id}, {"$set": update_dict})
    
    updated_property = await db.properties.find_one({"id": property_id})
    return Property(**updated_property)

@api_router.delete("/properties/{property_id}")
async def delete_property(property_id: str, current_user: User = Depends(get_current_user)):
    property_doc = await db.properties.find_one({"id": property_id})
    if not property_doc:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if property_doc["owner_id"] != current_user.id and current_user.role != UserRole.AGENT:
        raise HTTPException(status_code=403, detail="Not authorized to delete this property")
    
    await db.properties.delete_one({"id": property_id})
    return {"message": "Property deleted successfully"}

# Inquiry Routes
@api_router.post("/inquiries", response_model=Inquiry)
async def create_inquiry(inquiry_data: InquiryCreate, current_user: User = Depends(get_current_user)):
    inquiry_dict = inquiry_data.dict()
    inquiry_dict["user_id"] = current_user.id
    
    inquiry_obj = Inquiry(**inquiry_dict)
    await db.inquiries.insert_one(inquiry_obj.dict())
    
    return inquiry_obj

@api_router.get("/inquiries", response_model=List[Inquiry])
async def get_inquiries(current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.BUYER:
        inquiries = await db.inquiries.find({"user_id": current_user.id}).to_list(1000)
    else:
        # For sellers and agents, get inquiries for their properties
        user_properties = await db.properties.find({"owner_id": current_user.id}).to_list(1000)
        property_ids = [prop["id"] for prop in user_properties]
        inquiries = await db.inquiries.find({"property_id": {"$in": property_ids}}).to_list(1000)
    
    return [Inquiry(**inquiry) for inquiry in inquiries]

# Favorites Routes
@api_router.post("/favorites/{property_id}")
async def add_to_favorites(property_id: str, current_user: User = Depends(get_current_user)):
    # Check if property exists
    property_doc = await db.properties.find_one({"id": property_id})
    if not property_doc:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Check if already in favorites
    existing_favorite = await db.favorites.find_one({
        "user_id": current_user.id,
        "property_id": property_id
    })
    if existing_favorite:
        raise HTTPException(status_code=400, detail="Property already in favorites")
    
    favorite = Favorite(user_id=current_user.id, property_id=property_id)
    await db.favorites.insert_one(favorite.dict())
    
    return {"message": "Property added to favorites"}

@api_router.delete("/favorites/{property_id}")
async def remove_from_favorites(property_id: str, current_user: User = Depends(get_current_user)):
    result = await db.favorites.delete_one({
        "user_id": current_user.id,
        "property_id": property_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    return {"message": "Property removed from favorites"}

@api_router.get("/favorites", response_model=List[Property])
async def get_favorites(current_user: User = Depends(get_current_user)):
    favorites = await db.favorites.find({"user_id": current_user.id}).to_list(1000)
    property_ids = [fav["property_id"] for fav in favorites]
    
    properties = await db.properties.find({"id": {"$in": property_ids}}).to_list(1000)
    return [Property(**prop) for prop in properties]

# Search and Filter Routes
@api_router.post("/properties/search", response_model=List[Property])
async def search_properties(search_params: PropertySearch):
    skip = (search_params.page - 1) * search_params.limit
    filter_dict = {}
    
    # Text search
    if search_params.query:
        filter_dict["$or"] = [
            {"title": {"$regex": search_params.query, "$options": "i"}},
            {"description": {"$regex": search_params.query, "$options": "i"}},
            {"address": {"$regex": search_params.query, "$options": "i"}},
            {"city": {"$regex": search_params.query, "$options": "i"}}
        ]
    
    # Filter by property type
    if search_params.property_type:
        filter_dict["property_type"] = search_params.property_type
    
    # Filter by status
    if search_params.status:
        filter_dict["status"] = search_params.status
    
    # Price range
    if search_params.min_price is not None or search_params.max_price is not None:
        filter_dict["price"] = {}
        if search_params.min_price is not None:
            filter_dict["price"]["$gte"] = search_params.min_price
        if search_params.max_price is not None:
            filter_dict["price"]["$lte"] = search_params.max_price
    
    # Bedrooms range
    if search_params.min_bedrooms is not None or search_params.max_bedrooms is not None:
        filter_dict["bedrooms"] = {}
        if search_params.min_bedrooms is not None:
            filter_dict["bedrooms"]["$gte"] = search_params.min_bedrooms
        if search_params.max_bedrooms is not None:
            filter_dict["bedrooms"]["$lte"] = search_params.max_bedrooms
    
    # Bathrooms range
    if search_params.min_bathrooms is not None or search_params.max_bathrooms is not None:
        filter_dict["bathrooms"] = {}
        if search_params.min_bathrooms is not None:
            filter_dict["bathrooms"]["$gte"] = search_params.min_bathrooms
        if search_params.max_bathrooms is not None:
            filter_dict["bathrooms"]["$lte"] = search_params.max_bathrooms
    
    # Area range
    if search_params.min_area is not None or search_params.max_area is not None:
        filter_dict["area_sqft"] = {}
        if search_params.min_area is not None:
            filter_dict["area_sqft"]["$gte"] = search_params.min_area
        if search_params.max_area is not None:
            filter_dict["area_sqft"]["$lte"] = search_params.max_area
    
    # Location filters
    if search_params.city:
        filter_dict["city"] = {"$regex": search_params.city, "$options": "i"}
    if search_params.state:
        filter_dict["state"] = {"$regex": search_params.state, "$options": "i"}
    
    # Featured properties
    if search_params.is_featured is not None:
        filter_dict["is_featured"] = search_params.is_featured
    
    properties = await db.properties.find(filter_dict).skip(skip).limit(search_params.limit).to_list(search_params.limit)
    return [Property(**prop) for prop in properties]

# Stats Routes
@api_router.get("/stats")
async def get_stats():
    total_properties = await db.properties.count_documents({})
    properties_for_sale = await db.properties.count_documents({"status": "for_sale"})
    properties_for_rent = await db.properties.count_documents({"status": "for_rent"})
    total_users = await db.users.count_documents({})
    
    return {
        "total_properties": total_properties,
        "properties_for_sale": properties_for_sale,
        "properties_for_rent": properties_for_rent,
        "total_users": total_users
    }

# General Routes
@api_router.get("/")
async def root():
    return {"message": "Real Estate API", "version": "1.0.0"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
