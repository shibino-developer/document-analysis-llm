from utils.retrieval.multi_query import MultiQueryRetriever

generator = MultiQueryRetriever()

queries = generator.generate(
    "Machine Learning"
)

for i, q in enumerate(queries, 1):

    print(f"{i}. {q}")