from ocr_fr_detect_v2 import ocr_fr_detect_v2
import os

file_cache = set()

def pdf_path_extract(path: str):
    # Extract all pdf paths
    pdf_files = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                pdf_files[file] = os.path.join(root, file)
    return pdf_files

dict_paths = pdf_path_extract("dags/kpmg-pipeline/text_extractor/fr_text")

print(dict_paths)

from utils.upload_file import upload_file

for key, val in dict_paths.items():
    txt_file = os.path.basename(os.path.splitext(val)[0])
    if txt_file not in file_cache:
        upload_file(val, key)
        file_cache.add(txt_file)