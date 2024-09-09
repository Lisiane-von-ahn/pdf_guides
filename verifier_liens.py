import postgres
from util.dbLink import connect_db, get_files, get_formations, get_modules, get_sites, get_years
from util.util import generate_download_link, extraire_liens, liensNOk, liensOk, liensNOk_list, liensOk_list
from util.pdfmanage import convert_pdf_to_docx, generate_download_link_doc, generateTempFile
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

def process_file(file):
    file_name = file[0]
    file_content = file[1]
    file_id = file[2]

    print(file_name)

    generateTempFile(file_content, "pdf" in file_name)

    extension = "pdf" if "pdf" in file_name else "docx"
    
    liens = extraire_liens(f"temp.{extension}")
    
    update_liens(file_id, liens)

def update_liens(file_id, liens):
    if liens:
        bons = liensOk_list(liens)
        mauvais = len(liens) - len(bons)
        mauvais_list = [item for item in liens if item not in bons] 
        delim = " "
        res = delim.join(map(str, mauvais_list))
        postgres.update_liens(file_id, len(bons), mauvais, res)
    else:
        postgres.update_liens(file_id, 0, 0, "")

def process_file_by_fields(file_name,file_content,file_id):
    print(file_name)

    generateTempFile(file_content, "pdf" in file_name)

    extension = "pdf" if "pdf" in file_name else "docx"
    
    liens = extraire_liens(f"temp.{extension}")
    
    update_liens(file_id, liens)

def main():
    files = postgres.get_files()

    for file in files:
        process_file(file)

if __name__ == "__main__":
    main()
