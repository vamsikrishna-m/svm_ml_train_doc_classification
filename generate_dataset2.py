import os
import fitz  
import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
import io

def extract_text_from_page(pdf_path, page_index):
    """
    Tries text extraction via pdfplumber; falls back to OCR if needed.
    Returns text and whether OCR was used.
    """
    text = None
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if page_index < len(pdf.pages):
                text = pdf.pages[page_index].extract_text()
                if text and text.strip():
                    return text.strip(), False
    except Exception as e:
        print(f"[WARN] pdfplumber failed on {pdf_path}, page {page_index}: {e}")

   
    try:
        doc = fitz.open(pdf_path)
        page = doc[page_index]
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        ocr_text = pytesseract.image_to_string(img)
        return ocr_text.strip(), True
    except Exception as e:
        print(f"[ERROR] OCR failed on {pdf_path}, page {page_index}: {e}")
        return "", True

def extract_all_pages(pdf_dir):
    """
    Loops through all PDFs and extracts page-wise text.
    Returns a list of dictionaries.
    """
    records = []
    

    for folder_name in os.listdir(pdf_dir):
        folder_path = os.path.join(pdf_dir, folder_name)
        if os.path.isdir(folder_path): 
            for filename in os.listdir(folder_path):
                if filename.endswith(".pdf"):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        doc = fitz.open(file_path)
                        for i in range(len(doc)):
                            text, ocr_used = extract_text_from_page(file_path, i)
                            records.append({
                                "file_name": filename,
                                "page_number": i + 1,
                                "text": text,
                                "ocr_used": ocr_used,
                                "label": folder_name  
                            })
                        print(f"[INFO] Processed: {filename} (Folder: {folder_name})")
                    except Exception as e:
                        print(f"[ERROR] Failed to process {filename}: {e}")
    return records

def save_to_csv(records, output_file="test_dataset_22.csv"):
    """
    Saves extracted data to CSV.
    """
    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)
    print(f"[✓] Saved extracted data to {output_file}")

if __name__ == "__main__":
    input_dir = input("Enter the parent folder path (e.g., ai or web): ").strip()
    data = extract_all_pages(input_dir)
    save_to_csv(data)




















































# import os
# import fitz  # PyMuPDF
# import pdfplumber
# import pytesseract
# from PIL import Image
# import pandas as pd
# import io

# def extract_text_from_page(pdf_path, page_index):
#     """
#     Tries text extraction via pdfplumber; falls back to OCR if needed.
#     Returns text and whether OCR was used.
#     """
#     text = None
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             if page_index < len(pdf.pages):
#                 text = pdf.pages[page_index].extract_text()
#                 if text and text.strip():
#                     return text.strip(), False
#     except Exception as e:
#         print(f"[WARN] pdfplumber failed on {pdf_path}, page {page_index}: {e}")

#     # Fallback to OCR using fitz + pytesseract
#     try:
#         doc = fitz.open(pdf_path)
#         page = doc[page_index]
#         pix = page.get_pixmap()
#         img = Image.open(io.BytesIO(pix.tobytes()))
#         ocr_text = pytesseract.image_to_string(img)
#         return ocr_text.strip(), True
#     except Exception as e:
#         print(f"[ERROR] OCR failed on {pdf_path}, page {page_index}: {e}")
#         return "", True

# def extract_all_pages(pdf_dir):
#     """
#     Loops through all PDFs and extracts page-wise text.
#     Returns a list of dictionaries.
#     """
#     records = []
#     for filename in os.listdir(pdf_dir):
#         if filename.endswith(".pdf"):
#             file_path = os.path.join(pdf_dir, filename)
#             try:
#                 doc = fitz.open(file_path)
#                 for i in range(len(doc)):
#                     text, ocr_used = extract_text_from_page(file_path, i)
#                     records.append({
#                         "file_name": filename,
#                         "page_number": i + 1,
#                         "text": text,
#                         "ocr_used": ocr_used
#                     })
#                 print(f"[INFO] Processed: {filename}")
#             except Exception as e:
#                 print(f"[ERROR] Failed to process {filename}: {e}")
#     return records

# def save_to_csv(records, output_file="test_dataset_22.csv"):
#     """
#     Saves extracted data to CSV.
#     """
#     df = pd.DataFrame(records)
#     df.to_csv(output_file, index=False)
#     print(f"[✓] Saved extracted data to {output_file}")

# if __name__ == "__main__":
#     input_dir = input("folders path").strip()
#     data = extract_all_pages(input_dir)
#     save_to_csv(data)
