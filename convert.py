import fitz

def replace_text_in_pdf(input_pdf_path, output_pdf_path, old_text, new_text):
    pdf_document = fitz.open(input_pdf_path)
    
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)  
        text_instances = page.search_for(old_text)  
        for inst in text_instances:
            rect = inst  
            page.add_rect_annot(rect) 
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))  

            page.insert_text((rect.x0, rect.y0), new_text, fontsize=12, color=(0, 0, 0))

    pdf_document.save(output_pdf_path)
    pdf_document.close()