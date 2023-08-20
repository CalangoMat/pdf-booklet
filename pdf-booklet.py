import PyPDF2
from PyPDF2 import PageObject, PaperSize
import os, sys

# Function to check and add a blank page if the number of pages is odd
def make_even(input_pdf_path):
    print("\n–– Checking if the number of pages is odd.")
    pdf_reader = PyPDF2.PdfReader(input_pdf_path)
    num_pages = len(pdf_reader.pages)

    if num_pages % 2 == 1:
        print("\tThe number of pages is odd. Adding a blank page to make it even.")
        pdf_writer = PyPDF2.PdfWriter()
        
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        blank_page = PageObject.create_blank_page(width=PaperSize.A4[0], height=PaperSize.A4[1])
        pdf_writer.add_page(blank_page)

        with open(input_pdf_path, 'wb') as output_pdf_file:
            pdf_writer.write(output_pdf_file)
        print("\tA blank page was successfully added.")
    else:
        print("\tThe number of pages is even. No action needed.")

# Function to reorganize PDF pages based on a specified order
def reorganize_pdf(input_pdf_path, output_pdf_path, page_order, output_directory = sys.argv[1][:-4]):
    print(f"\n–––– Reorganizing the PDF {input_pdf_path} based on the specified order.")

    input_pdf_full_path = os.path.join(output_directory, input_pdf_path)
    output_pdf_full_path = os.path.join(output_directory, output_pdf_path)

    with open(input_pdf_full_path, 'rb') as input_pdf:
        pdf_reader = PyPDF2.PdfReader(input_pdf)
        pdf_writer = PyPDF2.PdfWriter()

        for pair in page_order:
            left_page_num, right_page_num = pair
            pdf_writer.add_page(pdf_reader.pages[left_page_num - 1])
            pdf_writer.add_page(pdf_reader.pages[right_page_num - 1])

        with open(output_pdf_full_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
            
    print(f"\tThe PDF has been reorganized and saved to '{output_pdf_full_path}'.")

# Function to create a booklet order for PDF pages
def booklet_order(input_pdf_path, output_directory):
    # print("\n–– Creating the booklet order...")
    input_path = os.path.join(output_directory, input_pdf_path)

    with open(input_path, 'rb') as input_pdf:
        pdf_reader = PyPDF2.PdfReader(input_pdf)
        t = len(pdf_reader.pages)
        m = int(t/4)
        l = [[t-2*i,2*i+1] for i in range(2*m)]
        return (l[:m], l[m:][::-1]) 

# Function to split a PDF into smaller blocks
def split_pdf(input_pdf_path, output_directory, block_size):
    print("\n–– Splitting the PDF into smaller blocks...")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

        with open(input_pdf_path, 'rb') as pdf_source:
            pdf_reader = PyPDF2.PdfReader(pdf_source)
            num_pages = len(pdf_reader.pages)

            for i in range(0, num_pages, block_size):
                pdf_writer = PyPDF2.PdfWriter()
                for j in range(i, min(i + block_size, num_pages)):
                    page = pdf_reader.pages[j]
                    pdf_writer.add_page(page)

                divided_pdf_name = f'{(i+1)//block_size+1}.pdf'
                divided_pdf_path = os.path.join(output_directory, divided_pdf_name)

                with open(divided_pdf_path, 'wb') as pdf_output:
                    pdf_writer.write(pdf_output)

        print('\tDivision completed.')
    else:
        print(f"The folder {output_directory} already exists!\nPlease delete the existing folder or rename the used PDF file.")
        sys.exit(1)

# Function to merge a list of PDF files
def merge_pdf_list(pdf_names, chave):
    print(f"\n–– Merging PDFs with the key '{chave}'...")

    merger = PyPDF2.PdfMerger()

    for pdf in pdf_names:
        merger.append(pdf)
        os.remove(pdf)

    pdf_output = f'{sys.argv[1][:-4]}_{chave}.pdf'
    merger.write(pdf_output)
    merger.close()

    print(f'\tPDFs with the key "{chave}" have been successfully merged.')

block_size = 24

# Check if at least one argument was passed
if len(sys.argv) < 2:
    print("Usage: pdf-booklet input_pdf.pdf")
    sys.exit(1)

# The first argument (sys.argv[0]) is the name of the script, so the PDF file will be the second argument (sys.argv[1])
input_pdf_path = sys.argv[1]

# Output directory for split PDFs
output_directory = input_pdf_path[:-4]+'/'

make_even(input_pdf_path)

split_pdf(input_pdf_path, output_directory, block_size)

quantidade_arquivos = len(os.listdir(output_directory))
arquivos = [str(i+1) for i in range(quantidade_arquivos)]

for arquivo in arquivos:
    ordem_frontal, ordem_verso = booklet_order(arquivo + '.pdf', output_directory)

    output_pdf_path1 = arquivo + '_frontal.pdf'
    reorganize_pdf(arquivo + '.pdf', output_pdf_path1, ordem_frontal, output_directory)

    output_pdf_path2 = arquivo + '_verso.pdf'
    reorganize_pdf(arquivo + '.pdf', output_pdf_path2, ordem_verso, output_directory)

    caminho_pdf_original = os.path.join(output_directory, arquivo + '.pdf')
    os.remove(caminho_pdf_original)

# Change to the directory to produce the final files
os.chdir(output_directory)

arquivos_frontal = [str(i+1)+'_frontal.pdf' for i in range(quantidade_arquivos)]
merge_pdf_list(arquivos_frontal, 'frontal')

arquivos_verso = [str(i+1)+'_verso.pdf' for i in range(quantidade_arquivos)]
merge_pdf_list(arquivos_verso, 'verso')

os.system(f'pdfjam --quiet --nup 2x1 {sys.argv[1][:-4]}_frontal.pdf --outfile {sys.argv[1][:-4]}_frontal_twopage.pdf --landscape')
os.system(f'pdfjam --quiet --nup 2x1 {sys.argv[1][:-4]}_verso.pdf --outfile {sys.argv[1][:-4]}_verso_twopage.pdf --landscape')
