# -*- coding: utf-8 -*-
"""
Processador de Frequência Escolar
Ponto de entrada da aplicação
"""

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
