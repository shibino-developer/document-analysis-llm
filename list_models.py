from google import genai
from config import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)

print("=" * 80)
print("Available Models")
print("=" * 80)

for model in client.models.list():
    print(model.name)