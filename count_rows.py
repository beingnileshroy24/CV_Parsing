from docx import Document

def count_rows(file_path):
    doc = Document(file_path)
    for i, table in enumerate(doc.tables):
        print(f"Table {i} has {len(table.rows)} rows.")

if __name__ == "__main__":
    count_rows('test_table_output.docx')
