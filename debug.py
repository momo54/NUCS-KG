import pdfplumber

def debug_pdf_page(pdf_path, page_number=256):  # 257 → index 256
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        print("[📄] Text extracted by pdfplumber on page 257:")
        print("-" * 60)
        text = page.extract_text()
        if text:
            for i, line in enumerate(text.splitlines()):
                print(f"{i:02d}: {repr(line)}")
        else:
            print("❌ No text extracted.")
        print("-" * 60)

# Appelle ta fonction
debug_pdf_page("./data/bok.pdf", page_number=256)
