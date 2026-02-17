from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from pdf_utils import extract_pages
from graph import build_graph

app = FastAPI()
graph = build_graph()


@app.post("/api/process")
async def process_claim(
    claim_id: str = Form(...),
    file: UploadFile = File(...)
):
    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    pages = extract_pages(temp_path)

    state = {
    "pages": pages,
    "assigned": {},
    "id_data": {},
    "discharge_data": {},
    "bill_data": {}
}



    result = graph.invoke(state)

    os.remove(temp_path)

    return {
        "claim_id": claim_id,
        "extracted_data": result
    }
