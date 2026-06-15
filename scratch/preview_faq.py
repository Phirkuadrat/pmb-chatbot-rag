import fitz
import sys

def preview_pdf(pdf_path):
    print(f"Opening: {pdf_path}")
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
        
    print("--- 500 karakter pertama ---")
    print(text[:500])
    
    # Save to temp file to view if needed
    with open("scratch/temp_faq_preview.txt", "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    preview_pdf(r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\FAQ PMB Itenas 2026.pdf")
