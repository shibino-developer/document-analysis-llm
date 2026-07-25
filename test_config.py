from config import GOOGLE_API_KEY

print("=" * 50)

if GOOGLE_API_KEY:
    print("✅ API Key Loaded Successfully")
    print()
    print("First 10 characters:")
    print(GOOGLE_API_KEY[:10] + "...")
else:
    print("❌ API Key NOT Found")

print("=" * 50)