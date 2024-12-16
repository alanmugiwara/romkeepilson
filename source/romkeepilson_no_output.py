import os
import re
from collections import defaultdict
from colorama import Fore, Style
from tkinter.filedialog import askdirectory

def extract_base_name(file_name):
    """
    Extrai o nome base de um arquivo, ignorando os parênteses e regiões.
    """
    return re.split(r'\s\(', file_name, maxsplit=1)[0]

def select_best_file(files):
    """
    Seleciona o arquivo de menor comprimento de um grupo de arquivos.
    """
    return min(files, key=len)

def filter_files(directory):
    print(f"{Fore.CYAN}Analisando arquivos em: {directory}{Style.RESET_ALL}")
    
    files = os.listdir(directory)
    groups = defaultdict(list)

    # Agrupa arquivos pelo nome base
    for file in files:
        base_name = extract_base_name(file)
        groups[base_name].append(file)

    filtered_files = []

    for base_name, group_files in groups.items():
        best_file = select_best_file(group_files)
        filtered_files.append(best_file)

        print(f"{Fore.WHITE}\nGrupo Base: == {base_name} =={Style.RESET_ALL}")
        
        # Primeiro, exibe os arquivos mantidos
        for file in group_files:
            if file == best_file:
                print(f"{Fore.YELLOW}Mantido: {file}{Style.RESET_ALL}")

        # Depois, remove e exibe os arquivos removidos
        for file in group_files:
            if file != best_file:
                os.remove(os.path.join(directory, file))
                print(f"{Fore.RED}Removido: {file}{Style.RESET_ALL}")
               

# Seleção de pasta de entrada via interface gráfica
input_directory = askdirectory(title="Selecione o diretório de entrada com os arquivos")

# Realizando a filtragem dos arquivos na pasta de entrada
filter_files(input_directory)
