# -*- coding: utf-8 -*-
"""Interface gráfica completa do sistema"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
import logica_app as logica
import os
from datetime import datetime
from ttkbootstrap.dialogs import Querybox
<<<<<<< HEAD
=======
from tkinter import filedialog
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c


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
            if hasattr(self, 'entry_busca_aluno'):
                self.combo_filtro_turma_alunos.configure(values=["Todas"] + logica.obter_turmas_distintas())
                self.pagina_alunos = 0
                self.carregar_alunos_tabela()
            
<<<<<<< HEAD
            if hasattr(self, 'combo_turma_grade'):
                self.carregar_grade_horarios()

=======
            # Atualizar aba de Horários
            if hasattr(self, 'combo_turma_grade'):
                self.carregar_grade_horarios()

            # Atualizar aba de Faltas
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
            if hasattr(self, 'combo_filtro_disciplina'):
                self.combo_filtro_disciplina.configure(values=["Todas"] + logica.obter_disciplinas_distintas())
                self.combo_filtro_turma_faltas.configure(values=["Todas"] + logica.obter_turmas_distintas())
                self.combo_filtro_dia_faltas.configure(values=["Todos"] + logica.obter_dias_semana_distintos())
                self.pagina_faltas = 0
                self.carregar_faltas_tabela()
            
            if hasattr(self, 'entry_data'):
                for item in self.tree_processar.get_children():
                    self.tree_processar.delete(item)
            
            Messagebox.show_info("Sistema atualizado com sucesso!", "Atualização Completa")
            
        except Exception as e:
            Messagebox.show_error(f"Erro ao atualizar: {str(e)}", "Erro")
    
    def criar_interface(self):
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
            self.tree_processar.heading(col, text=col, anchor=W)
            self.tree_processar.column(col, width=150, anchor=W)
        
        scrollbar = ttk.Scrollbar(frame_resultado, orient=VERTICAL, command=self.tree_processar.yview)
        self.tree_processar.configure(yscrollcommand=scrollbar.set)
        self.tree_processar.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    def selecionar_pdf_frequencia(self):
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
            nome = os.path.basename(arquivo)
            self.label_pdf_freq.config(text=nome, foreground="white")
    
    def selecionar_pdf_ausentes(self):
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
            nome = os.path.basename(arquivo)
            self.label_pdf_aus.config(text=nome, foreground="white")
    
    def abrir_calendario(self):
        try:
            from ttkbootstrap.dialogs.dialogs import DatePickerDialog
            dialog = DatePickerDialog(title="Selecionar Data", firstweekday=6)
<<<<<<< HEAD
=======
            
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
            if dialog.date_selected:
                data_selecionada = dialog.date_selected.strftime("%d/%m/%Y")
                self.entry_data.delete(0, END)
                self.entry_data.insert(0, data_selecionada)
<<<<<<< HEAD
        except:
=======
        except Exception as e:
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
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
    
    def criar_aba_alunos(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Gerenciar Alunos")
        
        frame_superior = ttk.Frame(aba)
        frame_superior.pack(fill=X, padx=10, pady=10)
        
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
        
        frame_botoes_acao = ttk.Frame(frame_superior)
        frame_botoes_acao.pack(side=RIGHT)

        ttk.Button(frame_botoes_acao, text="Adicionar Aluno", command=self.abrir_janela_adicionar_aluno, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        ttk.Button(frame_botoes_acao, text="Editar Aluno", command=self.abrir_janela_editar_aluno, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(frame_botoes_acao, text="Excluir Aluno", command=self.excluir_aluno_selecionado, bootstyle=DANGER).pack(side=LEFT, padx=5)
        
        colunas = ['Matrícula', 'Nome', 'Turma']
        self.tree_alunos = ttk.Treeview(aba, columns=colunas, show='headings', height=15)
        for col in colunas:
            self.tree_alunos.heading(col, text=col, anchor=W)
            self.tree_alunos.column(col, width=150, anchor=W)
        self.tree_alunos.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        frame_paginacao = ttk.Frame(aba)
        frame_paginacao.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(frame_paginacao, text="Anterior", command=self.pagina_anterior_alunos).pack(side=LEFT)
        self.label_pagina_alunos = ttk.Label(frame_paginacao, text="Página 1")
        self.label_pagina_alunos.pack(side=LEFT, padx=10)
        ttk.Button(frame_paginacao, text="Próxima", command=self.pagina_proxima_alunos).pack(side=LEFT)
        
        self.carregar_alunos_tabela()

    def aplicar_filtros_alunos(self):
        self.pagina_alunos = 0
        self.carregar_alunos_tabela()

    def limpar_filtros_alunos(self):
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
        janela_add.geometry("400x350")

        ttk.Label(janela_add, text="Adicionar Novo Aluno", font=('Arial', 14, 'bold')).pack(pady=20)
        
        frame_form = ttk.Frame(janela_add)
        frame_form.pack(fill=X, padx=20)

        ttk.Label(frame_form, text="Matrícula:").pack(anchor=W)
        entry_matricula = ttk.Entry(frame_form)
        entry_matricula.pack(fill=X, pady=(0, 10))
        
        ttk.Label(frame_form, text="Nome:").pack(anchor=W)
        entry_nome = ttk.Entry(frame_form)
        entry_nome.pack(fill=X, pady=(0, 10))
        
        ttk.Label(frame_form, text="Turma:").pack(anchor=W)
        entry_turma = ttk.Entry(frame_form)
        entry_turma.pack(fill=X, pady=(0, 10))
        
        entry_matricula.focus_set()

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
        
        ttk.Button(janela_add, text="Salvar", command=salvar_aluno, bootstyle=SUCCESS).pack(pady=20)

    def abrir_janela_editar_aluno(self):
        selecionado = self.tree_alunos.selection()
        if not selecionado:
            Messagebox.show_warning("Selecione um aluno para editar!", "Aviso")
            return
        
        valores = self.tree_alunos.item(selecionado[0])["values"]
        matricula_atual = valores[0]
        nome_atual = valores[1]
        turma_atual = valores[2]
        
        janela_edit = ttk.Toplevel(self.janela)
        janela_edit.title("Editar Aluno")
        janela_edit.geometry("400x350")
        
        ttk.Label(janela_edit, text="Editar Aluno", font=('Arial', 14, 'bold')).pack(pady=20)
        
        frame_form = ttk.Frame(janela_edit)
        frame_form.pack(fill=X, padx=20)

        ttk.Label(frame_form, text="Matrícula:").pack(anchor=W)
        entry_matricula = ttk.Entry(frame_form)
        entry_matricula.insert(0, matricula_atual)
        entry_matricula.pack(fill=X, pady=(0, 10))
        
        ttk.Label(frame_form, text="Nome:").pack(anchor=W)
        entry_nome = ttk.Entry(frame_form)
        entry_nome.insert(0, nome_atual)
        entry_nome.pack(fill=X, pady=(0, 10))
        
        ttk.Label(frame_form, text="Turma:").pack(anchor=W)
        entry_turma = ttk.Entry(frame_form)
        entry_turma.insert(0, turma_atual)
        entry_turma.pack(fill=X, pady=(0, 10))
        
        entry_matricula.focus_set()

        def salvar_edicao():
            try:
                novos_dados = {
                    "matricula": entry_matricula.get(),
                    "nome": entry_nome.get(),
                    "turma": entry_turma.get()
                }
                logica.atualizar_aluno(matricula_atual, novos_dados)
                Messagebox.show_info("Aluno atualizado com sucesso!", "Sucesso")
                janela_edit.destroy()
                self.carregar_alunos_tabela()
            except Exception as e:
                Messagebox.show_error(f"Erro: {str(e)}", "Erro")
        
        ttk.Button(janela_edit, text="Salvar", command=salvar_edicao, bootstyle=SUCCESS).pack(pady=20)

    def excluir_aluno_selecionado(self):
        selecionado = self.tree_alunos.selection()
        if not selecionado:
            Messagebox.show_warning("Selecione um aluno para excluir!", "Aviso")
            return
        
        valores = self.tree_alunos.item(selecionado[0])["values"]
        matricula_aluno = valores[0]
        nome_aluno = valores[1]
        
        resposta = Messagebox.yesno(
            f"Deseja realmente excluir o aluno {nome_aluno} (Matrícula: {matricula_aluno})?",
            "Confirmar Exclusão"
        )
        
        if resposta == "Sim":
            try:
                logica.excluir_aluno(matricula_aluno)
                Messagebox.show_info("Aluno excluído com sucesso!", "Sucesso")
                self.carregar_alunos_tabela()
            except Exception as e:
                Messagebox.show_error(f"Erro: {str(e)}", "Erro")

    def criar_aba_horarios(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Gerenciar Horários")
        
        frame_superior = ttk.Frame(aba)
        frame_superior.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(frame_superior, text="Selecionar Turma:").pack(side=LEFT, padx=5)
        self.combo_turma_grade = ttk.Combobox(frame_superior, values=["Todas"] + logica.obter_turmas_distintas(), state="readonly", width=15)
        self.combo_turma_grade.set("Todas")
        self.combo_turma_grade.bind("<<ComboboxSelected>>", lambda e: self.carregar_grade_horarios())
        self.combo_turma_grade.pack(side=LEFT, padx=5)
        
        ttk.Button(frame_superior, text="➕ Adicionar Horário", command=self.abrir_janela_adicionar_horario, bootstyle=SUCCESS).pack(side=LEFT, padx=10)
        ttk.Button(frame_superior, text="Modo Lista", command=self.mostrar_horarios_lista, bootstyle=INFO).pack(side=LEFT, padx=5)
        
        self.frame_grade = ttk.Frame(aba)
        self.frame_grade.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.carregar_grade_horarios()

    def carregar_grade_horarios(self):
        for widget in self.frame_grade.winfo_children():
            widget.destroy()
        
        turma_selecionada = self.combo_turma_grade.get()
        
        if turma_selecionada == "Todas":
            df_horarios = logica.obter_horarios_todas_turmas_grade()
        else:
            df_horarios = logica.obter_horarios_por_turma_grade(turma_selecionada)
        
        if df_horarios.empty:
            ttk.Label(self.frame_grade, text="Nenhum horário cadastrado para esta turma", font=('Arial', 12)).pack(pady=50)
            return
        
        dias = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO"]
        horarios_unicos = sorted(df_horarios['hora_inicio'].unique())
        
        canvas = ttk.Canvas(self.frame_grade)
        scrollbar_v = ttk.Scrollbar(self.frame_grade, orient="vertical", command=canvas.yview)
        scrollbar_h = ttk.Scrollbar(self.frame_grade, orient="horizontal", command=canvas.xview)
        frame_conteudo = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        scrollbar_v.pack(side=RIGHT, fill=Y)
        scrollbar_h.pack(side=BOTTOM, fill=X)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        
        canvas.create_window((0, 0), window=frame_conteudo, anchor='nw')
        
        ttk.Label(frame_conteudo, text="Horário", font=('Arial', 10, 'bold'), borderwidth=1, relief="solid", width=12).grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        
        for col, dia in enumerate(dias, start=1):
            ttk.Label(frame_conteudo, text=dia, font=('Arial', 10, 'bold'), borderwidth=1, relief="solid").grid(row=0, column=col, sticky='nsew', padx=1, pady=1)
        
        for row_idx, horario in enumerate(horarios_unicos, start=1):
            ttk.Label(frame_conteudo, text=horario, font=('Arial', 9, 'bold'), borderwidth=1, relief="solid").grid(row=row_idx, column=0, sticky='nsew', padx=1, pady=1)
            
            for col_idx, dia in enumerate(dias, start=1):
                aula = df_horarios[(df_horarios['dia_semana'] == dia) & (df_horarios['hora_inicio'] == horario)]
                
                if not aula.empty:
                    aula_info = aula.iloc[0]
                    id_horario = aula_info['id']
                    disciplina = aula_info['disciplina']
                    turma = aula_info['turma']
                    hora_fim = aula_info['hora_fim']
                    
                    frame_aula = ttk.Frame(frame_conteudo, borderwidth=2, relief="raised")
                    frame_aula.grid(row=row_idx, column=col_idx, sticky='nsew', padx=1, pady=1)
                    
                    texto = f"{disciplina}\n{turma}\n{horario}-{hora_fim}"
                    label_aula = ttk.Label(frame_aula, text=texto, font=('Arial', 8), justify='center', padding=5)
                    label_aula.pack(fill=BOTH, expand=YES)
                    
                    frame_aula.bind('<Button-1>', lambda e, id_h=int(id_horario): self.abrir_menu_horario(id_h))
                    label_aula.bind('<Button-1>', lambda e, id_h=int(id_horario): self.abrir_menu_horario(id_h))
                    
                    frame_aula.bind('<Enter>', lambda e, f=frame_aula: f.configure(relief="solid"))
                    frame_aula.bind('<Leave>', lambda e, f=frame_aula: f.configure(relief="raised"))
                else:
                    ttk.Label(frame_conteudo, text="", borderwidth=1, relief="solid").grid(row=row_idx, column=col_idx, sticky='nsew', padx=1, pady=1)
        
        for i in range(len(dias) + 1):
            frame_conteudo.columnconfigure(i, weight=1, minsize=120)
        
        for i in range(len(horarios_unicos) + 1):
            frame_conteudo.rowconfigure(i, weight=1, minsize=60)
        
        frame_conteudo.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def abrir_menu_horario(self, id_horario):
        try:
            horario = logica.obter_horario_por_id(id_horario)
            
            janela_menu = ttk.Toplevel(self.janela)
            janela_menu.title("Gerenciar Horário")
            janela_menu.geometry("400x380")
            
            ttk.Label(janela_menu, text="Informações do Horário", font=('Arial', 14, 'bold')).pack(pady=20)
            
            info_frame = ttk.Frame(janela_menu, padding=10)
            info_frame.pack(fill=X, padx=20)
            
            ttk.Label(info_frame, text=f"Turma: {horario[1]}", font=('Arial', 10)).pack(anchor=W, pady=2)
            ttk.Label(info_frame, text=f"Dia: {horario[2]}", font=('Arial', 10)).pack(anchor=W, pady=2)
            ttk.Label(info_frame, text=f"Horário: {horario[3]} - {horario[4]}", font=('Arial', 10)).pack(anchor=W, pady=2)
            ttk.Label(info_frame, text=f"Disciplina: {horario[5]}", font=('Arial', 10)).pack(anchor=W, pady=2)
            
            frame_botoes = ttk.Frame(janela_menu)
            frame_botoes.pack(fill=X, padx=20, pady=20)
            
            frame_botoes.columnconfigure(0, weight=1)

            ttk.Button(frame_botoes, text="Editar", command=lambda: self.editar_horario(id_horario, janela_menu), bootstyle=INFO).pack(fill=X, pady=4)
            ttk.Button(frame_botoes, text="Remover", command=lambda: self.remover_horario(id_horario, janela_menu), bootstyle=DANGER).pack(fill=X, pady=4)
            ttk.Button(frame_botoes, text="Fechar", command=janela_menu.destroy, bootstyle=SECONDARY).pack(fill=X, pady=4)
            
        except Exception as e:
            Messagebox.show_error(f"Erro ao carregar horário: {str(e)}", "Erro")

    def editar_horario(self, id_horario, janela_anterior):
        try:
            janela_anterior.destroy()
            
            horario = logica.obter_horario_por_id(id_horario)
            
            janela_edit = ttk.Toplevel(self.janela)
            janela_edit.title("Editar Horário")
            janela_edit.geometry("400x450")
            
            ttk.Label(janela_edit, text="Editar Horário", font=('Arial', 12, 'bold')).pack(pady=10)
            
            frame_form = ttk.Frame(janela_edit, padding=20)
            frame_form.pack(fill=BOTH, expand=YES)
            
            ttk.Label(frame_form, text="Turma:").pack(pady=5)
            entry_turma = ttk.Entry(frame_form, width=30)
            entry_turma.insert(0, horario[1])
<<<<<<< HEAD
=======
            entry_turma.configure(state='normal')
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
            entry_turma.pack(pady=5)

            ttk.Label(frame_form, text="Dia da Semana:").pack(pady=5)
            combo_dia_semana = ttk.Combobox(
                frame_form,
<<<<<<< HEAD
                values=["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"],
=======
                values=[
                    "SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA",
                    "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"
                ],
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
                state="normal",
                width=28
            )
            combo_dia_semana.set(horario[2])
            combo_dia_semana.pack(pady=5)

            ttk.Label(frame_form, text="Hora Início (HH:MM):").pack(pady=5)
            entry_hora_inicio = ttk.Entry(frame_form, width=30)
            entry_hora_inicio.insert(0, horario[3])
<<<<<<< HEAD
=======
            entry_hora_inicio.configure(state='normal')
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
            entry_hora_inicio.pack(pady=5)

            ttk.Label(frame_form, text="Hora Fim (HH:MM):").pack(pady=5)
            entry_hora_fim = ttk.Entry(frame_form, width=30)
            entry_hora_fim.insert(0, horario[4])
<<<<<<< HEAD
=======
            entry_hora_fim.configure(state='normal')
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
            entry_hora_fim.pack(pady=5)

            ttk.Label(frame_form, text="Disciplina:").pack(pady=5)
            entry_disciplina = ttk.Entry(frame_form, width=30)
            entry_disciplina.insert(0, horario[5])
<<<<<<< HEAD
            entry_disciplina.pack(pady=5)
            
            entry_turma.focus_set()
=======
            entry_disciplina.configure(state='normal')
            entry_disciplina.pack(pady=5)
            
            entry_turma.focus_set()    
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
                
            def salvar_edicao():
                try:
                    dados = {
                        'turma': entry_turma.get(),
                        'dia_semana': combo_dia_semana.get(),
                        'hora_inicio': entry_hora_inicio.get(),
                        'hora_fim': entry_hora_fim.get(),
                        'disciplina': entry_disciplina.get()
                    }
                    logica.atualizar_horario(id_horario, dados)
                    Messagebox.show_info("Horário atualizado com sucesso!", "Sucesso")
                    janela_edit.destroy()
                    self.carregar_grade_horarios()
                except Exception as e:
                    Messagebox.show_error(f"Erro: {str(e)}", "Erro")
            
            ttk.Button(frame_form, text="Salvar", command=salvar_edicao, bootstyle=SUCCESS).pack(pady=15)
            
        except Exception as e:
            Messagebox.show_error(f"Erro ao carregar dados para edição: {str(e)}", "Erro")

    def remover_horario(self, id_horario, janela_anterior):
        try:
            horario = logica.obter_horario_por_id(id_horario)
            
            resposta = Messagebox.yesno(
                f"Deseja realmente remover este horário?\n\nTurma: {horario[1]}\nDia: {horario[2]}\nHorário: {horario[3]}-{horario[4]}\nDisciplina: {horario[5]}",
                "Confirmar Remoção"
            )
            
            if resposta == "Sim":
                logica.excluir_horario(id_horario)
                Messagebox.show_info("Horário removido com sucesso!", "Sucesso")
                janela_anterior.destroy()
                self.carregar_grade_horarios()
                
        except Exception as e:
            Messagebox.show_error(f"Erro ao remover horário: {str(e)}", "Erro")

    def mostrar_horarios_lista(self):
        for widget in self.frame_grade.winfo_children():
            widget.destroy()
        
        frame_filtros = ttk.Frame(self.frame_grade)
        frame_filtros.pack(fill=X, pady=10)
        
        ttk.Label(frame_filtros, text="Filtrar por Turma:").pack(side=LEFT, padx=5)
        combo_turma_lista = ttk.Combobox(frame_filtros, values=["Todas"] + logica.obter_turmas_distintas(), state="readonly", width=15)
        combo_turma_lista.set("Todas")
        combo_turma_lista.pack(side=LEFT, padx=5)
        
        ttk.Label(frame_filtros, text="Dia da Semana:").pack(side=LEFT, padx=5)
        combo_dia_lista = ttk.Combobox(frame_filtros, values=["Todos"] + logica.obter_dias_semana_distintos(), state="readonly", width=15)
        combo_dia_lista.set("Todos")
        combo_dia_lista.pack(side=LEFT, padx=5)
        
        ttk.Button(frame_filtros, text="Modo Grade", command=self.carregar_grade_horarios, bootstyle=INFO).pack(side=RIGHT, padx=5)
        
        colunas = ['ID', 'Turma', 'Dia da Semana', 'Hora Início', 'Hora Fim', 'Disciplina']
        tree_lista = ttk.Treeview(self.frame_grade, columns=colunas, show='headings', height=20)
        for col in colunas:
            tree_lista.heading(col, text=col)
            tree_lista.column(col, width=100)
        tree_lista.pack(fill=BOTH, expand=YES)
        
        self.atualizar_lista(tree_lista, combo_turma_lista, combo_dia_lista)
        
        tree_lista.bind('<Double-1>', lambda e: self.abrir_menu_horario_lista(tree_lista))
        
        combo_turma_lista.bind('<<ComboboxSelected>>', lambda e: self.atualizar_lista(tree_lista, combo_turma_lista, combo_dia_lista))
        combo_dia_lista.bind('<<ComboboxSelected>>', lambda e: self.atualizar_lista(tree_lista, combo_turma_lista, combo_dia_lista))

    def atualizar_lista(self, tree, combo_turma, combo_dia):
        for item in tree.get_children():
            tree.delete(item)
        
        turma_filtro = combo_turma.get()
        dia_filtro = combo_dia.get()
        horarios = logica.carregar_horarios(None, 0, turma_filtro, dia_filtro)
        
        for horario in horarios.itertuples(index=False):
            tree.insert('', END, values=horario)

    def abrir_menu_horario_lista(self, tree):
        selecionado = tree.selection()
        if not selecionado:
            return
        
        valores = tree.item(selecionado[0])['values']
        id_horario = valores[0]
        self.abrir_menu_horario(id_horario)

    def abrir_janela_adicionar_horario(self):
        janela_add = ttk.Toplevel(self.janela)
        janela_add.title("Adicionar Horário")
        janela_add.geometry("400x400")
        
        ttk.Label(janela_add, text="Adicionar Novo Horário", font=('Arial', 12, 'bold')).pack(pady=10)
        
        frame_form = ttk.Frame(janela_add, padding=20)
        frame_form.pack(fill=BOTH, expand=YES)
        
        ttk.Label(frame_form, text="Turma:").pack(pady=5)
        entry_turma = ttk.Entry(frame_form, width=30)
        entry_turma.pack(pady=5)
        
        ttk.Label(frame_form, text="Dia da Semana:").pack(pady=5)
        combo_dia_semana = ttk.Combobox(frame_form, values=["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"], state="readonly", width=28)
        combo_dia_semana.pack(pady=5)
        
        ttk.Label(frame_form, text="Hora Início (HH:MM):").pack(pady=5)
        entry_hora_inicio = ttk.Entry(frame_form, width=30)
        entry_hora_inicio.pack(pady=5)
        
        ttk.Label(frame_form, text="Hora Fim (HH:MM):").pack(pady=5)
        entry_hora_fim = ttk.Entry(frame_form, width=30)
        entry_hora_fim.pack(pady=5)
        
        ttk.Label(frame_form, text="Disciplina:").pack(pady=5)
        entry_disciplina = ttk.Entry(frame_form, width=30)
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
                self.carregar_grade_horarios()
            except Exception as e:
                Messagebox.show_error(f"Erro: {str(e)}", "Erro")
        
        ttk.Button(frame_form, text="Salvar", command=salvar_horario, bootstyle=SUCCESS).pack(pady=15)
    
<<<<<<< HEAD
=======
    # ========== ABA 4: FALTAS ==========
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
    def criar_aba_faltas(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Quadro Geral de Faltas")
        
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
        
        frame_superior = ttk.Frame(aba)
        frame_superior.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(frame_superior, text="Adicionar Falta", command=self.abrir_janela_adicionar_falta, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        ttk.Button(frame_superior, text="Editar Falta", command=self.abrir_janela_editar_falta, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(frame_superior, text="Remover Falta", command=self.remover_falta, bootstyle=DANGER).pack(side=LEFT, padx=5)
        ttk.Button(frame_superior, text="📊 Exportar para Excel", command=self.exportar_excel, bootstyle="success-outline", width=20).pack(side=LEFT, padx=15)
        ttk.Button(frame_superior, text="Limpar Todas as Faltas", command=self.limpar_todas_faltas, bootstyle="danger-outline").pack(side=RIGHT, padx=5)
        
        colunas = ['Matrícula', 'Nome', 'Turma', 'Disciplina', 'Total de Faltas']
        self.tree_faltas = ttk.Treeview(aba, columns=colunas, show='headings', height=15)
        for col in colunas:
            self.tree_faltas.heading(col, text=col, anchor=W)
            if col == 'Total de Faltas':
<<<<<<< HEAD
                self.tree_faltas.column(col, width=130, anchor=CENTER)
=======
                self.tree_faltas.column(col, width=130, anchor=CENTER) # Manter números centralizados
>>>>>>> dff7806e9187c3a3a5bf23e75924bc777d34899c
            else:
                self.tree_faltas.column(col, width=130, anchor=W)
        self.tree_faltas.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        frame_paginacao = ttk.Frame(aba)
        frame_paginacao.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(frame_paginacao, text="Anterior", command=self.pagina_anterior_faltas).pack(side=LEFT)
        self.label_pagina_faltas = ttk.Label(frame_paginacao, text="Página 1")
        self.label_pagina_faltas.pack(side=LEFT, padx=10)
        ttk.Button(frame_paginacao, text="Próxima", command=self.pagina_proxima_faltas).pack(side=LEFT)
        
        self.carregar_faltas_tabela()

    def exportar_excel(self):
        try:
            meses_disponiveis = logica.obter_meses_com_faltas()
            
            if not meses_disponiveis:
                Messagebox.show_warning("Nenhuma falta registrada no histórico!", "Aviso")
                return
            
            janela_export = ttk.Toplevel(self.janela)
            janela_export.title("Exportar para Excel")
            janela_export.geometry("400x300")
            
            ttk.Label(janela_export, text="Exportar Faltas para Excel", font=('Arial', 14, 'bold')).pack(pady=20)
            
            frame_form = ttk.Frame(janela_export, padding=20)
            frame_form.pack(fill=BOTH, expand=YES)
            
            ttk.Label(frame_form, text="Selecione o mês/ano:").pack(pady=10)
            
            opcoes_meses = [m['label'] for m in meses_disponiveis]
            combo_mes = ttk.Combobox(frame_form, values=opcoes_meses, state="readonly", width=25)
            if opcoes_meses:
                combo_mes.set(opcoes_meses[0])
            combo_mes.pack(pady=10)
            
            def realizar_exportacao():
                try:
                    if not combo_mes.get():
                        Messagebox.show_warning("Selecione um mês!", "Aviso")
                        return
                    
                    idx_selecionado = opcoes_meses.index(combo_mes.get())
                    mes_selecionado = meses_disponiveis[idx_selecionado]
                    
                    pasta_inicial = os.path.join(os.getcwd(), 'Exportacoes')
                    if not os.path.exists(pasta_inicial):
                        os.makedirs(pasta_inicial)
                    
                    nome_arquivo_padrao = f"Faltas_{mes_selecionado['mes']:02d}_{mes_selecionado['ano']}.xlsx"
                    caminho_arquivo = filedialog.asksaveasfilename(
                        title="Salvar arquivo Excel",
                        initialdir=pasta_inicial,
                        initialfile=nome_arquivo_padrao,
                        defaultextension=".xlsx",
                        filetypes=[("Excel", "*.xlsx")]
                    )
                    
                    if not caminho_arquivo:
                        return
                    
                    logica.exportar_faltas_para_excel(
                        mes_selecionado['mes'],
                        mes_selecionado['ano'],
                        caminho_arquivo
                    )
                    
                    Messagebox.show_info(
                        f"Planilha exportada com sucesso!\n\nLocal: {caminho_arquivo}",
                        "Sucesso"
                    )
                    
                    janela_export.destroy()
                    
                except Exception as e:
                    Messagebox.show_error(f"Erro ao exportar: {str(e)}", "Erro")
            
            ttk.Button(frame_form, text="Exportar", command=realizar_exportacao, bootstyle=SUCCESS, width=20).pack(pady=20)
            ttk.Button(frame_form, text="Cancelar", command=janela_export.destroy, bootstyle=SECONDARY, width=20).pack(pady=5)
            
        except Exception as e:
            Messagebox.show_error(f"Erro: {str(e)}", "Erro")

    def aplicar_filtros_faltas(self):
        self.pagina_faltas = 0
        self.carregar_faltas_tabela()

    def limpar_filtros_faltas(self):
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
        resposta = Messagebox.yesno(
            "⚠️ ATENÇÃO!\n\nEsta ação irá APAGAR PERMANENTEMENTE todos os registros de faltas do sistema.\n\nDeseja realmente continuar?",
            "Confirmar Exclusão Total"
        )
        
        if resposta == "Sim":
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
        disciplina_atual = valores[3]
        total_atual = valores[4]
        
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

    def remover_falta(self):
        selecionado = self.tree_faltas.selection()
        if not selecionado:
            Messagebox.show_warning("Selecione uma falta para remover!", "Aviso")
            return
        
        valores = self.tree_faltas.item(selecionado[0])['values']
        matricula = valores[0]
        nome = valores[1]
        turma = valores[2]
        disciplina = valores[3]
        
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

if __name__ == "__main__":
    app = AplicativoFrequencia()
    app.iniciar()