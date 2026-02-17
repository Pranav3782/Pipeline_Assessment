# Claim Processing Pipeline using FastAPI + LangGraph

This project is a multi-agent AI system that processes medical claim PDFs and extracts structured information using LangGraph orchestration.

The system classifies document pages using an AI-powered segregator and routes relevant pages to specialized extraction agents.

---

## 🚀 Features

- Upload claim PDF via FastAPI API
- AI Segregator classifies each page into document types
- Routes only relevant pages to extraction agents
- Extracts:
  - Identity Information
  - Discharge Summary
  - Itemized Hospital Bill
- Aggregates results into a clean JSON response
- Uses LangGraph for workflow orchestration
- Uses Groq LLM for fast inference

---

## 🧠 Workflow

START  
→ Segregator Agent (classifies pages)  
→ ID Agent  
→ Discharge Summary Agent  
→ Itemized Bill Agent  
→ Aggregator  
→ END  

Only relevant pages are sent to each agent.

---

## 📁 Project Structure

langchain/
├── main.py
├── graph.py
├── agents.py
├── pdf_utils.py
├── requirements.txt
└── .env


Open:

http://127.0.0.1:8000/docs

---

## 📤 API Usage

POST `/api/process`

Form Data:
- claim_id (string)
- file (PDF)

Returns extracted JSON data.

---

## 🧪 Tech Stack

- FastAPI
- LangGraph
- LangChain
- Groq LLM
- pdfplumber

---

## ✅ Output Example

```json
{
  "claim_id": "CLM-001",
  "extracted_data": {
    "identity": {...},
    "discharge": {...},
    "bill": {...}
  }
}
