# -*- coding: utf-8 -*-
"""
Processador de Frequência Escolar
Ponto de entrada da aplicação
"""

import sys
import subprocess
import os
import re

def verificar_e_instalar_requisitos():
    """Verifica e instala automaticamente os pacotes do requirements.txt"""
    
    # Verifica se o arquivo requirements.txt existe
    if not os.path.exists('requirements.txt'):
        print("Aviso: arquivo requirements.txt não encontrado")
        return
    
    print("Verificando dependências do requirements.txt...")
    
    # Lê os pacotes do requirements.txt
    pacotes_requeridos = []
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                # Ignora comentários e linhas vazias
                if linha and not linha.startswith('#'):
                    # Extrai apenas o nome do pacote (antes de >= ou ==)
                    pacote = re.split(r'[><=!]', linha)[0].strip()
                    pacotes_requeridos.append(pacote)
    except Exception as e:
        print(f"Erro ao ler requirements.txt: {e}")
        return
    
    # Verifica se todos os pacotes estão instalados
    pacotes_faltando = []
    for pacote in pacotes_requeridos:
        # Mapeamento de nomes especiais (PyMuPDF importa como fitz)
        nome_import = 'fitz' if pacote.lower() == 'pymupdf' else pacote.lower().replace('-', '_')
        
        try:
            __import__(nome_import)
        except ImportError:
            pacotes_faltando.append(pacote)
    
    if pacotes_faltando:
        print(f"Dependências faltando: {', '.join(pacotes_faltando)}")
        print("Instalando automaticamente...\n")
        
        try:
            # Instala todos os requisitos de uma vez
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                "requirements.txt",
                "--quiet"
            ])
            print("\n✓ Todas as dependências foram instaladas com sucesso!")
            print("Reiniciando a aplicação...\n")
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Erro ao instalar dependências: {e}")
            print("Tente instalar manualmente: pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("✓ Todas as dependências estão instaladas!\n")

# Executar verificação antes de importar os módulos da aplicação
verificar_e_instalar_requisitos()

import os
from interface import AplicativoFrequencia
import logica_app

def criar_estrutura_diretorios():
    if not os.path.exists('data'):
        os.makedirs('data')
    logica_app.inicializar_bancos()
    print("Bancos de dados SQLite inicializados")

def main():
    criar_estrutura_diretorios()
    app = AplicativoFrequencia()
    app.iniciar()

if __name__ == "__main__":
    main()