import fitz
import sys

def preview_pdf(pdf_path):
    print(f"Opening: {pdf_path}")
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    for i in range(min(5, len(doc))):
        page = doc[i]
        text = page.get_text()
        print(f"--- Page {i+1} ---")
        print(text[:500])
        print("Images on this page:", len(page.get_images(full=True)))
        print("---------")

if __name__ == "__main__":
    preview_pdf(r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\Itenas-Edufair.pdf")
