# 📄 Document Analysis using LLMs & RAG

An end-to-end **Document Analysis and Retrieval-Augmented Generation (RAG)** application that allows users to upload documents, process their content, retrieve relevant information, and generate grounded answers using Large Language Models (LLMs).

The project combines **document processing, semantic search, hybrid retrieval, cross-encoder reranking, prompt engineering, and Gemini-based answer generation** into a modular RAG pipeline.

---

## 🚀 Project Overview

Traditional LLM applications can struggle when answering questions about private or domain-specific documents because the required information may not exist in the model's training data.

This project addresses that problem using **Retrieval-Augmented Generation (RAG)**.

The application:

1. Loads documents such as PDF, DOCX, and TXT files.
2. Extracts and cleans the document text.
3. Splits documents into meaningful chunks.
4. Converts chunks into vector embeddings.
5. Stores embeddings in a FAISS vector database.
6. Retrieves relevant chunks for a user query.
7. Performs hybrid retrieval using semantic and keyword-based search.
8. Reranks retrieved results using a cross-encoder.
9. Builds a context-aware prompt.
10. Sends the retrieved context to a Gemini LLM.
11. Generates an answer grounded in the uploaded documents.

---

## 🏗️ RAG Architecture

```text
                    ┌─────────────────────┐
                    │      User Query     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Query Processing    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
     ┌─────────────────┐              ┌─────────────────┐
     │ Semantic Search │              │  BM25 Retrieval │
     │     (FAISS)     │              │    (Keywords)   │
     └────────┬────────┘              └────────┬────────┘
              │                                │
              └────────────────┬───────────────┘
                               ▼
                    ┌─────────────────────┐
                    │  Hybrid Retrieval   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Cross-Encoder       │
                    │     Reranking       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Relevant Context    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Prompt Construction │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Gemini LLM          │
                    │ Answer Generation   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Final Answer    │
                    └─────────────────────┘
```

---

## ✨ Key Features

### 📥 Multi-Format Document Loading

Supports processing of:

- PDF
- DOCX
- TXT

The document loader extracts the textual content and passes it to the processing pipeline.

### 🧹 Text Cleaning

Removes unnecessary formatting, whitespace, and noise before the text enters the chunking stage.

### ✂️ Intelligent Text Chunking

Large documents are divided into smaller chunks so that relevant information can be retrieved efficiently.

Chunking helps:

- Improve retrieval accuracy
- Reduce unnecessary context
- Control LLM token usage
- Improve response relevance

### 🧠 Embedding Generation

The project converts document chunks into numerical vector representations using Hugging Face sentence-transformer embeddings.

Current embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Embedding dimension:

```text
384
```

### 🗂️ FAISS Vector Store

FAISS is used for efficient similarity search over document embeddings.

The generated vector index is persisted locally and can be reused without embedding the same documents repeatedly.

Example:

```text
database/
└── faiss_index/
```

### 🔎 Semantic Retrieval

User queries are converted into embeddings and compared against document vectors to identify semantically relevant chunks.

### 🔤 BM25 Keyword Retrieval

BM25 provides keyword-based retrieval and helps identify documents/chunks containing important exact terms.

This complements semantic retrieval, particularly when the query contains:

- Names
- Technical terms
- Numbers
- IDs
- Exact phrases

### 🔀 Hybrid Retrieval

The system combines:

```text
Semantic Retrieval + BM25 Retrieval
```

to improve retrieval coverage and robustness.

### 🎯 Cross-Encoder Reranking

Retrieved candidates are passed through a cross-encoder reranker to improve the ordering of results based on query-document relevance.

This creates a pipeline similar to:

```text
Retrieve many candidates
        ↓
Rerank candidates
        ↓
Select best context
        ↓
Send to LLM
```

### 📝 Prompt Building

A dedicated prompt-building layer constructs the final LLM prompt using:

- User question
- Retrieved document context
- Instructions
- Answering constraints

This helps keep the generated answer grounded in the source documents.

### 🤖 LLM Answer Generation

Google Gemini is used as the final generation model.

The LLM receives the retrieved context and generates a natural-language answer.

The application is designed so that the LLM answers using the retrieved document information rather than relying solely on its pretrained knowledge.

### 🖥️ Streamlit Interface

Streamlit provides the application interface for document upload, querying, and displaying generated responses.

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| UI | Streamlit |
| LLM | Google Gemini |
| RAG | Retrieval-Augmented Generation |
| Embeddings | Hugging Face Sentence Transformers |
| Embedding Model | `all-MiniLM-L6-v2` |
| Vector Database | FAISS |
| Keyword Retrieval | BM25 |
| Reranking | Cross-Encoder |
| Frameworks/Libraries | LangChain / custom modular services |
| Document Formats | PDF, DOCX, TXT |
| Version Control | Git / GitHub |
| Environment | Python virtual environment |

---

## 📁 Project Structure

```text
Document-Analysis-using-LLMs/
│
├── app.py
├── config.py
├── loader.py
├── requirements.txt
├── .env
├── .gitignore
│
├── database/
│   └── faiss_index/
│
├── utils/
│   ├── embeddings.py
│   ├── vectorstore.py
│   ├── cleaner.py
│   ├── splitter.py
│   ├── llm.py
│   ├── prompt.py
│   │
│   └── retrieval/
│       ├── bm25.py
│       ├── hybrid.py
│       └── reranker.py
│
└── tests/
    ├── test_embedding.py
    ├── test_vectorstore.py
    └── test_llm.py
```

> The exact file structure may evolve as the project is further developed.

---

## 🔄 End-to-End Pipeline

### Step 1 — Document Upload

The user uploads a supported document.

```text
PDF / DOCX / TXT
       ↓
Document Loader
```

### Step 2 — Text Extraction

The loader extracts raw text from the uploaded document.

### Step 3 — Text Cleaning

Raw text is cleaned to remove unnecessary noise.

```text
Raw Text
   ↓
Cleaning
   ↓
Clean Text
```

### Step 4 — Chunking

The cleaned document is divided into smaller chunks.

```text
Document
   ↓
Text Chunks
   ↓
Chunk 1
Chunk 2
Chunk 3
...
```

### Step 5 — Embedding Generation

Each chunk is converted into a vector representation.

```text
Text Chunk
    ↓
Embedding Model
    ↓
384-dimensional Vector
```

### Step 6 — Vector Storage

The vectors are stored in FAISS.

```text
Chunk → Embedding → FAISS
```

### Step 7 — User Query

The user asks a natural-language question.

Example:

```text
"What are the main findings of this document?"
```

### Step 8 — Retrieval

The query is processed using:

```text
Semantic Search
      +
BM25 Search
      ↓
Hybrid Retrieval
```

### Step 9 — Reranking

Candidate chunks are reranked using a cross-encoder.

```text
Retrieved Chunks
       ↓
Cross Encoder
       ↓
Most Relevant Chunks
```

### Step 10 — Prompt Construction

The retrieved context is combined with the user question.

```text
System Instructions
        +
Retrieved Context
        +
User Question
        ↓
Final Prompt
```

### Step 11 — LLM Generation

The final prompt is sent to Gemini.

```text
Gemini
  ↓
Grounded Answer
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Document-Analysis-using-LLMs
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-flash-latest
```

Never commit your API key to GitHub.

Add `.env` to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

Typical workflow:

```text
Upload Document
      ↓
Process Document
      ↓
Create Embeddings
      ↓
Store in FAISS
      ↓
Ask Question
      ↓
Retrieve Context
      ↓
Rerank Results
      ↓
Generate Answer
```

---

## 🧪 Testing

Individual components can be tested separately.

### Test Embeddings

```bash
python tests/test_embedding.py
```

Expected behavior:

```text
Embedding model loaded successfully
Vector dimension: 384
```

### Test Vector Store

```bash
python tests/test_vectorstore.py
```

Expected pipeline:

```text
Loading Document
Cleaning Text
Splitting Chunks
Creating Embeddings
Saving FAISS Index
```

### Test LLM

```bash
python tests/test_llm.py
```

This verifies Gemini configuration and LLM response generation.

---

## 🧩 Core Components

### `loader.py`

Responsible for loading supported document formats.

```text
PDF
DOCX
TXT
 ↓
Extracted Text
```

### `utils/cleaner.py`

Responsible for cleaning extracted text.

### `utils/splitter.py`

Responsible for dividing documents into manageable chunks.

### `utils/embeddings.py`

Responsible for generating embeddings using Hugging Face sentence-transformer models.

### `utils/vectorstore.py`

Responsible for:

- Creating the FAISS index
- Adding embeddings
- Saving the index
- Loading the index
- Similarity search

### `utils/retrieval/bm25.py`

Implements keyword-based BM25 retrieval.

### `utils/retrieval/hybrid.py`

Combines semantic retrieval with BM25 retrieval.

### `utils/retrieval/reranker.py`

Uses a cross-encoder to rerank retrieved candidates.

### `utils/prompt.py`

Responsible for constructing prompts containing the relevant document context and user query.

### `utils/llm.py`

Handles communication with the Gemini API and generates the final answer.

### `app.py`

Acts as the main Streamlit application layer.

---

## 📊 Retrieval Strategy

The project uses a multi-stage retrieval architecture:

```text
                User Query
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    Semantic Search        BM25 Search
       (FAISS)              (Keyword)
          │                   │
          └─────────┬─────────┘
                    ▼
             Hybrid Retrieval
                    │
                    ▼
             Candidate Chunks
                    │
                    ▼
            Cross-Encoder
              Reranking
                    │
                    ▼
            Top Relevant Chunks
                    │
                    ▼
                 Gemini
```

This architecture is designed to improve retrieval quality compared with relying on a single retrieval technique.

---

## 🧠 Why RAG?

A normal LLM pipeline looks like:

```text
User Question
      ↓
     LLM
      ↓
    Answer
```

A RAG pipeline instead uses external knowledge:

```text
User Question
      ↓
   Retriever
      ↓
Relevant Documents
      ↓
     LLM
      ↓
Grounded Answer
```

This provides several advantages:

- Better answers for private documents
- Reduced dependence on model memory
- More relevant context
- Easier knowledge updates
- Lower need for model fine-tuning
- Better control over the information supplied to the LLM

---

## 🎯 Example Use Cases

This system can be adapted for:

- 📚 Research paper analysis
- 📄 Company document analysis
- 🏥 Medical document analysis
- ⚖️ Legal document analysis
- 📑 Resume analysis
- 📖 Study material Q&A
- 🏢 Enterprise knowledge bases
- 📋 Policy and compliance documents
- 🔍 Technical documentation search
- 🧾 Report analysis

> For sensitive domains such as medical or legal applications, generated answers should be treated as informational and reviewed by qualified professionals.

---

## 🔮 Future Improvements

Planned or possible improvements include:

- [ ] Advanced document metadata handling
- [ ] Better chunking strategies
- [ ] Query rewriting
- [ ] Multi-query retrieval
- [ ] Parent-child document retrieval
- [ ] Retrieval evaluation metrics
- [ ] Faithfulness and answer-quality evaluation
- [ ] Source/citation display in answers
- [ ] Conversation memory
- [ ] Multiple-document comparison
- [ ] Support for tables and images
- [ ] OCR for scanned documents
- [ ] Streaming LLM responses
- [ ] Authentication and user management
- [ ] Docker deployment
- [ ] Cloud deployment
- [ ] Production-grade observability
- [ ] Automated CI/CD pipeline

---

## 📈 Future Production Architecture

A production version could evolve toward:

```text
                    ┌───────────────┐
                    │    Frontend   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   FastAPI     │
                    │   Backend     │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        Document       Retrieval       LLM
        Processing       Service       Service
              │             │             │
              ▼             ▼             ▼
          Storage        Vector DB      Gemini
                            │
                            ▼
                         Reranker
```

Potential production technologies:

- FastAPI
- PostgreSQL
- Redis
- FAISS / ChromaDB / other vector databases
- Docker
- GitHub Actions
- Cloud deployment
- Monitoring and logging

---

## 🔒 Security Considerations

Before deploying this project publicly or commercially:

- Never expose API keys.
- Validate uploaded files.
- Restrict supported file types.
- Enforce file-size limits.
- Sanitize extracted content.
- Protect user documents.
- Implement authentication and authorization.
- Avoid logging sensitive document content.
- Secure API endpoints.
- Apply rate limiting.

---

## 📚 Concepts Demonstrated

This project demonstrates practical knowledge of:

### Python

- Modular programming
- Object-oriented design
- File handling
- Environment configuration
- Exception handling

### NLP / LLM

- Tokenization concepts
- Text preprocessing
- Text chunking
- Embeddings
- Prompt engineering
- LLM inference

### RAG

- Document ingestion
- Vector search
- Semantic retrieval
- Keyword retrieval
- Hybrid retrieval
- Reranking
- Context construction
- Grounded generation

### AI Engineering

- LLM integration
- Retrieval pipelines
- Modular AI architecture
- Evaluation considerations
- Application deployment concepts

---

## 👨‍💻 Author

**Shibino P Abraham**

Python Developer | Backend Developer | AI/ML Engineer

Kerala, India

### Areas of Interest

- Python Development
- Backend Engineering
- Django & REST APIs
- Artificial Intelligence
- Machine Learning
- Generative AI
- LLM Applications
- Retrieval-Augmented Generation
- NLP

---

## ⭐ Project Highlights

> **Document Analysis using LLMs & RAG** is a practical AI engineering project demonstrating how documents can be transformed into searchable knowledge and used by an LLM to generate context-aware answers.

The project focuses not only on calling an LLM API, but on building the **complete retrieval pipeline around the LLM**:

```text
Documents
   ↓
Cleaning
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Database
   ↓
Hybrid Retrieval
   ↓
Reranking
   ↓
Prompt Engineering
   ↓
LLM
   ↓
Grounded Answer
```

---

## 📜 License

This project is intended for educational, portfolio, and development purposes.

Add an appropriate open-source license before distributing the project publicly.
