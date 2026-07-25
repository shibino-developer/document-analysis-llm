from utils.llm import LLMService

print("=" * 60)
print("Testing Gemini")
print("=" * 60)

llm = LLMService()

response = llm.generate_response(
    "What is Artificial Intelligence?"
)

print("\nResponse:\n")
print(response)