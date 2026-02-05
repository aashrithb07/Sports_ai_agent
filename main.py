import uvicorn
from fastapi import FastAPI
import os
from dotenv import load_dotenv  # Added this

# 🚨 CRITICAL: Load environment variables BEFORE importing app routes
# This ensures the API key is available when the AI model initializes
load_dotenv()

# TEST 1: Immediate Print
print("--- SCRIPT STARTED ---")

# Print check to see if key is found (only shows first 4 chars for safety)
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"🔑 API Key found: {api_key[:4]}****")
else:
    print("⚠️ WARNING: GOOGLE_API_KEY not found in .env file!")

try:
    from app.routes import router
    print("✅ Successfully imported routes from the app folder")
except Exception as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("TIP: Make sure you have a folder named 'app' with a file 'routes.py' inside it.")
    exit()

# Initialize FastAPI
app = FastAPI()
app.include_router(router)

print("🚀 Attempting to start server on http://127.0.0.1:8000")

# Run directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)