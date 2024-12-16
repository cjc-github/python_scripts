import PyPDF2

# 切割pdf文件
def split_pdf(input_pdf, start_page, end_page, output_pdf):
    """切割 PDF 文件，从 start_page 到 end_page"""
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # print("pdf文件页数:", len(reader.pages))
        
        writer = PyPDF2.PdfWriter()

        for page in range(start_page - 1, end_page):  # 页码从 0 开始
            writer.add_page(reader.pages[page])

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)


# 合并pdf
def merge_pdfs(pdf_list, output_pdf):
    """合并多个 PDF 文件"""
    writer = PyPDF2.PdfWriter()

    for pdf in pdf_list:
        with open(pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in range(len(reader.pages)):
                writer.add_page(reader.pages[page])

    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)


# 示例使用
if __name__ == "__main__":
    # 切割示例
    split_pdf('DDGF_ISSTA24.pdf', 1, 2, 'page_1-2.pdf')  # 提取第1-2页
    split_pdf('DDGF_ISSTA24.pdf', 3, 4, 'page_3-4.pdf')  # 提取第3-4页

    # 合并示例
    merge_pdfs(['page_1-2.pdf', 'page_3-4.pdf'], 'page_1-4.pdf')