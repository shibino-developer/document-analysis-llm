from utils.loader import DocumentLoader
from utils.cleaner import TextCleaner
from utils.splitter import DocumentSplitter
from utils.prompt import PromptBuilder

loader = DocumentLoader()

with open("AI.pdf", "rb") as file:
    documents = loader.load(file)

cleaner = TextCleaner()
documents = cleaner.clean(documents)

splitter = DocumentSplitter()
chunks = splitter.split(documents)

question = "What is Artificial Intelligence?"

prompt = PromptBuilder.build_from_documents(
    chunks[:2],
    question
)

print("=" * 80)
print(prompt)
print("=" * 80)