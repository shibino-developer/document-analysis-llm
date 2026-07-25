from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.vectorstore import VectorStoreService
from utils.llm import LLMService

print("=" * 80)
print("DOCUMENT ANALYSIS USING LLMs")
print("=" * 80)

# --------------------------------------------------------
# Load
# --------------------------------------------------------

loader = DocumentLoader()

with open("AI.pdf", "rb") as file:
    documents = loader.load(file)

print("Document Loaded")

# --------------------------------------------------------
# Clean
# --------------------------------------------------------

cleaner = TextCleaner()

documents = cleaner.clean(documents)

print("Cleaning Completed")

# --------------------------------------------------------
# Split
# --------------------------------------------------------

splitter = DocumentSplitter()

chunks = splitter.split(documents)

print("Chunks Created:", len(chunks))

# --------------------------------------------------------
# Vector Store
# --------------------------------------------------------

vector_store = VectorStoreService()

vector_store.create_vector_store(chunks)

print("Vector Store Ready")

# --------------------------------------------------------
# Question
# --------------------------------------------------------

question = "What are the applications of Artificial Intelligence?"

print()
print("Question")
print(question)

# --------------------------------------------------------
# Retrieve
# --------------------------------------------------------

results = vector_store.similarity_search(
    question,
    k=3
)

print()
print("Retrieved Chunks:", len(results))

# --------------------------------------------------------
# Gemini
# --------------------------------------------------------

llm = LLMService()

answer = llm.answer_question(
    results,
    question
)

print()

print("=" * 80)
print("ANSWER")
print("=" * 80)

print(answer)