import os  # Biblioteca de manipulação de diretórios e arquivos no sistema operacional
import re  # Biblioteca de operações com expressões regulares para manipular strings
from collections import defaultdict  # Estrutura de dados para agrupar elementos com chaves
from colorama import Fore, Style  # Biblioteca de formatação de texto colorido no terminal
from tkinter.filedialog import askdirectory  # Biblioteca de interface gráfica para seleção de diretórios
import shutil  # Biblioteca de operações de cópia e movimentação de arquivos

def extract_base_name(file_name):
    """
    Extrai o nome base de um arquivo, ignorando os parênteses e o restante do texto após eles.
    """
    return re.split(r'\s\(', file_name, maxsplit=1)[0]  # Divide o título no primeiro parêntese identificado e retorna a parte inicial

def select_best_file(files):
    """
    Seleciona o arquivo de menor comprimento em uma lista de arquivos.
    """
    return min(files, key=len)  # Retorna o arquivo que tiver o título mais curto

def filter_files(input_directory, output_directory):
    """
    Filtra arquivos de um diretório de entrada e copia os melhores arquivos para um diretório de saída.
    """
    # Printa o diretório de entrada e saída com formatação colorida do 'colorama'
    print(f"{Fore.CYAN}Analisando arquivos em: {input_directory}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Copiando para arquivos filtrados: {output_directory}{Style.RESET_ALL}")
    
    # Cria o diretório de saída se ele não existir
    os.makedirs(output_directory, exist_ok=True)
    
    files = os.listdir(input_directory)  # Lista todos os arquivos do diretório de entrada
    groups = defaultdict(list)  # Inicializa um dicionário que agrupa arquivos por nome base

    # Agrupa os arquivos pelo título base
    for file in files:
        base_name = extract_base_name(file)  # Obtém o nome base do arquivo
        groups[base_name].append(file)  # Adiciona o arquivo ao grupo correspondente

    # Processa cada grupo de arquivos
    for base_name, group_files in groups.items():
        best_file = select_best_file(group_files)  # Seleciona o melhor arquivo do grupo

        # Exibe o nome do grupo base no terminal
        print(f"{Fore.WHITE}\nGrupo Base: == {base_name} =={Style.RESET_ALL}")

        # Percorre os arquivos do grupo para copiar apenas o melhor e listar os ignorados
        for file in group_files:
            if file == best_file:
                # Definição dos caminhos de entrada e saída
                source_file = os.path.join(input_directory, file)
                destination_file = os.path.join(output_directory, file)
                shutil.copy2(source_file, destination_file)  # Copia o arquivo preservando metadados
                print(f"{Fore.GREEN}Mantido: {file}{Style.RESET_ALL}")  # Exibe que o arquivo foi mantido

        # Exibição dos arquivos ignorados via terminal
        for file in group_files:
            if file != best_file:
                print(f"{Fore.RED}Ignorado: {file}{Style.RESET_ALL}")  # Indica que o arquivo foi ignorado


# Seleção do diretório de entrada via UI
input_directory = askdirectory(title="Defina pasta de entrada")

# Seleção do diretório de saída via UI
output_directory = askdirectory(title="Defina pasta de saída")

# Chama a função principal para filtrar os arquivos
filter_files(input_directory, output_directory)
