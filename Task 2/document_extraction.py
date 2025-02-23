import fitz  # PyMuPDF
import pdfplumber
import json
import os
import pandas as pd

def extract_text_from_pdf(pdf_path):
    text_data = {}
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            text_data[f"Page_{page_num+1}"] = page.get_text("text")
    return text_data

def extract_tables_from_pdf(pdf_path):
    table_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)
                table_data.append(df.to_dict(orient="records"))
    return table_data

def process_pdfs_in_folder(folder_path, output_json):
    extracted_data = {}

    for pdf_file in os.listdir(folder_path):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, pdf_file)
            print(f"Processing: {pdf_file}")

            extracted_data[pdf_file] = {
                "headers": extract_text_from_pdf(pdf_path),
                "list_items": extract_tables_from_pdf(pdf_path)
            }


    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)

    print(f"✅ Extraction Complete! JSON file saved as: {output_json}")

if __name__ == "__main__":
    folder_path = "documents"  # Set folder name where PDFs are stored

    if not os.path.exists(folder_path):
        print("❌ Error: Folder does not exist. Please check the path.")
    else:
        output_json = "extracted_data.json"
        process_pdfs_in_folder(folder_path, output_json)
