from tkinter import *
from tkinter import ttk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser
import sqlite3

root = Tk()

    


class FuncsFerr():
    def limpar_ferramentas(self):
        self.entry_tamanho.delete(0, END)
        self.entry_materialFerramenta.delete(0, END)
        self.entry_tipoFerramenta.delete(0, END)
        self.entry_codigo.delete(0, END)
        self.entry_unidadeMedida.delete(0, END)
        self.entry_partNumber.delete(0, END)
        self.entry_descricao.delete(0, END)
        self.entry_fabricante.delete(0, END)
        self.entry_voltagem.delete(0, END)

    def restaurar(self):
        self.frames_da_tela()
        self.widgets_frame1()

    def salvarFerramentas(self):
        global a1, a2, a3, a4, a5, a6, a7, a8, a9
        a1 = self.entry_tamanho.get()
        a2 = self.entry_materialFerramenta.get()
        a3 = self.entry_tipoFerramenta.get()
        a4 = self.entry_codigo.get()
        a5 = self.entry_unidadeMedida.get()
        a6 = self.entry_partNumber.get()
        a7 = self.entry_descricao.get()
        a8 = self.entry_fabricante.get()
        a9 = self.entry_voltagem.get()
        self.limpar_ferramentas()

    def limpaCodigo_ferramentas(self):
        self.entry_codigo_consulta.delete(0, END)

    def conecta_bd_ferramentas(self):
        self.conn = sqlite3.connect("ferramentas.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd_ferramentas(self):
        self.conn.close(); print("Desconectando ao banco de dados")
    def montaTabelas_ferramentas(self):
        self.conecta_bd_ferramentas();
        # Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ferramentas (
                cod INTEGER PRIMARY KEY,
                descFerr CHAR(40) NOT NULL,
                partNum INTEGER(20),
                fabricante CHAR(40),
                voltagem CHAR(10),
                tamanho INTEGER(10),
                uniMed CHAR(10),
                tipoFerr CHAR(20),
                matFerr CHAR(20)
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd_ferramentas()

    def add_ferramenta(self):
        self.codigo = self.entry_codigo.get()
        self.descricao = self.entry_descricao.get()
        self.partNum = self.entry_partNumber.get()
        self.fabricante = self.entry_fabricante.get()
        self.voltagem = self.entry_voltagem.get()
        self.tamanho = self.entry_tamanho.get()
        self.uniMed = self.entry_unidadeMedida.get()
        self.tipoFerr = self.entry_tipoFerramenta.get()
        self.matFerr = self.entry_materialFerramenta.get()
        self.conecta_bd_ferramentas()

        self.cursor.execute(""" INSERT INTO ferramentas (descFerr, partNum, fabricante,
         voltagem, tamanho, uniMed, tipoFerr, matFerr)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (self.descricao, self.partNum, self.fabricante, self.voltagem,
                                                 self.tamanho, self.uniMed, self.tipoFerr, self.matFerr))
        self.conn.commit()
        self.desconecta_bd_ferramentas()
        self.limpar_ferramentas()

    def select_lista(self):
        self.listaFerr.delete(*self.listaFerr.get_children())
        self.conecta_bd_ferramentas()
        lista = self.cursor.execute(""" SELECT cod, descFerr, partNum, fabricante,
         voltagem, tamanho, uniMed, tipoFerr, matFerr FROM ferramentas
            """)
        for i in lista:
            self.listaFerr.insert("", END, values=i)
            print(i)
        self.desconecta_bd_ferramentas()
    
    def OnDoubleClick_Ferramentas(self, event):
        self.entry_codigo_consulta.delete(0, END)
        self.listaFerr.selection()

        for n in self.listaFerr.selection():
            col1, col2, col3, col4, col5, col6,col7, col8, col9 = self.listaFerr.item(n, 'values')
            self.entry_codigo_consulta.insert(END, col1)
            print(self.listaFerr.selection())
            print(col1, col2, col3, col4, col5, col6,col7, col8, col9)

    def exclui_ferramenta(self):
        self.codigo_consulta = self.entry_codigo_consulta.get()
        # self.variaveis_ferramenta()
        self.conecta_bd_ferramentas()
        self.cursor.execute(f"""DELETE FROM ferramentas WHERE cod = {self.codigo_consulta}""")
        self.conn.commit()
        self.desconecta_bd_ferramentas()
        self.select_lista()
        self.entry_codigo_consulta.delete(0, END)
        
    def busca_ferramenta(self):
        self.conecta_bd_ferramentas()
        self.listaFerr.delete(*self.listaFerr.get_children())
        
        self.entry_codigo_consulta.insert(END, '%')
        codigo = self.entry_codigo_consulta.get()
        self.cursor.execute("""
                            SELECT cod, descFerr, partNum, fabricante,
                            voltagem, tamanho, uniMed, tipoFerr, matFerr 
                            FROM ferramentas 
                            WHERE cod LIKE '%s'
                            """ % codigo)
        buscaCodFerr = self.cursor.fetchall()
        for i in buscaCodFerr:
            self.listaFerr.insert("",END, values=i)
        self.desconecta_bd_ferramentas()
        self.entry_codigo_consulta.delete(0, END)

class Relatorios_Ferramentas(FuncsFerr):
    
    def printFerramentas(self):
        webbrowser.open('ferramentas.pdf')

    def geraRelatorioFerramentas(self):
        self.listaFerr.delete(*self.listaFerr.get_children())
        self.conecta_bd_ferramentas()
        self.c = canvas.Canvas("ferramentas.pdf")

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Relatório Ferramentas')


        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(50-35, 700, 'Código')
        self.c.drawString(90-35, 700, 'Descrição')
        self.c.drawString(145-35, 700, 'Part Number')
        self.c.drawString(215-35, 700, 'Fabricante')
        self.c.drawString(275-35, 700, 'Voltagem')
        self.c.drawString(330-35, 700, 'Tamanho')
        self.c.drawString(380-35, 700, 'Unidade de Med')
        self.c.drawString(450-35, 700, 'Tipo da Ferramenta')
        self.c.drawString(530-35, 700, 'Material da Ferramenta')



        lista = self.cursor.execute(""" SELECT cod, descFerr, partNum, fabricante,
         voltagem, tamanho, uniMed, tipoFerr, matFerr FROM ferramentas
            """)
        b = 20
        for i in lista:
            self.listaFerr.insert("", END, values=i)
            print(i)
            self.c.drawString(50-30, 700-b, str(i[0]))
            self.c.drawString(90-30, 700-b, str(i[1]))
            self.c.drawString(145-30, 700-b, str(i[2]))
            self.c.drawString(215-30, 700-b, str(i[3]))
            self.c.drawString(275-30, 700-b, str(i[4]))
            self.c.drawString(330-30, 700-b, str(i[5]))
            self.c.drawString(380-30, 700-b, str(i[6]))
            self.c.drawString(450-30, 700-b, str(i[7]))
            self.c.drawString(530-30, 700-b, str(i[8]))
            b+=20

        self.c.showPage()
        self.c.save()
        self.printFerramentas()
        self.desconecta_bd_ferramentas()




class FuncsTec():
    def limpar_tecnicos(self):
        self.entry_CPF.delete(0, END)
        self.entry_nome.delete(0, END)
        self.entry_telefone.delete(0, END)
        self.entry_turno.delete(0, END)
        self.entry_nomeEquipe.delete(0, END)

    def restaurar(self):
        self.frames_da_tela()
        self.widgets_frame1()

    def salvartecnicos(self):
        global a1, a2, a3, a4, a5
        a1 = self.entry_CPF.get()
        a2 = self.entry_nome.get()
        a3 = self.entry_telefone.get()
        a4 = self.entry_turno.get()
        a5 = self.entry_nomeEquipe.get()
        self.limpar_tecnicos()

    def limpaCodigo_tecnicos(self):
        self.entry_CPF_consulta.delete(0, END)

    def conecta_bd_tecnicos(self):
        self.conn = sqlite3.connect("tecnicos.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados - Técnicos")
    def desconecta_bd_tecnicos(self):
        self.conn.close(); print("Desconectando ao banco de dados - Técnicos")
    def montaTabelas_tecnicos(self):
        self.conecta_bd_tecnicos();
        # Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnicos (
                cpf CHAR(11),
                nome CHAR(40) NOT NULL,
                telefone INTEGER(20),
                turno CHAR(10),
                nomeEquipe CHAR(30)
            );
        """)
        self.conn.commit(); print("Banco de dados criado - Técnicos")
        self.desconecta_bd_tecnicos()

    def valida_cpf_resto1(self):
        
        self.cpf = self.entry_CPF.get()
        cpf_list = [int(x) for x in str(self.cpf)]
        if len(cpf_list) == 11:
            j=10
            self.cpfs= []
            for i in cpf_list[0:9]:
                i *= j
                self.cpfs.append(i)
                j -= 1
            resto = (sum(self.cpfs)*10)%11
            return resto == cpf_list[9]
        else:
            self.lb_cpf_invalido.place(relx=0.30, rely=0.80)
            return 0 ==1

    def valida_cpf_resto2(self):
        
        self.cpf = self.entry_CPF.get()
        cpf_list = [int(x) for x in str(self.cpf)]
        if len(cpf_list) == 11:
            j=11
            self.cpfs= []
            for i in cpf_list[0:10]:
                i *= j
                self.cpfs.append(i)
                j -= 1
            resto = (sum(self.cpfs)*10)%11
            return resto == cpf_list[10]
        else:
            self.lb_cpf_invalido.place(relx=0.30, rely=0.80)
            return 0 ==1

    def add_tecnico(self):
        self.valida_cpf_resto1()
        self.valida_cpf_resto2()
        if self.valida_cpf_resto2() and self.valida_cpf_resto1(): 
            self.cpf = self.entry_CPF.get()
            self.nome = self.entry_nome.get()
            self.telefone = self.entry_telefone.get()
            self.turno = self.entry_turno.get()
            self.nomeEquipe = self.entry_nomeEquipe.get()
            self.conecta_bd_tecnicos()

            self.cursor.execute(""" INSERT INTO tecnicos (cpf, nome, telefone,
            turno, nomeEquipe)
                VALUES (?, ?, ?, ?, ?)""", (self.cpf, self.nome, self.telefone, self.turno,
                                                    self.nomeEquipe))
            print(self.cpf, self.nome, self.telefone, self.turno,
                                                    self.nomeEquipe)
            self.conn.commit()
            self.desconecta_bd_tecnicos()
            self.limpar_tecnicos()
            self.lb_cpf_invalido.place(relx=0.30, rely=100)

        else:
            self.lb_cpf_invalido.place(relx=0.30, rely=0.80)

    def select_lista_tecnicos(self):
        self.listaTec.delete(*self.listaTec.get_children())
        self.conecta_bd_tecnicos()
        lista = self.cursor.execute(""" SELECT cpf, nome, telefone, 
        turno, nomeEquipe FROM tecnicos
            """)
        for i in lista:
            self.listaTec.insert("", END, values=i)
        self.desconecta_bd_tecnicos()
    
    def OnDoubleClick_Tecnicos(self, event):
        self.entry_CPF_consulta.delete(0, END)
        self.listaTec.selection()

        for n in self.listaTec.selection():
            col1, col2, col3, col4, col5= self.listaTec.item(n, 'values')
            self.entry_CPF_consulta.insert(END, col1)
            
        print(self.entry_CPF_consulta.get())

    def exclui_tecnico(self):
        self.CPF_consulta = self.entry_CPF_consulta.get()
        print(self.CPF_consulta)
        self.conecta_bd_tecnicos()
        # self.CPF_consulta = int(self.CPF_consulta)
        self.cursor.execute(f"""DELETE FROM tecnicos WHERE cpf = {self.CPF_consulta} """, )
        self.conn.commit()
        self.desconecta_bd_tecnicos()
        self.select_lista_tecnicos()
        self.entry_CPF_consulta.delete(0, END)
        print(self.CPF_consulta)
    
    def busca_tecnico(self):
        self.conecta_bd_tecnicos()
        self.listaTec.delete(*self.listaTec.get_children())
        
        self.entry_CPF_consulta.insert(END, '%')
        cpf = self.entry_CPF_consulta.get()
        self.cursor.execute("""
                            SELECT  cpf, nome, telefone, turno, nomeEquipe
                            FROM tecnicos 
                            WHERE cpf LIKE '%s'
                            """ % cpf)
        buscaCpfTec = self.cursor.fetchall()
        for i in buscaCpfTec:
            self.listaTec.insert("",END, values=i)
        self.desconecta_bd_tecnicos()
        self.entry_CPF_consulta.delete(0, END)


class Relatorios_Tecnicos(FuncsTec):
    
    def printtecnicos(self):
        webbrowser.open('tecnicos.pdf')

    def geraRelatorioTecnicos(self):
        self.listaTec.delete(*self.listaTec.get_children())
        self.conecta_bd_tecnicos()
        self.c = canvas.Canvas("tecnicos.pdf")

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Relatório tecnicos')


        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(50-35, 700, 'CPF')
        self.c.drawString(90-35, 700, 'Nome Completo')
        self.c.drawString(145-35, 700, 'Telefone')
        self.c.drawString(215-35, 700, 'Turno')
        self.c.drawString(275-35, 700, 'Nome da Equipe')



        lista = self.cursor.execute(""" SELECT cpf, nome, telefone, 
        turno, nomeEquipe FROM tecnicos
            """)
        b = 20
        for i in lista:
            self.listaTec.insert("", END, values=i)
            print(i)
            self.c.drawString(50-30, 700-b, str(i[0]))
            self.c.drawString(90-30, 700-b, str(i[1]))
            self.c.drawString(145-30, 700-b, str(i[2]))
            self.c.drawString(215-30, 700-b, str(i[3]))
            self.c.drawString(275-30, 700-b, str(i[4]))
            b+=20

        self.c.showPage()
        self.c.save()
        self.printtecnicos()
        self.desconecta_bd_tecnicos()





class Application(Relatorios_Ferramentas, Relatorios_Tecnicos):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.montaTabelas_tecnicos()
        self.montaTabelas_ferramentas()


        root.mainloop()

    def tela(self):
        self.root.title("Gerenciador de tecnicos")
        self.root.configure(background='#1e3743')
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.maxsize(width=1200, height=900)
        self.root.minsize(width=850, height=600)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.47, relheight=0.96)
        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame_2.place(relx=0.50, rely=0.02, relwidth=0.47, relheight=0.96)

    def frame_consultar_ferramentas(self):
        self.conFerramentas = Frame(self.conFerramentas, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.conFerramentas.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def widgets_frame1(self):
        # Título
        lb_titulo = Label(self.frame_1, text="Bem-Vindo", bg='#dfe3ee', font=('verdana', 14))
        lb_titulo.pack()
        # Botão Ferramentas
        self.bt_ferramentas = Button(self.frame_1, text="Ferramentas", bd=4, fg='black', font=('verdana', 14, 'bold'),
                                     bg='#00BFFF', activebackground='#2E9AFE', activeforeground="white",
                                     command=self.bt_ferramentas_frame2)
        self.bt_ferramentas.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.15)

        # Botão Técnicos
        self.bt_tecnicos = Button(self.frame_1, text="Técnicos", bd=4, fg='black', font=('verdana', 14, 'bold'),
                                  bg='#00BFFF', activebackground='#2E9AFE', activeforeground="white",
                                  command=self.bt_tecnicos_frame2)
        self.bt_tecnicos.place(relx=0.02, rely=0.27, relwidth=0.96, relheight=0.15)
        # Botão Reserva de Ferramentas
        self.bt_reservaFerramentas = Button(self.frame_1, text="Reserva de Ferramentas", bd=4, fg='black',
                                            font=('verdana', 14, 'bold'), bg='#00BFFF', activebackground='#2E9AFE',
                                            activeforeground="white", command=self.bt_reserva_frame2)
        self.bt_reservaFerramentas.place(relx=0.02, rely=0.44, relwidth=0.96, relheight=0.15)

    def bt_ferramentas_frame2(self):
        self.restaurar()
        # Título do frame
        lb_ferramentas = Label(self.frame_2, text="Ferramentas", bg='#dfe3ee', font=('verdana', 14))
        lb_ferramentas.place(relx=0.02, rely=0.02)
        # Botão Cadastrar Ferramentas
        bt_cadastrarFerramentas = Button(self.frame_2, text="Cadastrar Ferramenta", bd=4, fg='black',
                                         font=('verdana', 14, 'bold'),
                                         bg='#00BFFF', activebackground='#2E9AFE', activeforeground="white",
                                         command=self.cadastrar_ferramentas)
        bt_cadastrarFerramentas.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.15)
        # Botão Consultar Ferramentas
        bt_conFerramentas = Button(self.frame_2, text="Consultar Ferramenta", bd=4, fg='black',
                                         font=('verdana', 14, 'bold'), bg='#00BFFF', activebackground='#2E9AFE',
                                         activeforeground="white", command=self.consultar_ferramentas)
        bt_conFerramentas.place(relx=0.02, rely=0.27, relwidth=0.96, relheight=0.15)
        bt_x = Button(self.frame_2, text='X', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                      activeforeground="white", command=self.restaurar)
        bt_x.place(relx=0.96, rely=0, relwidth=0.04, relheight=0.04)



    def bt_tecnicos_frame2(self):
        # Título do frame
        self.restaurar()
        lb_tecnicos = Label(self.frame_2, text="Técnicos", bg='#dfe3ee', font=('verdana', 14))
        lb_tecnicos.place(relx=0.02, rely=0.02)
        # Botão Cadastrar Técnicos
        bt_cadastrarTecnico = Button(self.frame_2, text="Cadastrar Técnico", bd=4, fg='black',
                                     font=('verdana', 14, 'bold'),
                                     bg='#00BFFF', activebackground='#2E9AFE', activeforeground="white",
                                     command=self.cadastrar_tecnico)
        bt_cadastrarTecnico.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.15)
        # Botão Consultar Técnicos
        bt_consultarTecnicos = Button(self.frame_2, text="Consultar Técnicos", bd=4, fg='black',
                                      font=('verdana', 14, 'bold'),
                                      bg='#00BFFF', activebackground='#2E9AFE', activeforeground="white",
                                      command=self.consultar_tecnico)
        bt_consultarTecnicos.place(relx=0.02, rely=0.27, relwidth=0.96, relheight=0.15)
        bt_x = Button(self.frame_2, text='X', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                      activeforeground="white", command=self.restaurar)
        bt_x.place(relx=0.96, rely=0, relwidth=0.04, relheight=0.04)

    def bt_reserva_frame2(self):
        self.restaurar()
        lb_reserva = Label(self.frame_2, text="EM BREVE!", bg='#dfe3ee', font=('verdana', 48, 'bold'), fg='#610B21')
        lb_reserva.place(relx=0, rely=0.4)

        bt_x = Button(self.frame_2, text='X', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                      activeforeground="white", command=self.restaurar)
        bt_x.place(relx=0.96, rely=0, relwidth=0.04, relheight=0.04)

    def cadastrar_ferramentas(self):
        self.restaurar()

        bt_x = Button(self.frame_2, text='X', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                      activeforeground="white", command=self.restaurar)
        bt_x.place(relx=0.96, rely=0, relwidth=0.04, relheight=0.04)

        bt_salvar = Button(self.frame_2, text='Salvar', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                           activeforeground="white", command=self.add_ferramenta)
        bt_salvar.place(relx=0.01, rely=0.53, relwidth=0.83, relheight=0.05)

        lb_titulo = Label(self.frame_2, text="Cadastrar Ferramenta", bg='#dfe3ee', font=('verdana', 14))
        lb_titulo.place(relx=0.01, rely=0.01)

        lb_codigo = Label(self.frame_2, text="Código", font=('verdana', 12), bg='#dfe3ee')
        lb_codigo.place(relx=0.01, rely=0.1)
        self.entry_codigo = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_codigo.place(relx=0.01, rely=0.16, relheight=0.04, relwidth=0.14)

        lb_partNumber = Label(self.frame_2, text="Part Number", font=('verdana', 12), bg='#dfe3ee')
        lb_partNumber.place(relx=0.20, rely=0.1)
        self.entry_partNumber = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_partNumber.place(relx=0.20, rely=0.16, relheight=0.04, relwidth=0.30)

        lb_fabricante = Label(self.frame_2, text="Fabricante", font=('verdana', 12), bg='#dfe3ee')
        lb_fabricante.place(relx=0.55, rely=0.1)
        self.entry_fabricante = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_fabricante.place(relx=0.55, rely=0.16, relheight=0.04, relwidth=0.30)

        lb_descricao = Label(self.frame_2, text="Descrição", font=('verdana', 12), bg='#dfe3ee')
        lb_descricao.place(relx=0.01, rely=0.20)
        self.entry_descricao = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_descricao.place(relx=0.01, rely=0.26, relheight=0.04, relwidth=0.84)

        lb_voltagem = Label(self.frame_2, text="Voltagem", font=('verdana', 12), bg='#dfe3ee')
        lb_voltagem.place(relx=0.01, rely=0.30)
        self.entry_voltagem = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_voltagem.place(relx=0.01, rely=0.36, relheight=0.04, relwidth=0.19)

        lb_tamanho = Label(self.frame_2, text="Tamanho", font=('verdana', 12), bg='#dfe3ee')
        lb_tamanho.place(relx=0.25, rely=0.30)
        self.entry_tamanho = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_tamanho.place(relx=0.25, rely=0.36, relheight=0.04, relwidth=0.19)

        lb_unidadeMedida = Label(self.frame_2, text="Unidade de Medida", font=('verdana', 12), bg='#dfe3ee')
        lb_unidadeMedida.place(relx=0.49, rely=0.30)
        self.entry_unidadeMedida = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_unidadeMedida.place(relx=0.55, rely=0.36, relheight=0.04, relwidth=0.29)

        lb_tipoFerramenta = Label(self.frame_2, text="Tipo da Ferramenta", font=('verdana', 12), bg='#dfe3ee')
        lb_tipoFerramenta.place(relx=0.01, rely=0.40)
        self.entry_tipoFerramenta = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_tipoFerramenta.place(relx=0.01, rely=0.46, relheight=0.04, relwidth=0.39)

        lb_materialFerramenta = Label(self.frame_2, text="Material da Ferramenta", font=('verdana', 12), bg='#dfe3ee')
        lb_materialFerramenta.place(relx=0.43, rely=0.40)
        self.entry_materialFerramenta = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_materialFerramenta.place(relx=0.43, rely=0.46, relheight=0.04, relwidth=0.41)

    def consultar_ferramentas(self):
        self.tela2 = Tk()
        self.tela2.title("Consultar Ferramentas")
        self.tela2.configure(background='#1e3743')
        self.tela2.geometry("1200x700")
        self.tela2.resizable(True, True)
        self.tela2.maxsize(width=1800, height=900)
        self.tela2.minsize(width=900, height=600)

        self.conFerramentas = Frame(self.tela2, bd=4, bg='#dfe3ee', highlightbackground='#759fe6',
                             highlightthickness=2)
        self.conFerramentas.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        bt_x = Button(self.conFerramentas, text='X', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                      activeforeground="white", command= self.tela2.destroy)
        bt_x.place(relx=0.96, rely=0, relwidth=0.04, relheight=0.04)

        lb_titulo = Label(self.conFerramentas, text="Consultar Ferramenta", bg='#dfe3ee', font=('verdana', 14))
        lb_titulo.place(relx=0.01, rely=0.01)

        lb_codigo = Label(self.conFerramentas, text="Código", font=('verdana', 12), bg='#dfe3ee')
        lb_codigo.place(relx=0.01, rely=0.1)
        self.entry_codigo_consulta = Entry(self.conFerramentas, fg='red', font=('verdana', 10),)
        self.entry_codigo_consulta.place(relx=0.01, rely=0.16, relheight=0.04, relwidth=0.14)

        bt_conFerramentas = Button(self.conFerramentas, text='Consultar', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                                         activeforeground="white",
                                         font=('verdana', 14, 'bold'), command=self.busca_ferramenta)
        bt_conFerramentas.place(relx=0.17, rely=0.1, relwidth=0.10, relheight=0.1)

        bt_limpaCod = Button(self.conFerramentas, text='Limpar', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                             activeforeground="white", command=self.limpaCodigo_ferramentas, font=('verdana', 14, 'bold'))
        bt_limpaCod.place(relx=0.4, rely=0.1, relwidth=0.10, relheight=0.1)

        bt_excluiFerr = Button(self.conFerramentas, text='Excluir', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                             activeforeground="white", command=self.exclui_ferramenta, font=('verdana', 14, 'bold'))
        bt_excluiFerr.place(relx=0.63, rely=0.1, relwidth=0.10, relheight=0.1)
        self.listaFerramentas()
        self.select_lista()

        bt_imprime = Button(self.conFerramentas, text='Imprimir', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                             activeforeground="white", command=self.geraRelatorioFerramentas, font=('verdana', 14, 'bold'))
        bt_imprime.place(relx=0.86, rely=0.1, relwidth=0.10, relheight=0.1)


    def listaFerramentas(self):
        self.listaFerr = ttk.Treeview(self.conFerramentas, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6",
                                                                       "col7", "col8", "col9", "col10"))
        self.listaFerr.heading("#0", text="")
        self.listaFerr.heading("#1", text="Codigo")
        self.listaFerr.heading("#2", text="Descrição")
        self.listaFerr.heading("#3", text="Part Number")
        self.listaFerr.heading("#4", text="Fabricante")
        self.listaFerr.heading("#5", text="Voltagem")
        self.listaFerr.heading("#6", text="Tamanho")
        self.listaFerr.heading("#7", text="Medida")
        self.listaFerr.heading("#8", text="Tipo")
        self.listaFerr.heading("#9", text="Material")

        self.listaFerr.column("#0", width=0)
        self.listaFerr.column("#1", width=50)
        self.listaFerr.column("#2", width=320)
        self.listaFerr.column("#3", width=110)
        self.listaFerr.column("#4", width=110)
        self.listaFerr.column("#5", width=85)
        self.listaFerr.column("#6", width=85)
        self.listaFerr.column("#7", width=85)
        self.listaFerr.column("#8", width=100)
        self.listaFerr.column("#9", width=100)

        self.listaFerr.place(relx=0.01, rely=0.3, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.conFerramentas, orient='vertical')
        self.listaFerr.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaFerr.bind("<Double-1>", self.OnDoubleClick_Ferramentas)


    def cadastrar_tecnico(self):
        self.restaurar()

        bt_x = Button(self.frame_2, text='X', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                      activeforeground="white", command=self.restaurar)
        bt_x.place(relx=0.96, rely=0, relwidth=0.04, relheight=0.04)

        bt_salvar = Button(self.frame_2, text='Salvar', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                           activeforeground="white", command=self.add_tecnico)
        bt_salvar.place(relx=0.01, rely=0.53, relwidth=0.83, relheight=0.05)

        lb_titulo = Label(self.frame_2, text="Cadastrar Técnico", bg='#dfe3ee', font=('verdana', 14))
        lb_titulo.place(relx=0.01, rely=0.01)

        lb_CPF = Label(self.frame_2, text="CPF", font=('verdana', 12), bg='#dfe3ee')
        lb_CPF.place(relx=0.01, rely=0.1)
        self.entry_CPF = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_CPF.place(relx=0.01, rely=0.16, relheight=0.04, relwidth=0.60)

        lb_nome = Label(self.frame_2, text="Nome Completo", font=('verdana', 12), bg='#dfe3ee')
        lb_nome.place(relx=0.01, rely=0.2)
        self.entry_nome = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_nome.place(relx=0.01, rely=0.26, relheight=0.04, relwidth=0.85)

        lb_telefone = Label(self.frame_2, text="Telefone celular ou rádio", font=('verdana', 12), bg='#dfe3ee')
        lb_telefone.place(relx=0.01, rely=0.30)
        self.entry_telefone = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_telefone.place(relx=0.01, rely=0.36, relheight=0.04, relwidth=0.50)

        lb_turno = Label(self.frame_2, text="Turno", font=('verdana', 12), bg='#dfe3ee')
        lb_turno.place(relx=0.66, rely=0.10)
        uniTurno = ['Manhã','Tarde','Noite']
        self.entry_turno = ttk.Combobox(self.frame_2, value=uniTurno)
        self.entry_turno.place(relx=0.66, rely=0.16, relheight=0.04, relwidth=0.25)

        lb_nomeEquipe = Label(self.frame_2, text="Nome da Equipe", font=('verdana', 12), bg='#dfe3ee')
        lb_nomeEquipe.place(relx=0.01, rely=0.40)
        self.entry_nomeEquipe = Entry(self.frame_2, fg='red', font=('verdana', 10))
        self.entry_nomeEquipe.place(relx=0.01, rely=0.46, relheight=0.04, relwidth=0.50)

        self.lb_cpf_invalido = Label(self.frame_2, text="CPF Inválido!", font=('verdana', 12), bg='#ff0000')


    def consultar_tecnico(self):
        self.tela2 = Tk()
        self.tela2.title("Consultar Técnico")
        self.tela2.configure(background='#1e3743')
        self.tela2.geometry("1200x700")
        self.tela2.resizable(True, True)
        self.tela2.maxsize(width=1800, height=900)
        self.tela2.minsize(width=900, height=600)

        self.conTecnicos = Frame(self.tela2, bd=4, bg='#dfe3ee', highlightbackground='#759fe6',
                             highlightthickness=2)
        self.conTecnicos.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        bt_x = Button(self.conTecnicos, text='X', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                      activeforeground="white", command= self.tela2.destroy)
        bt_x.place(relx=0.96, rely=0, relwidth=0.04, relheight=0.04)

        lb_titulo = Label(self.conTecnicos, text="Consultar Técnico", bg='#dfe3ee', font=('verdana', 14))
        lb_titulo.place(relx=0.01, rely=0.01)

        lb_CPF = Label(self.conTecnicos, text="CPF", font=('verdana', 12), bg='#dfe3ee')
        lb_CPF.place(relx=0.01, rely=0.1)
        self.entry_CPF_consulta = Entry(self.conTecnicos, fg='red', font=('verdana', 10))
        self.entry_CPF_consulta.place(relx=0.01, rely=0.16, relheight=0.04, relwidth=0.14)

        bt_conTecnicos = Button(self.conTecnicos, text='Consultar', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                                         activeforeground="white",
                                         font=('verdana', 14, 'bold'), command=self.busca_tecnico)
        bt_conTecnicos.place(relx=0.17, rely=0.1, relwidth=0.10, relheight=0.1)

        bt_limpaCod = Button(self.conTecnicos, text='Limpar', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                             activeforeground="white", command=self.limpaCodigo_tecnicos, font=('verdana', 14, 'bold'))
        bt_limpaCod.place(relx=0.4, rely=0.1, relwidth=0.10, relheight=0.1)

        bt_excluiTec = Button(self.conTecnicos, text='Excluir', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                             activeforeground="white", command=self.exclui_tecnico, font=('verdana', 14, 'bold'))
        bt_excluiTec.place(relx=0.63, rely=0.1, relwidth=0.10, relheight=0.1)
        self.listaTecnicos()
        self.select_lista_tecnicos()

        bt_imprime = Button(self.conTecnicos, text='Imprimir', bd=2, bg='#00BFFF', activebackground='#2E9AFE',
                             activeforeground="white", command=self.geraRelatorioTecnicos, font=('verdana', 14, 'bold'))
        bt_imprime.place(relx=0.86, rely=0.1, relwidth=0.10, relheight=0.1)
    


    def listaTecnicos(self):
        self.listaTec = ttk.Treeview(self.conTecnicos, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        self.listaTec.heading("#0", text="")
        self.listaTec.heading("#1", text="CPF")
        self.listaTec.heading("#2", text="Turno")
        self.listaTec.heading("#3", text="Nome Completo")
        self.listaTec.heading("#4", text="Telefone ou Rádio")
        self.listaTec.heading("#5", text="Nome da Equipe")


        self.listaTec.column("#0", width=0)
        self.listaTec.column("#1", width=50)
        self.listaTec.column("#2", width=320)
        self.listaTec.column("#3", width=110)
        self.listaTec.column("#4", width=110)
        self.listaTec.column("#5", width=85)


        self.listaTec.place(relx=0.01, rely=0.3, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.conTecnicos, orient='vertical')
        self.listaTec.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaTec.bind("<Double-1>", self.OnDoubleClick_Tecnicos)

Application()