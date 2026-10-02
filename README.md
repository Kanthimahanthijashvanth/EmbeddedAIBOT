# EmbeddedAIBOT

# EmbeddedAIbot 🤖

A workshop-focused **Retrieval-Augmented Generation (RAG) application** that helps students understand technical workshop material from PDF and PowerPoint resources.

EmbeddedAIbot retrieves relevant information from the workshop documents, builds context, and generates grounded answers using a local LLM. Answers also include the relevant **slide/page sources**.

---

## 🚀 Features

* 📄 Supports **PDF and PowerPoint (PPTX)** workshop resources
* 🔍 Semantic search using vector embeddings
* 🧠 Retrieval-Augmented Generation (RAG)
* 🗂️ ChromaDB vector database
* 🤗 HuggingFace sentence-transformer embeddings
* 🦙 Local LLM inference using Ollama and Llama 3.2
* 🎯 Custom retrieval and keyword-aware reranking
* 🧩 Semantic text chunking
* 📊 Table extraction from PowerPoint slides
* 💻 Code-content detection
* 🖼️ PowerPoint image extraction support
* 📚 Slide/page-level source citations
* 🔒 Runs locally without sending workshop documents to an external LLM API

---

## 🏗️ Architecture

```text
                 Workshop Resources
                  PDF / PPTX
                      │
                      ▼
              ┌─────────────────┐
              │    Ingestion    │
              │  PDF / PPTX     │
              └────────┬────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │ Text / Code / Tables /   │
          │ Images + Metadata        │
          └────────────┬─────────────┘
                       │
                       ▼
                Semantic Chunking
                       │
                       ▼
             HuggingFace Embeddings
                       │
                       ▼
                  ChromaDB
                       │
                       │
User Query ────────────┘
       │
       ▼
   Retrieval
       │
       ▼
 Keyword-aware Reranking
       │
       ▼
  Context Builder
       │
       ▼
  Prompt Builder
       │
       ▼
 Ollama / Llama 3.2
       │
       ▼
 Answer + Sources
```

---

## 📁 Project Structure

```text
EmbeddedAIBOT/
│
├── root.ipynb
├── Modelfile
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── slide_parser.py
│   │   ├── code_detector.py
│   │   ├── image_extractor.py
│   │   ├── table_extractor.py
│   │   ├── slide_structure.py
│   │   └── ingestion_pipeline.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   ├── vector_store.py
│   │   └── unified_processor.py
│   │
│   └── rag/
│       ├── __init__.py
│       ├── retriever.py
│       ├── context_builder.py
│       ├── prompt.py
│       ├── response_builder.py
│       ├── rag_chain.py
│       ├── resource_formatter.py
│       └── llm.py
│
├── Data/          # Local workshop resources (ignored)
├── vector_db/     # Local Chroma database (ignored)
└── output/        # Generated files (ignored)
```

---

## 🔄 RAG Pipeline

### 1. Document Ingestion

Workshop PDF and PPTX resources are loaded and processed.

PowerPoint files are additionally analyzed for:

* Slide text
* Code
* Tables
* Images
* Slide metadata

### 2. Content Processing

The extracted content is converted into structured LangChain documents.

Text is divided into semantic chunks while preserving metadata such as:

```text
File
Slide / Page
Content Type
Workshop ID
Chunk ID
```

### 3. Embeddings

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The resulting embeddings are stored in ChromaDB.

### 4. Retrieval

For every user query:

```text
Query
  ↓
Semantic Search
  ↓
Candidate Documents
  ↓
Keyword-aware Reranking
  ↓
Top Relevant Documents
```

The retriever combines semantic similarity with technical keyword matching to improve retrieval for workshop-specific terminology.

### 5. Context Building

The most relevant documents are formatted into a structured context containing their source information.

### 6. LLM Generation

The retrieved context is passed to a local:

```text
Ollama
   ↓
Llama 3.2
```

The prompt instructs the model to answer using only information supported by the workshop material.

### 7. Response

The final response contains:

```text
Answer
+
Relevant Sources
```

Sources include the corresponding file and slide/page information.

---

## 🧰 Technology Stack

| Component               | Technology                          |
| ----------------------- | ----------------------------------- |
| Language                | Python                              |
| RAG Framework           | LangChain                           |
| Vector Database         | ChromaDB                            |
| Embeddings              | HuggingFace / Sentence Transformers |
| LLM                     | Llama 3.2                           |
| Local LLM Runtime       | Ollama                              |
| PDF Processing          | PyPDF                               |
| PowerPoint Processing   | python-pptx                         |
| Development Environment | JupyterLab                          |

---

## 📊 Current Corpus

The current workshop corpus contains:

* **25 resources**
* **3 PPTX files**
* **22 PDF files**
* **375 unique processed chunks**
* **363 text chunks**
* **12 table chunks**
* **0 duplicate chunks**

The workshop resources are kept locally and are **not included in this repository**.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/KanthimahanthiJashvanth/EmbeddedAIBOT.git
cd EmbeddedAIBOT
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is installed and running.

Pull the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Verify:

```bash
ollama list
```

---

## 📚 Add Workshop Data

Place your workshop PDF and PPTX files inside:

```text
Data/
```

The `Data/` directory is intentionally excluded from Git using `.gitignore`.

The generated vector database is stored locally in:

```text
vector_db/
```

and is also excluded from Git.

---

## ▶️ Running the Application

Open:

```text
root.ipynb
```

Initialize the assistant:

```python
bot = EmbeddedAIbot()
```

Then enter a question:

```python
query = input("You: ")

response = bot.ask(query)

bot.display(response)
```

Example:

```text
You: What is a Hardware Abstraction Layer?
```

The system retrieves relevant workshop material and generates an answer with its sources.

---

## 💡 Example Questions

```text
What is firmware architecture?
```

```text
What is the role of BSP?
```

```text
What is HAL?
```

```text
Explain the relationship between BSP, HAL, drivers and middleware.
```

```text
Explain the firmware development methodology discussed in the workshop.
```

---

## 🔐 Data & Privacy

EmbeddedAIbot is designed to run locally.

Workshop documents are processed locally and the LLM runs through Ollama.

The following directories are intentionally excluded from Git:

```text
Data/
vector_db/
output/
```

This prevents workshop resources and generated data from being uploaded to the repository.

---

## 🎯 Project Goal

The goal of EmbeddedAIbot is to make technical workshop material easier to explore by combining document retrieval with a locally running language model.

Instead of manually searching through multiple PDFs and PowerPoint presentations, users can ask questions in natural language and receive answers grounded in the workshop resources.

---

## 👨‍💻 Author

**Kanthimahanthi Jashvanth**

B.Tech — Electronics and Communication Engineering

---

## 📌 Future Improvements

* Improved multimodal retrieval for slide images
* Better code-resource retrieval
* Reranking using dedicated reranker models
* Conversation memory
* Streaming responses
* Web-based user interface
* Additional document formats
* Improved citation handling
* Custom Ollama model configuration
