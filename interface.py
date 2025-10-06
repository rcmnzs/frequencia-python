# -*- coding: utf-8 -*-
"""Interface gráfica completa do sistema"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
import logica_app as logica
import os
from datetime import datetime
from ttkbootstrap.dialogs import Messagebox, Querybox
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import logica_app as logica

class AplicativoFrequencia:
    def __init__(self):
        self.janela = ttk.Window(themename="darkly")
        self.janela.title("Processador de Frequência Escolar")
        self.janela.geometry("1100x750")
        
        self.pdf_frequencia = None
        self.pdf_ausentes = None
        self.pagina_alunos = 0
        self.pagina_horarios = 0
        self.pagina_faltas = 0
        self.itens_por_pagina = 50
        
        self.criar_interface()
    
    def atualizar_sistema_completo(self):
        """Atualiza todas as abas e dados do sistema"""
        try:
            # Atualizar aba de Alunos
            if hasattr(self, 'entry_busca_aluno'):
                self.combo_filtro_turma_alunos.configure(values=["Todas"] + logica.obter_turmas_distintas())
                self.pagina_alunos = 0
                self.carregar_alunos_tabela()
            
            # Atualizar aba de Horários
            if hasattr(self, 'combo_turma_horarios'):
                self.combo_turma_horarios.configure(values=["Todas"] + logica.obter_turmas_distintas())
                self.combo_dia_semana_horarios.configure(values=["Todos"] + logica.obter_dias_semana_distintos())
                self.pagina_horarios = 0
                self.carregar_horarios_tabela()
            
            # Atualizar aba de Faltas
            if hasattr(self, 'combo_filtro_disciplina'):
                self.combo_filtro_disciplina.configure(values=["Todas"] + logica.obter_disciplinas_distintas())
                self.combo_filtro_turma_faltas.configure(values=["Todas"] + logica.obter_turmas_distintas())
                self.combo_filtro_dia_faltas.configure(values=["Todos"] + logica.obter_dias_semana_distintos())
                self.pagina_faltas = 0
                self.carregar_faltas_tabela()
            
            # Limpar campos da aba processar
            if hasattr(self, 'entry_data'):
                for item in self.tree_processar.get_children():
                    self.tree_processar.delete(item)
            
            Messagebox.show_info("Sistema atualizado com sucesso!", "Atualização Completa")
            
        except Exception as e:
            Messagebox.show_error(f"Erro ao atualizar: {str(e)}", "Erro")
    
    def criar_interface(self):
        # Frame superior com botão de atualização global
        frame_topo = ttk.Frame(self.janela)
        frame_topo.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(frame_topo, text="Sistema de Frequência Escolar", font=('Arial', 14, 'bold')).pack(side=LEFT, padx=10)
        ttk.Button(frame_topo, text="🔄 Atualizar Sistema", command=self.atualizar_sistema_completo, bootstyle="info-outline", width=20).pack(side=RIGHT, padx=10)
        
        self.notebook = ttk.Notebook(self.janela)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.criar_aba_processar()
        self.criar_aba_alunos()
        self.criar_aba_horarios()
        self.criar_aba_faltas()
    
    # ========== ABA 1: PROCESSAR ==========
    def criar_aba_processar(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Processar Frequência")
        
        frame_arquivos = ttk.LabelFrame(aba, text="Arquivos PDF", padding=15)
        frame_arquivos.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(frame_arquivos, text="PDF Frequência:").grid(row=0, column=0, sticky=W, pady=5)
        self.label_pdf_freq = ttk.Label(frame_arquivos, text="Nenhum arquivo", foreground="gray")
        self.label_pdf_freq.grid(row=0, column=1, sticky=W, padx=10)
        ttk.Button(frame_arquivos, text="Selecionar", command=self.selecionar_pdf_frequencia, bootstyle=INFO).grid(row=0, column=2)
        
        ttk.Label(frame_arquivos, text="PDF Ausentes:").grid(row=1, column=0, sticky=W, pady=5)
        self.label_pdf_aus = ttk.Label(frame_arquivos, text="Nenhum arquivo", foreground="gray")
        self.label_pdf_aus.grid(row=1, column=1, sticky=W, padx=10)
        ttk.Button(frame_arquivos, text="Selecionar", command=self.selecionar_pdf_ausentes, bootstyle=INFO).grid(row=1, column=2)
        
        frame_data = ttk.LabelFrame(aba, text="Data", padding=15)
        frame_data.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(frame_data, text="Data (DD/MM/AAAA):").pack(side=LEFT, padx=5)
        self.entry_data = ttk.Entry(frame_data, width=15)
        self.entry_data.pack(side=LEFT, padx=5)
        ttk.Button(frame_data, text="📅 Calendário", command=self.abrir_calendario, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(frame_data, text="Processar", command=self.processar_frequencia, bootstyle=SUCCESS).pack(side=LEFT, padx=20)
        
        frame_resultado = ttk.LabelFrame(aba, text="Faltas do Dia", padding=10)
        frame_resultado.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        colunas = ['Matrícula', 'Nome', 'Turma', 'Disciplina']
        self.tree_processar = ttk.Treeview(frame_resultado, columns=colunas, show='headings', height=15)
        
        for col in colunas:
            self.tree_processar.heading(col, text=col)
            self.tree_processar.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_resultado, orient=VERTICAL, command=self.tree_processar.yview)
        self.tree_processar.configure(yscrollcommand=scrollbar.set)
        self.tree_processar.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    def selecionar_pdf_frequencia(self):
        # Define o diretório inicial
        pasta_pdfs = os.path.join(os.getcwd(), 'PDFs')
        if not os.path.exists(pasta_pdfs):
            os.makedirs(pasta_pdfs)
        
        arquivo = filedialog.askopenfilename(
            title="PDF Frequência", 
            filetypes=[("PDF", "*.pdf")],
            initialdir=pasta_pdfs
        )
        if arquivo:
            self.pdf_frequencia = arquivo
            nome = arquivo.split('/')[-1].split('\\')[-1]
            self.label_pdf_freq.config(text=nome, foreground="white")
    
    def selecionar_pdf_ausentes(self):
        # Define o diretório inicial
        pasta_pdfs = os.path.join(os.getcwd(), 'PDFs')
        if not os.path.exists(pasta_pdfs):
            os.makedirs(pasta_pdfs)
        
        arquivo = filedialog.askopenfilename(
            title="PDF Ausentes", 
            filetypes=[("PDF", "*.pdf")],
            initialdir=pasta_pdfs
        )
        if arquivo:
            self.pdf_ausentes = arquivo
            nome = arquivo.split('/')[-1].split('\\')[-1]
            self.label_pdf_aus.config(text=nome, foreground="white")
    
    def abrir_calendario(self):
        """Abre uma janela com calendário para seleção de data"""
        try:
            from ttkbootstrap.dialogs.dialogs import DatePickerDialog
            
            dialog = DatePickerDialog(title="Selecionar Data", firstweekday=6)
            dialog.date_selected
            
            if dialog.date_selected:
                data_selecionada = dialog.date_selected.strftime("%d/%m/%Y")
                self.entry_data.delete(0, END)
                self.entry_data.insert(0, data_selecionada)
        except Exception as e:
            # Fallback: usar entrada manual de data se calendário falhar
            Messagebox.show_info("Use o formato DD/MM/AAAA para inserir a data manualmente.", "Calendário")
            
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
    
    # ========== ABA 2: ALUNOS ==========
    def criar_aba_alunos(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Gerenciar Alunos")
        
        frame_superior = ttk.Frame(aba)
        frame_superior.pack(fill=X, padx=10, pady=10)
        
        # Linha de filtros
        frame_filtros = ttk.Frame(frame_superior)
        frame_filtros.pack(side=LEFT, fill=X, expand=True)
        
        ttk.Label(frame_filtros, text="Buscar:").pack(side=LEFT, padx=5)
        self.entry_busca_aluno = ttk.Entry(frame_filtros, width=25)
        self.entry_busca_aluno.pack(side=LEFT, padx=5)
        
        ttk.Label(frame_filtros, text="Turma:").pack(side=LEFT, padx=5)
        self.combo_filtro_turma_alunos = ttk.Combobox(frame_filtros, values=["Todas"] + logica.obter_turmas_distintas(), state="readonly", width=15)
        self.combo_filtro_turma_alunos.set("Todas")
        self.combo_filtro_turma_alunos.pack(side=LEFT, padx=5)
        
        ttk.Button(frame_filtros, text="Filtrar", command=self.aplicar_filtros_alunos, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(frame_filtros, text="Limpar Filtros", command=self.limpar_filtros_alunos, bootstyle=SECONDARY).pack(side=LEFT, padx=5)
        
        ttk.Button(frame_superior, text="Adicionar Aluno", command=self.abrir_janela_adicionar_aluno, bootstyle=SUCCESS).pack(side=RIGHT, padx=5)
        
        colunas = ['Matrícula', 'Nome', 'Turma']
        self.tree_alunos = ttk.Treeview(aba, columns=colunas, show='headings', height=15)
        for col in colunas:
            self.tree_alunos.heading(col, text=col)
            self.tree_alunos.column(col, width=150)
        self.tree_alunos.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        frame_paginacao = ttk.Frame(aba)
        frame_paginacao.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(frame_paginacao, text="Anterior", command=self.pagina_anterior_alunos).pack(side=LEFT)
        self.label_pagina_alunos = ttk.Label(frame_paginacao, text="Página 1")
        self.label_pagina_alunos.pack(side=LEFT, padx=10)
        ttk.Button(frame_paginacao, text="Próxima", command=self.pagina_proxima_alunos).pack(side=LEFT)
        
        self.carregar_alunos_tabela()

    def aplicar_filtros_alunos(self):
        """Aplica os filtros e reseta para primeira página"""
        self.pagina_alunos = 0
        self.carregar_alunos_tabela()

    def limpar_filtros_alunos(self):
        """Limpa os filtros de alunos"""
        self.entry_busca_aluno.delete(0, END)
        self.combo_filtro_turma_alunos.set("Todas")
        self.pagina_alunos = 0
        self.carregar_alunos_tabela()

    def carregar_alunos_tabela(self):
        for item in self.tree_alunos.get_children():
            self.tree_alunos.delete(item)
        
        termo_busca = self.entry_busca_aluno.get()
        filtro_turma = self.combo_filtro_turma_alunos.get()
        
        alunos = logica.carregar_alunos(self.itens_por_pagina, self.pagina_alunos * self.itens_por_pagina, termo_busca, filtro_turma)
        total_alunos = logica.contar_alunos(termo_busca, filtro_turma)
        
        for aluno in alunos.itertuples(index=False):
            self.tree_alunos.insert('', END, values=aluno)
        
        total_paginas = max(1, (total_alunos + self.itens_por_pagina - 1) // self.itens_por_pagina)
        self.label_pagina_alunos.config(text=f"Página {self.pagina_alunos + 1} de {total_paginas}")

    def pagina_anterior_alunos(self):
        if self.pagina_alunos > 0:
            self.pagina_alunos -= 1
            self.carregar_alunos_tabela()

    def pagina_proxima_alunos(self):
        termo_busca = self.entry_busca_aluno.get()
        filtro_turma = self.combo_filtro_turma_alunos.get()
        total_alunos = logica.contar_alunos(termo_busca, filtro_turma)
        if (self.pagina_alunos + 1) * self.itens_por_pagina < total_alunos:
            self.pagina_alunos += 1
            self.carregar_alunos_tabela()

    def abrir_janela_adicionar_aluno(self):
        janela_add = ttk.Toplevel(self.janela)
        janela_add.title("Adicionar Aluno")
        
        ttk.Label(janela_add, text="Matrícula:").pack(pady=5)
        entry_matricula = ttk.Entry(janela_add)
        entry_matricula.pack(pady=5)
        
        ttk.Label(janela_add, text="Nome:").pack(pady=5)
        entry_nome = ttk.Entry(janela_add)
        entry_nome.pack(pady=5)
        
        ttk.Label(janela_add, text="Turma:").pack(pady=5)
        entry_turma = ttk.Entry(janela_add)
        entry_turma.pack(pady=5)
        
        def salvar_aluno():
            try:
                dados = {
                    'matricula': entry_matricula.get(),
                    'nome': entry_nome.get(),
                    'turma': entry_turma.get()
                }
                logica.adicionar_aluno(dados)
                Messagebox.show_info("Aluno adicionado com sucesso!", "Sucesso")
                janela_add.destroy()
                self.carregar_alunos_tabela()
            except Exception as e:
                Messagebox.show_error(f"Erro: {str(e)}", "Erro")
        
        ttk.Button(janela_add, text="Salvar", command=salvar_aluno, bootstyle=SUCCESS).pack(pady=10)

    # ========== ABA 3: HORÁRIOS ==========
    def criar_aba_horarios(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Gerenciar Horários")
        
        frame_superior = ttk.Frame(aba)
        frame_superior.pack(fill=X, padx=10, pady=10)
        
        # Frame de filtros
        frame_filtros = ttk.Frame(frame_superior)
        frame_filtros.pack(side=LEFT, fill=X, expand=True)
        
        ttk.Label(frame_filtros, text="Filtrar por Turma:").pack(side=LEFT, padx=5)
        self.combo_turma_horarios = ttk.Combobox(frame_filtros, values=["Todas"] + logica.obter_turmas_distintas(), state="readonly", width=15)
        self.combo_turma_horarios.set("Todas")
        self.combo_turma_horarios.pack(side=LEFT, padx=5)
        
        ttk.Label(frame_filtros, text="Dia da Semana:").pack(side=LEFT, padx=5)
        self.combo_dia_semana_horarios = ttk.Combobox(frame_filtros, values=["Todos"] + logica.obter_dias_semana_distintos(), state="readonly", width=15)
        self.combo_dia_semana_horarios.set("Todos")
        self.combo_dia_semana_horarios.pack(side=LEFT, padx=5)
        
        ttk.Button(frame_filtros, text="Filtrar", command=self.aplicar_filtros_horarios, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(frame_filtros, text="Limpar Filtros", command=self.limpar_filtros_horarios, bootstyle=SECONDARY).pack(side=LEFT, padx=5)
        
        ttk.Button(frame_superior, text="Adicionar Horário", command=self.abrir_janela_adicionar_horario, bootstyle=SUCCESS).pack(side=RIGHT, padx=5)
        
        colunas = ['ID', 'Turma', 'Dia da Semana', 'Hora Início', 'Hora Fim', 'Disciplina']
        self.tree_horarios = ttk.Treeview(aba, columns=colunas, show='headings', height=15)
        for col in colunas:
            self.tree_horarios.heading(col, text=col)
            self.tree_horarios.column(col, width=100)
        self.tree_horarios.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        frame_paginacao = ttk.Frame(aba)
        frame_paginacao.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(frame_paginacao, text="Anterior", command=self.pagina_anterior_horarios).pack(side=LEFT)
        self.label_pagina_horarios = ttk.Label(frame_paginacao, text="Página 1")
        self.label_pagina_horarios.pack(side=LEFT, padx=10)
        ttk.Button(frame_paginacao, text="Próxima", command=self.pagina_proxima_horarios).pack(side=LEFT)
        
        self.carregar_horarios_tabela()

    def aplicar_filtros_horarios(self):
        """Aplica os filtros e reseta para primeira página"""
        self.pagina_horarios = 0
        self.carregar_horarios_tabela()

    def limpar_filtros_horarios(self):
        """Limpa os filtros de horários"""
        self.combo_turma_horarios.set("Todas")
        self.combo_dia_semana_horarios.set("Todos")
        self.pagina_horarios = 0
        self.carregar_horarios_tabela()

    def carregar_horarios_tabela(self):
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)
        
        turma_filtro = self.combo_turma_horarios.get()
        dia_semana_filtro = self.combo_dia_semana_horarios.get()
        
        horarios = logica.carregar_horarios(self.itens_por_pagina, self.pagina_horarios * self.itens_por_pagina, turma_filtro, dia_semana_filtro)
        total_horarios = logica.contar_horarios(turma_filtro, dia_semana_filtro)
        
        for horario in horarios.itertuples(index=False):
            self.tree_horarios.insert('', END, values=horario)
        
        total_paginas = max(1, (total_horarios + self.itens_por_pagina - 1) // self.itens_por_pagina)
        self.label_pagina_horarios.config(text=f"Página {self.pagina_horarios + 1} de {total_paginas}")

    def pagina_anterior_horarios(self):
        if self.pagina_horarios > 0:
            self.pagina_horarios -= 1
            self.carregar_horarios_tabela()

    def pagina_proxima_horarios(self):
        turma_filtro = self.combo_turma_horarios.get()
        dia_semana_filtro = self.combo_dia_semana_horarios.get()
        total_horarios = logica.contar_horarios(turma_filtro, dia_semana_filtro)
        if (self.pagina_horarios + 1) * self.itens_por_pagina < total_horarios:
            self.pagina_horarios += 1
            self.carregar_horarios_tabela()

    
    def pagina_anterior_horarios(self):
        if self.pagina_horarios > 0:
            self.pagina_horarios -= 1
            self.carregar_horarios_tabela()

    def pagina_proxima_horarios(self):
        turma_filtro = self.combo_turma_horarios.get()
        total_horarios = logica.contar_horarios(turma_filtro)
        if (self.pagina_horarios + 1) * self.itens_por_pagina < total_horarios:
            self.pagina_horarios += 1
            self.carregar_horarios_tabela()

    def abrir_janela_adicionar_horario(self):
        janela_add = ttk.Toplevel(self.janela)
        janela_add.title("Adicionar Horário")
        
        ttk.Label(janela_add, text="Turma:").pack(pady=5)
        entry_turma = ttk.Entry(janela_add)
        entry_turma.pack(pady=5)
        
        ttk.Label(janela_add, text="Dia da Semana:").pack(pady=5)
        combo_dia_semana = ttk.Combobox(janela_add, values=["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"], state="readonly")
        combo_dia_semana.pack(pady=5)
        
        ttk.Label(janela_add, text="Hora Início (HH:MM):").pack(pady=5)
        entry_hora_inicio = ttk.Entry(janela_add)
        entry_hora_inicio.pack(pady=5)
        
        ttk.Label(janela_add, text="Hora Fim (HH:MM):").pack(pady=5)
        entry_hora_fim = ttk.Entry(janela_add)
        entry_hora_fim.pack(pady=5)
        
        ttk.Label(janela_add, text="Disciplina:").pack(pady=5)
        entry_disciplina = ttk.Entry(janela_add)
        entry_disciplina.pack(pady=5)
        
        def salvar_horario():
            try:
                dados = {
                    'turma': entry_turma.get(),
                    'dia_semana': combo_dia_semana.get(),
                    'hora_inicio': entry_hora_inicio.get(),
                    'hora_fim': entry_hora_fim.get(),
                    'disciplina': entry_disciplina.get()
                }
                logica.adicionar_horario(dados)
                Messagebox.show_info("Horário adicionado com sucesso!", "Sucesso")
                janela_add.destroy()
                self.carregar_horarios_tabela()
            except Exception as e:
                Messagebox.show_error(f"Erro: {str(e)}", "Erro")
        
        ttk.Button(janela_add, text="Salvar", command=salvar_horario, bootstyle=SUCCESS).pack(pady=10)

    
   # ========== ABA 4: FALTAS ==========
    def criar_aba_faltas(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Quadro Geral de Faltas")
        
        # Frame de filtros
        frame_filtros = ttk.LabelFrame(aba, text="Filtros", padding=10)
        frame_filtros.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(frame_filtros, text="Nome:").grid(row=0, column=0, sticky=W, padx=5)
        self.entry_filtro_nome = ttk.Entry(frame_filtros, width=18)
        self.entry_filtro_nome.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_filtros, text="Turma:").grid(row=0, column=2, sticky=W, padx=5)
        self.combo_filtro_turma_faltas = ttk.Combobox(frame_filtros, values=["Todas"] + logica.obter_turmas_distintas(), state="readonly", width=13)
        self.combo_filtro_turma_faltas.set("Todas")
        self.combo_filtro_turma_faltas.grid(row=0, column=3, padx=5)
        
        ttk.Label(frame_filtros, text="Disciplina:").grid(row=0, column=4, sticky=W, padx=5)
        self.combo_filtro_disciplina = ttk.Combobox(frame_filtros, values=["Todas"] + logica.obter_disciplinas_distintas(), state="readonly", width=15)
        self.combo_filtro_disciplina.set("Todas")
        self.combo_filtro_disciplina.grid(row=0, column=5, padx=5)
        
        ttk.Label(frame_filtros, text="Dia:").grid(row=0, column=6, sticky=W, padx=5)
        self.combo_filtro_dia_faltas = ttk.Combobox(frame_filtros, values=["Todos"] + logica.obter_dias_semana_distintos(), state="readonly", width=13)
        self.combo_filtro_dia_faltas.set("Todos")
        self.combo_filtro_dia_faltas.grid(row=0, column=7, padx=5)
        
        ttk.Button(frame_filtros, text="Filtrar", command=self.aplicar_filtros_faltas, bootstyle=INFO).grid(row=0, column=8, padx=5)
        ttk.Button(frame_filtros, text="Limpar", command=self.limpar_filtros_faltas, bootstyle=SECONDARY).grid(row=0, column=9, padx=5)
        
        # Frame de ações
        frame_superior = ttk.Frame(aba)
        frame_superior.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(frame_superior, text="Adicionar Falta", command=self.abrir_janela_adicionar_falta, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        ttk.Button(frame_superior, text="Editar Falta", command=self.abrir_janela_editar_falta, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(frame_superior, text="Remover Falta", command=self.remover_falta, bootstyle=DANGER).pack(side=LEFT, padx=5)
        ttk.Button(frame_superior, text="Limpar Todas as Faltas", command=self.limpar_todas_faltas, bootstyle="danger-outline").pack(side=RIGHT, padx=5)
        
        # Tabela com coluna Turma
        colunas = ['Matrícula', 'Nome', 'Turma', 'Disciplina', 'Total de Faltas']
        self.tree_faltas = ttk.Treeview(aba, columns=colunas, show='headings', height=15)
        for col in colunas:
            self.tree_faltas.heading(col, text=col)
            if col == 'Total de Faltas':
                self.tree_faltas.column(col, width=120)
            else:
                self.tree_faltas.column(col, width=130)
        self.tree_faltas.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Paginação
        frame_paginacao = ttk.Frame(aba)
        frame_paginacao.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(frame_paginacao, text="Anterior", command=self.pagina_anterior_faltas).pack(side=LEFT)
        self.label_pagina_faltas = ttk.Label(frame_paginacao, text="Página 1")
        self.label_pagina_faltas.pack(side=LEFT, padx=10)
        ttk.Button(frame_paginacao, text="Próxima", command=self.pagina_proxima_faltas).pack(side=LEFT)
        
        self.carregar_faltas_tabela()

    def aplicar_filtros_faltas(self):
        """Aplica os filtros e reseta para primeira página"""
        self.pagina_faltas = 0
        self.carregar_faltas_tabela()

    def limpar_filtros_faltas(self):
        """Limpa os filtros"""
        self.entry_filtro_nome.delete(0, END)
        self.combo_filtro_disciplina.set("Todas")
        self.combo_filtro_turma_faltas.set("Todas")
        self.combo_filtro_dia_faltas.set("Todos")
        self.pagina_faltas = 0
        self.carregar_faltas_tabela()

    def carregar_faltas_tabela(self):
        for item in self.tree_faltas.get_children():
            self.tree_faltas.delete(item)
        
        filtro_nome = self.entry_filtro_nome.get()
        filtro_disciplina = self.combo_filtro_disciplina.get()
        filtro_turma = self.combo_filtro_turma_faltas.get()
        filtro_dia = self.combo_filtro_dia_faltas.get()
        
        faltas = logica.obter_quadro_geral_faltas(
            self.itens_por_pagina, 
            self.pagina_faltas * self.itens_por_pagina,
            filtro_nome,
            filtro_disciplina,
            filtro_turma,
            filtro_dia
        )
        total_faltas = logica.contar_faltas(filtro_nome, filtro_disciplina, filtro_turma, filtro_dia)
        
        for falta in faltas.itertuples(index=False):
            self.tree_faltas.insert('', END, values=falta)
        
        total_paginas = max(1, (total_faltas + self.itens_por_pagina - 1) // self.itens_por_pagina)
        self.label_pagina_faltas.config(text=f"Página {self.pagina_faltas + 1} de {total_paginas}")


    def pagina_anterior_faltas(self):
        if self.pagina_faltas > 0:
            self.pagina_faltas -= 1
            self.carregar_faltas_tabela()

    def pagina_proxima_faltas(self):
        filtro_nome = self.entry_filtro_nome.get()
        filtro_disciplina = self.combo_filtro_disciplina.get()
        filtro_turma = self.combo_filtro_turma_faltas.get()
        filtro_dia = self.combo_filtro_dia_faltas.get()
        total_faltas = logica.contar_faltas(filtro_nome, filtro_disciplina, filtro_turma, filtro_dia)
        if (self.pagina_faltas + 1) * self.itens_por_pagina < total_faltas:
            self.pagina_faltas += 1
            self.carregar_faltas_tabela()

    def limpar_todas_faltas(self):
        """Limpa todos os registros de faltas do banco"""
        resposta = Messagebox.yesno(
            "⚠️ ATENÇÃO!\n\nEsta ação irá APAGAR PERMANENTEMENTE todos os registros de faltas do sistema.\n\nDeseja realmente continuar?",
            "Confirmar Exclusão Total"
        )
        
        if resposta == "Sim":
            # Segunda confirmação
            resposta2 = Messagebox.yesno(
                "Tem certeza absoluta?\n\nTodos os dados de faltas serão perdidos!",
                "Última Confirmação"
            )
            
            if resposta2 == "Sim":
                try:
                    logica.limpar_todas_faltas()
                    Messagebox.show_info("Todas as faltas foram removidas com sucesso!", "Sucesso")
                    self.pagina_faltas = 0
                    self.carregar_faltas_tabela()
                except Exception as e:
                    Messagebox.show_error(f"Erro: {str(e)}", "Erro")

    def abrir_janela_adicionar_falta(self):
        janela_add = ttk.Toplevel(self.janela)
        janela_add.title("Adicionar Falta")
        janela_add.geometry("400x300")
        
        ttk.Label(janela_add, text="Matrícula do Aluno:").pack(pady=5)
        entry_matricula = ttk.Entry(janela_add, width=30)
        entry_matricula.pack(pady=5)
        
        ttk.Label(janela_add, text="Disciplina:").pack(pady=5)
        combo_disciplina = ttk.Combobox(janela_add, values=logica.obter_disciplinas_distintas(), width=28)
        combo_disciplina.pack(pady=5)
        
        ttk.Label(janela_add, text="Quantidade de Faltas:").pack(pady=5)
        entry_qtd = ttk.Entry(janela_add, width=30)
        entry_qtd.insert(0, "1")
        entry_qtd.pack(pady=5)
        
        def salvar_falta():
            try:
                dados = {
                    'matricula': entry_matricula.get(),
                    'disciplina': combo_disciplina.get(),
                    'total_faltas': int(entry_qtd.get())
                }
                logica.adicionar_falta(dados)
                Messagebox.show_info("Falta adicionada com sucesso!", "Sucesso")
                janela_add.destroy()
                self.carregar_faltas_tabela()
            except ValueError:
                Messagebox.show_error("Quantidade de faltas deve ser um número!", "Erro")
            except Exception as e:
                Messagebox.show_error(f"Erro: {str(e)}", "Erro")
        
        ttk.Button(janela_add, text="Salvar", command=salvar_falta, bootstyle=SUCCESS).pack(pady=20)

    def abrir_janela_editar_falta(self):
        selecionado = self.tree_faltas.selection()
        if not selecionado:
            Messagebox.show_warning("Selecione uma falta para editar!", "Aviso")
            return
        
        valores = self.tree_faltas.item(selecionado[0])['values']
        matricula_atual = valores[0]
        nome_atual = valores[1]
        turma_atual = valores[2]
        disciplina_atual = valores[3]  # Agora disciplina está na posição 3
        total_atual = valores[4]  # Total de faltas na posição 4
        
        janela_edit = ttk.Toplevel(self.janela)
        janela_edit.title("Editar Falta")
        janela_edit.geometry("400x300")
        
        ttk.Label(janela_edit, text=f"Matrícula: {matricula_atual}", font=('Arial', 10, 'bold')).pack(pady=5)
        ttk.Label(janela_edit, text=f"Nome: {nome_atual}", font=('Arial', 10, 'bold')).pack(pady=5)
        ttk.Label(janela_edit, text=f"Turma: {turma_atual}", font=('Arial', 10, 'bold')).pack(pady=5)
        ttk.Label(janela_edit, text=f"Disciplina: {disciplina_atual}", font=('Arial', 10, 'bold')).pack(pady=5)
        
        ttk.Label(janela_edit, text="Novo Total de Faltas:").pack(pady=10)
        entry_novo_total = ttk.Entry(janela_edit, width=30)
        entry_novo_total.insert(0, str(total_atual))
        entry_novo_total.pack(pady=5)
        
        def salvar_edicao():
            try:
                novo_total = int(entry_novo_total.get())
                logica.atualizar_falta(matricula_atual, disciplina_atual, novo_total)
                Messagebox.show_info("Falta atualizada com sucesso!", "Sucesso")
                janela_edit.destroy()
                self.carregar_faltas_tabela()
            except ValueError:
                Messagebox.show_error("Total de faltas deve ser um número!", "Erro")
            except Exception as e:
                Messagebox.show_error(f"Erro: {str(e)}", "Erro")
        
        ttk.Button(janela_edit, text="Salvar", command=salvar_edicao, bootstyle=SUCCESS).pack(pady=20)
        
        def salvar_edicao():
            try:
                novo_total = int(entry_novo_total.get())
                logica.atualizar_falta(matricula_atual, disciplina_atual, novo_total)
                Messagebox.show_info("Falta atualizada com sucesso!", "Sucesso")
                janela_edit.destroy()
                self.carregar_faltas_tabela()
            except ValueError:
                Messagebox.show_error("Total de faltas deve ser um número!", "Erro")
            except Exception as e:
                Messagebox.show_error(f"Erro: {str(e)}", "Erro")
        
        ttk.Button(janela_edit, text="Salvar", command=salvar_edicao, bootstyle=SUCCESS).pack(pady=20)

    def remover_falta(self):
        selecionado = self.tree_faltas.selection()
        if not selecionado:
            Messagebox.show_warning("Selecione uma falta para remover!", "Aviso")
            return
        
        valores = self.tree_faltas.item(selecionado[0])['values']
        matricula = valores[0]
        nome = valores[1]
        turma = valores[2]
        disciplina = valores[3]  # Agora disciplina está na posição 3
        
        resposta = Messagebox.yesno(
            f"Deseja realmente remover o registro de faltas de:\n\n{nome} ({matricula})\nTurma: {turma}\nDisciplina: {disciplina}?",
            "Confirmar Remoção"
        )
        
        if resposta == "Sim":
            try:
                logica.excluir_falta(matricula, disciplina)
                Messagebox.show_info("Falta removida com sucesso!", "Sucesso")
                self.carregar_faltas_tabela()
            except Exception as e:
                Messagebox.show_error(f"Erro: {str(e)}", "Erro")
                
                    
    def iniciar(self):
        self.janela.mainloop()