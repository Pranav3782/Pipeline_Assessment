import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv()

llm = ChatGroq(
    groq_api_key = os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0
)

SEGREGATOR_PROMPT = PromptTemplate.from_template("""
You are a document classifier.

Classify each page number into:
claim_forms, cheque_or_bank_details, identity_document, itemized_bill,
discharge_summary, prescription, investigation_report, cash_receipt, other

Return ONLY valid JSON.

Pages:
{pages}
""")

ID_PROMPT = PromptTemplate.from_template("""
Extract as JSON:
patient_name, dob, id_number, policy_number
Text:
{text}
""")

DISCHARGE_PROMPT = PromptTemplate.from_template("""
Extract as JSON:
diagnosis, admission_date, discharge_date, physician
Text:
{text}
""")

BILL_PROMPT = PromptTemplate.from_template("""
Extract JSON with:
items (list of description, qty, amount) and total_amount
Text:
{text}
""")


def segregate(pages):
    preview = "\n".join(
        f"Page {k}: {v[:600]}" for k, v in pages.items()
    )

    raw = llm.invoke(
        SEGREGATOR_PROMPT.format(pages=preview)
    ).content

    return json.loads(raw)


def extract_id(text):
    return llm.invoke(ID_PROMPT.format(text=text)).content


def extract_discharge(text):
    return llm.invoke(DISCHARGE_PROMPT.format(text=text)).content


def extract_bill(text):
    return llm.invoke(BILL_PROMPT.format(text=text)).content
