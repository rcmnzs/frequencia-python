# -*- coding: utf-8 -*-
"""
Script para recriar todos os arquivos do sistema com encoding correto
Execute: python recriar_sistema.py
"""

import os

# Criar diretório data
os.makedirs('data', exist_ok=True)

# ============ MAIN.PY ============
main_content = '''# -*- coding: utf-8 -*-
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
'''

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(main_content)
print("✓ main.py criado")

# ============ LOGICA_APP.PY ============
# (Use o conteúdo do artifact logica_fix que criei anteriormente)
print("✓ Copie o conteúdo do artifact 'logica_fix' para logica_app.py")

# ============ INTERFACE.PY - VERSÃO SIMPLIFICADA ============
interface_content = '''# -*- coding: utf-8 -*-
"""Interface gráfica do sistema"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
import logica_app as logica

class AplicativoFrequencia:
    def __init__(self):
        self.janela = ttk.Window(themename="cosmo")
        self.janela.title("Processador de Frequência Escolar")
        self.janela.geometry("1100x750")
        
        self.pdf_frequencia = None
        self.pdf_ausentes = None
        self.pagina_alunos = 0
        self.pagina_horarios = 0
        self.pagina_faltas = 0
        self.itens_por_pagina = 50
        
        self.criar_interface()
    
    def criar_interface(self):
        self.notebook = ttk.Notebook(self.janela)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.criar_aba_processar()
        self.criar_aba_alunos()
        self.criar_aba_horarios()
        self.criar_aba_faltas()
    
    def criar_aba_processar(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Processar Frequência")
        
        frame_arquivos = ttk.LabelFrame(aba, text="Selecionar Arquivos PDF", padding=15)
        frame_arquivos.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(frame_arquivos, text="PDF de Frequência:").grid(row=0, column=0, sticky=W, pady=5)
        self.label_pdf_freq = ttk.Label(frame_arquivos, text="Nenhum arquivo", foreground="gray")
        self.label_pdf_freq.grid(row=0, column=1, sticky=W, padx=10)
        ttk.Button(frame_arquivos, text="Selecionar", command=self.selecionar_pdf_frequencia, bootstyle=INFO).grid(row=0, column=2, padx=5)
        
        ttk.Label(frame_arquivos, text="PDF de Ausentes:").grid(row=1, column=0, sticky=W, pady=5)
        self.label_pdf_aus = ttk.Label(frame_arquivos, text="Nenhum arquivo", foreground="gray")
        self.label_pdf_aus.grid(row=1, column=1, sticky=W, padx=10)
        ttk.Button(frame_arquivos, text="Selecionar", command=self.selecionar_pdf_ausentes, bootstyle=INFO).grid(row=1, column=2, padx=5)
        
        frame_data = ttk.LabelFrame(aba, text="Data", padding=15)
        frame_data.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(frame_data, text="Data (DD/MM/AAAA):").pack(side=LEFT, padx=5)
        self.entry_data = ttk.Entry(frame_data, width=15)
        self.entry_data.pack(side=LEFT, padx=5)
        ttk.Button(frame_data, text="Processar", command=self.processar_frequencia, bootstyle=SUCCESS).pack(side=LEFT, padx=20)
        
        frame_resultados = ttk.LabelFrame(aba, text="Faltas do Dia", padding=10)
        frame_resultados.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        colunas = ['Matrícula', 'Nome', 'Turma', 'Disciplina']
        self.tree_processar = ttk.Treeview(frame_resultados, columns=colunas, show='headings', height=15)
        
        for col in colunas:
            self.tree_processar.heading(col, text=col)
            self.tree_processar.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=VERTICAL, command=self.tree_processar.yview)
        self.tree_processar.configure(yscrollcommand=scrollbar.set)
        self.tree_processar.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    def selecionar_pdf_frequencia(self):
        arquivo = filedialog.askopenfilename(title="PDF de Frequência", filetypes=[("PDF", "*.pdf")])
        if arquivo:
            self.pdf_frequencia = arquivo
            self.label_pdf_freq.config(text=arquivo.split('/')[-1], foreground="black")
    
    def selecionar_pdf_ausentes(self):
        arquivo = filedialog.askopenfilename(title="PDF de Ausentes", filetypes=[("PDF", "*.pdf")])
        if arquivo:
            self.pdf_ausentes = arquivo
            self.label_pdf_aus.config(text=arquivo.split('/')[-1], foreground="black")
    
    def processar_frequencia(self):
        try:
            if not self.entry_data.get():
                Messagebox.show_warning("Informe a data!", "Aviso")
                return
            
            lista_presentes = []
            lista_ausentes = []
            
            if self.pdf_frequencia:
                lista_presentes = logica.extrair_matriculas_presentes(self.pdf_frequencia)
            
            if self.pdf_ausentes:
                lista_ausentes = logica.extrair_matriculas_ausentes(self.pdf_ausentes)
            
            faltas = logica.processar_faltas_do_dia(self.entry_data.get(), lista_presentes, lista_ausentes)
            
            for item in self.tree_processar.get_children():
                self.tree_processar.delete(item)
            
            for falta in faltas:
                self.tree_processar.insert('', END, values=(
                    falta['matricula'], falta['nome'], falta['turma'], falta['disciplina']
                ))
            
            Messagebox.show_info(f"{len(faltas)} faltas registradas!", "Sucesso")
        except Exception as e:
            Messagebox.show_error(f"Erro: {str(e)}", "Erro")
    
    def criar_aba_alunos(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Gerenciar Alunos")
        ttk.Label(aba, text="Aba de Alunos - Em desenvolvimento", font=('Arial', 14)).pack(pady=50)
    
    def criar_aba_horarios(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Gerenciar Horários")
        ttk.Label(aba, text="Aba de Horários - Em desenvolvimento", font=('Arial', 14)).pack(pady=50)
    
    def criar_aba_faltas(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Quadro Geral de Faltas")
        ttk.Label(aba, text="Aba de Faltas - Em desenvolvimento", font=('Arial', 14)).pack(pady=50)
    
    def iniciar(self):
        self.janela.mainloop()
'''

with open('interface.py', 'w', encoding='utf-8') as f:
    f.write(interface_content)
print("✓ interface.py criado (versão simplificada)")

print("\n" + "="*60)
print("ARQUIVOS RECRIADOS COM SUCESSO!")
print("="*60)
print("\nAgora execute:")
print("1. Copie o conteúdo do artifact 'logica_fix' para logica_app.py")
print("2. Execute: python main.py")
print("="*60)