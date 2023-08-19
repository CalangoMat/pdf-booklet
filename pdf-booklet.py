import PyPDF2
from PyPDF2 import PageObject, PaperSize
import os, sys

def make_even(input_pdf_path):
    print("\n–– Verificando se o número de páginas é ímpar...")
    pdf_reader = PyPDF2.PdfReader(input_pdf_path)
    num_paginas = len(pdf_reader.pages)

    if num_paginas % 2 == 1:
        print("\tO número de páginas é ímpar. Adicionando uma página em branco...")
        pdf_writer = PyPDF2.PdfWriter()
        
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        blank_page = PageObject.create_blank_page(width=PaperSize.A4[0], height=PaperSize.A4[1])
        pdf_writer.add_page(blank_page)

        with open(input_pdf_path, 'wb') as output_pdf_file:
            pdf_writer.write(output_pdf_file)
        print("\tUma página em branco foi adicionada com sucesso.")
    else:
        print("\tO número de páginas é par. Nenhuma ação necessária.")

def reorganize_pdf(input_pdf_path, output_pdf_path, page_order, output_directory=sys.argv[1][:-4]):
    print(f"\n–––– Reorganizando o PDF {input_pdf_path} com base na ordem especificada...")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

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
    print(f"\tO PDF foi reorganizado e salvo em '{output_pdf_full_path}'.")

def booklet_order(input_pdf_path, output_directory):
    # print("\n–– Criando a ordem do livreto...")
    input_path = os.path.join(output_directory, input_pdf_path)

    with open(input_path, 'rb') as input_pdf:
        pdf_reader = PyPDF2.PdfReader(input_pdf)
        t = len(pdf_reader.pages)
        m = int(t/4)
        l = [[t-2*i,2*i+1] for i in range(2*m)]
        return (l[:m], l[m:][::-1]) 

def split_pdf(input_pdf_path, output_directory, block_size):
    print("\n–– Dividindo o PDF em blocos menores...")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

        with open(input_pdf_path, 'rb') as pdf_source:
            pdf_reader = PyPDF2.PdfReader(pdf_source)
            num_paginas = len(pdf_reader.pages)

            for i in range(0, num_paginas, block_size):
                pdf_writer = PyPDF2.PdfWriter()
                for j in range(i, min(i + block_size, num_paginas)):
                    page = pdf_reader.pages[j]
                    pdf_writer.add_page(page)

                nome_pdf_dividido = f'{(i+1)//block_size+1}.pdf'
                caminho_pdf_dividido = os.path.join(output_directory, nome_pdf_dividido)

                with open(caminho_pdf_dividido, 'wb') as pdf_output:
                    pdf_writer.write(pdf_output)

        print('\tDivisão concluída.')
    else:
        print(f"A pasta {output_directory} já existe!\nPor favor, exclua a pasta existente ou renomeie o arquivo PDF utilizado.")
        sys.exit(1)

def merge_pdf_list(pdf_names, chave):
    print(f"\n–– Mesclando PDFs com a chave '{chave}'...")
    pdf_writer = PyPDF2.PdfWriter()

    for pdf_name in pdf_names:
        with open(pdf_name, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
            os.remove(pdf_name)

    pdf_output = f'{sys.argv[1][:-4]}_{chave}.pdf'

    with open(pdf_output, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

    print(f'\tPDFs com a chave "{chave}" foram mesclados com sucesso.')

block_size = 24

# Verifica se pelo menos um argumento foi passado
if len(sys.argv) < 2:
    print("Uso: python3 mypdf.py arquivo_pdf.pdf")
    sys.exit(1)

# O primeiro argumento (sys.argv[0]) é o nome do script, então o arquivo PDF será o segundo argumento (sys.argv[1])
input_pdf_path = sys.argv[1]

# Diretório de destino para os PDFs divididos
output_directory = input_pdf_path[:-4]+'/'

# # Caminho para o PDF de entrada
# input_pdf_path = 'meupdf.pdf'

make_even(input_pdf_path)

split_pdf(input_pdf_path, output_directory, block_size)

# lista_arquivos = os.listdir(output_directory)
# arquivos = [arquivo[:-4] for arquivo in lista_arquivos if os.path.isfile(os.path.join(output_directory, arquivo))]

quantidade_arquivos = len(os.listdir(output_directory))
arquivos = [str(i+1) for i in range(quantidade_arquivos)]

# print('\n\n',arquivos,'\n\n')

for arquivo in arquivos:
    ordem_frontal, ordem_verso = booklet_order(arquivo + '.pdf', output_directory)

    output_pdf_path1 = arquivo + '_frontal.pdf'
    reorganize_pdf(arquivo + '.pdf', output_pdf_path1, ordem_frontal, output_directory)

    output_pdf_path2 = arquivo + '_verso.pdf'
    reorganize_pdf(arquivo + '.pdf', output_pdf_path2, ordem_verso, output_directory)

    caminho_pdf_original = os.path.join(output_directory, arquivo + '.pdf')
    os.remove(caminho_pdf_original)

# entra no diretório para que produza os arquivos finais
os.chdir(output_directory)

arquivos_frontal = [str(i+1)+'_frontal.pdf' for i in range(quantidade_arquivos)]
merge_pdf_list(arquivos_frontal, 'frontal')

arquivos_verso = [str(i+1)+'_verso.pdf' for i in range(quantidade_arquivos)]
merge_pdf_list(arquivos_verso, 'verso')
