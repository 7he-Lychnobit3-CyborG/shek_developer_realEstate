import requests
import json
import unittest
import random
import string
import time

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://d6e68300-baa3-411d-a8fd-5067b0f10850.preview.emergentagent.com/api"

def random_string(length=8):
    """Generate a random string for test data"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class RealEstateAPITest(unittest.TestCase):
    """Test suite for the Real Estate API"""
    
    def setUp(self):
        """Setup for each test"""
        self.headers = {"Content-Type": "application/json"}
        self.auth_headers = {"Content-Type": "application/json"}
        self.test_user = {
            "email": f"test_{random_string()}@example.com",
            "password": "Password123!",
            "full_name": "Test User",
            "phone": "555-123-4567",
            "role": "buyer"
        }
        self.test_seller = {
            "email": f"seller_{random_string()}@example.com",
            "password": "Password123!",
            "full_name": "Test Seller",
            "phone": "555-987-6543",
            "role": "seller"
        }
        self.test_property = {
            "title": f"Test Property {random_string()}",
            "description": "A beautiful test property with amazing views",
            "property_type": "house",
            "status": "for_sale",
            "price": 350000.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "area_sqft": 2000.0,
            "address": "123 Test Street",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
            "country": "USA",
            "images": ["https://example.com/image1.jpg"],
            "amenities": ["pool", "garage", "garden"],
            "year_built": 2010,
            "parking_spaces": 2,
            "is_featured": True
        }
        self.property_ids = []
        self.user_id = None
        self.seller_id = None
        self.access_token = None
        self.seller_token = None
    
    def test_01_api_health(self):
        """Test API health endpoint"""
        response = requests.get(f"{BACKEND_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("version", data)
        print("✅ API health check passed")
    
    def test_02_register_user(self):
        """Test user registration"""
        response = requests.post(
            f"{BACKEND_URL}/auth/register",
            headers=self.headers,
            json=self.test_user
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertIn("user", data)
        self.assertEqual(data["token_type"], "bearer")
        self.user_id = data["user"]["id"]
        self.access_token = data["access_token"]
        self.auth_headers["Authorization"] = f"Bearer {self.access_token}"
        print("✅ User registration passed")
        
        # Register a seller user for property tests
        response = requests.post(
            f"{BACKEND_URL}/auth/register",
            headers=self.headers,
            json=self.test_seller
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.seller_id = data["user"]["id"]
        self.seller_token = data["access_token"]
        print("✅ Seller registration passed")
    
    def test_03_login(self):
        """Test user login"""
        login_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        }
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            headers=self.headers,
            json=login_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertIn("user", data)
        self.assertEqual(data["user"]["email"], self.test_user["email"])
        print("✅ User login passed")
    
    def test_04_get_current_user(self):
        """Test getting current user info"""
        response = requests.get(
            f"{BACKEND_URL}/auth/me",
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], self.test_user["email"])
        self.assertEqual(data["full_name"], self.test_user["full_name"])
        print("✅ Get current user passed")
    
    def test_05_create_property(self):
        """Test creating a new property"""
        # Use seller token for creating property
        seller_headers = self.headers.copy()
        seller_headers["Authorization"] = f"Bearer {self.seller_token}"
        
        response = requests.post(
            f"{BACKEND_URL}/properties",
            headers=seller_headers,
            json=self.test_property
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], self.test_property["title"])
        self.assertEqual(data["owner_id"], self.seller_id)
        self.property_ids.append(data["id"])
        print("✅ Create property passed")
        
        # Create a second property for testing
        self.test_property["title"] = f"Second Test Property {random_string()}"
        response = requests.post(
            f"{BACKEND_URL}/properties",
            headers=seller_headers,
            json=self.test_property
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.property_ids.append(data["id"])
        print("✅ Created second test property")
    
    def test_06_get_properties(self):
        """Test getting all properties"""
        response = requests.get(f"{BACKEND_URL}/properties")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print("✅ Get all properties passed")
        
        # Test with filters
        response = requests.get(
            f"{BACKEND_URL}/properties?property_type=house&status=for_sale&min_price=300000&max_price=400000"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print("✅ Get properties with filters passed")
    
    def test_07_get_property_by_id(self):
        """Test getting a specific property by ID"""
        if not self.property_ids:
            self.skipTest("No property IDs available")
        
        response = requests.get(f"{BACKEND_URL}/properties/{self.property_ids[0]}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.property_ids[0])
        print("✅ Get property by ID passed")
    
    def test_08_update_property(self):
        """Test updating a property"""
        if not self.property_ids:
            self.skipTest("No property IDs available")
        
        seller_headers = self.headers.copy()
        seller_headers["Authorization"] = f"Bearer {self.seller_token}"
        
        update_data = {
            "title": f"Updated Property {random_string()}",
            "price": 375000.0,
            "is_featured": True
        }
        
        response = requests.put(
            f"{BACKEND_URL}/properties/{self.property_ids[0]}",
            headers=seller_headers,
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], update_data["title"])
        self.assertEqual(data["price"], update_data["price"])
        self.assertEqual(data["is_featured"], update_data["is_featured"])
        print("✅ Update property passed")
    
    def test_09_search_properties(self):
        """Test property search functionality"""
        search_data = {
            "query": "Test Property",
            "property_type": "house",
            "status": "for_sale",
            "min_price": 300000,
            "max_price": 400000,
            "min_bedrooms": 2,
            "max_bedrooms": 4,
            "city": "Test City",
            "page": 1,
            "limit": 10
        }
        
        response = requests.post(
            f"{BACKEND_URL}/properties/search",
            headers=self.headers,
            json=search_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print("✅ Property search passed")
    
    def test_10_add_to_favorites(self):
        """Test adding a property to favorites"""
        if not self.property_ids:
            self.skipTest("No property IDs available")
        
        response = requests.post(
            f"{BACKEND_URL}/favorites/{self.property_ids[0]}",
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        print("✅ Add to favorites passed")
    
    def test_11_get_favorites(self):
        """Test getting user's favorite properties"""
        response = requests.get(
            f"{BACKEND_URL}/favorites",
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        print("✅ Get favorites passed")
    
    def test_12_remove_from_favorites(self):
        """Test removing a property from favorites"""
        if not self.property_ids:
            self.skipTest("No property IDs available")
        
        response = requests.delete(
            f"{BACKEND_URL}/favorites/{self.property_ids[0]}",
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        print("✅ Remove from favorites passed")
    
    def test_13_create_inquiry(self):
        """Test creating a property inquiry"""
        if not self.property_ids:
            self.skipTest("No property IDs available")
        
        inquiry_data = {
            "property_id": self.property_ids[0],
            "message": "I'm interested in this property. Please contact me.",
            "contact_email": self.test_user["email"],
            "contact_phone": "555-123-4567"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/inquiries",
            headers=self.auth_headers,
            json=inquiry_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["property_id"], self.property_ids[0])
        self.assertEqual(data["user_id"], self.user_id)
        print("✅ Create inquiry passed")
    
    def test_14_get_inquiries(self):
        """Test getting user's inquiries"""
        response = requests.get(
            f"{BACKEND_URL}/inquiries",
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        print("✅ Get inquiries passed")
        
        # Test seller getting inquiries for their properties
        seller_headers = self.headers.copy()
        seller_headers["Authorization"] = f"Bearer {self.seller_token}"
        
        response = requests.get(
            f"{BACKEND_URL}/inquiries",
            headers=seller_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print("✅ Seller get inquiries passed")
    
    def test_15_get_stats(self):
        """Test getting platform statistics"""
        response = requests.get(f"{BACKEND_URL}/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_properties", data)
        self.assertIn("properties_for_sale", data)
        self.assertIn("properties_for_rent", data)
        self.assertIn("total_users", data)
        print("✅ Get stats passed")
    
    def test_16_delete_property(self):
        """Test deleting a property"""
        if not self.property_ids or len(self.property_ids) < 2:
            self.skipTest("Not enough property IDs available")
        
        seller_headers = self.headers.copy()
        seller_headers["Authorization"] = f"Bearer {self.seller_token}"
        
        # Delete the second property
        response = requests.delete(
            f"{BACKEND_URL}/properties/{self.property_ids[1]}",
            headers=seller_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        print("✅ Delete property passed")
    
    def test_17_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        # Try to access a protected endpoint without authentication
        response = requests.get(f"{BACKEND_URL}/auth/me")
        self.assertEqual(response.status_code, 403)
        
        # Try to update a property without proper ownership
        if not self.property_ids:
            self.skipTest("No property IDs available")
        
        update_data = {"title": "Unauthorized Update"}
        response = requests.put(
            f"{BACKEND_URL}/properties/{self.property_ids[0]}",
            headers=self.auth_headers,  # Using buyer token instead of seller
            json=update_data
        )
        self.assertEqual(response.status_code, 403)
        print("✅ Unauthorized access tests passed")

if __name__ == "__main__":
    # Create a test suite with tests in specific order
    test_suite = unittest.TestSuite()
    test_suite.addTest(RealEstateAPITest('test_01_api_health'))
    test_suite.addTest(RealEstateAPITest('test_02_register_user'))
    test_suite.addTest(RealEstateAPITest('test_03_login'))
    test_suite.addTest(RealEstateAPITest('test_04_get_current_user'))
    test_suite.addTest(RealEstateAPITest('test_05_create_property'))
    test_suite.addTest(RealEstateAPITest('test_06_get_properties'))
    test_suite.addTest(RealEstateAPITest('test_07_get_property_by_id'))
    test_suite.addTest(RealEstateAPITest('test_08_update_property'))
    test_suite.addTest(RealEstateAPITest('test_09_search_properties'))
    test_suite.addTest(RealEstateAPITest('test_10_add_to_favorites'))
    test_suite.addTest(RealEstateAPITest('test_11_get_favorites'))
    test_suite.addTest(RealEstateAPITest('test_12_remove_from_favorites'))
    test_suite.addTest(RealEstateAPITest('test_13_create_inquiry'))
    test_suite.addTest(RealEstateAPITest('test_14_get_inquiries'))
    test_suite.addTest(RealEstateAPITest('test_15_get_stats'))
    test_suite.addTest(RealEstateAPITest('test_16_delete_property'))
    test_suite.addTest(RealEstateAPITest('test_17_unauthorized_access'))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)