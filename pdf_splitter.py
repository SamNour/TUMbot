import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfReader(path)
    for page in range(len(pdf.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page])

        output_filename = '{}_page_{}.pdf'.format(fname, page+1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(output_filename))

for root, dirs, files in os.walk("data"):
    for file in files:
        if file.endswith(".pdf"):
            split_pdf(os.path.join(root, file))