from tkinter import *
from tkinter import ttk
from datetime import datetime
import sqlite3

root =Tk()

class Func():
#Funções de database, autoexplicativas
    def conecta_db(self):
        self.conn = sqlite3.connect("anotações_bd")
        self.cursor = self.conn.cursor()

    def desconecta_db(self):
        self.conn.close()

    def createTable(self):
        self.conecta_db(); print(" Conectado ao servidor e banco de dados.")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS notes(
                          id_arq integer primary key,
                          nome_arq char(40),
                          conteudo_arq text,
                          datatime date);""")
        self.conn.commit(); print(" Tabela criada/já existente")
        self.desconecta_db()

    def variaveis(self):
        self.texto = self.content.get("1.0", END)
        self.nome = "HOLDPLACE NOME"
        self.datetime = datetime.now()
        
    def salvar_arq(self):
        self.conecta_db()
        self.variaveis()
        self.cursor.execute("""INSERT INTO notes(nome_arq, conteudo_arq, datatime)
                          VALUES (?, ?, ?)""", (self.nome, self.texto, self.datetime))
        self.conn.commit(); print(" Dados cadastrados.")
        self.listagem_fr2()
        self.desconecta_db()

    def abrir_arq(self):
        self.conecta_db()
        self.conn.execute("""SELECT nome_arq, conteudo_arq FROM notes
                          ORDER BY nome_arq""")
        self.desconecta_db()

    def listagem_fr2(self):
        self.conecta_db()
        self.variaveis()
        self.listaTV.delete(*self.listaTV.get_children())
        lista2 = self.cursor.execute("""SELECT nome_arq, length(conteudo_arq), datatime 
                                    FROM notes
                                    ORDER BY nome_arq;""")
        for i in lista2:
            self.listaTV.insert('', END, values = i)
        self.desconecta_db()
    
    def doubleClick(self, event):
        self.listaTV.selection()
        for i in self.listaTV.selection():
            col1,col2,col3 = self.listaTV.item(i, "values")
            self.nome.insert(END, col1)
            self.len(self.texto).insert(END, col2)
            self.datetime.insert(END, col3)

class App(Func):
#Função de iniciação
    def __init__(self):
        self.root = root
        self.janela = None
        self.tela()
        self.frames()
        self.nota()
        self.menu()
        self.createTable()
        root.mainloop()
#Widget principal
    def tela(self):
        self.root.title("Holdplace")
        self.root.configure(background="#ffffff")
        self.root.geometry("1020x720")
        self.root.resizable(True, True)
        self.root.maxsize(width = 1020, height = 640)
        self.root.minsize(width = 480, height = 640)
#Widget do buscador 
    def buscador(self):
        self.janela = Toplevel(self.root)
        self.janela.title("ARQUIVOS NO DATABASE")
        self.janela.configure(background="#ffffff")
        self.janela.geometry("480x640")
        self.janela.resizable(False, False)
        self.janela.maxsize(width = 1020, height = 640)
        self.janela.minsize(width = 480, height = 640)
    #Chamadas de funções 
        self.menu_arqs()
        self.bus_lista()
        self.listagem_fr2()

#Frame principal
    def frames(self):
        self.frame = Frame(
            self.root,
            bd = 2,
            bg = "#0a0a0a",
            highlightbackground= "#d3d3d3",
            highlightthickness= 2
            )
        self.frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        self.frame2 = Frame(self.janela,
                            bd = 2,
                            bg = "#0a0a0a",
                            highlightbackground= "#20b2aa",
                            highlightthickness= 2)
        self.frame2.place(relx= 0, rely= 0, relheight= 1, relwidth= 1)
#Entrada de texto  na tela principal
    def nota(self):
        self.content = Text(self.root,
                            font = ("Verdana", "12", "bold"),
                            bg= "#2e2e2e",
                            insertbackground = "#ffffff",
                            fg= "#ffffff",
                            wrap = "word",
                            cursor = "circle" )
        self.content.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
#Menu principal
    def menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label = "Opções", menu = filemenu)
        menubar.add_cascade(label = "Post-It", menu = filemenu2)

        filemenu.add_command(label = "Salvar", command = self.salvar_arq)
        filemenu.add_command(label = "Abrir", command = self.buscador)
        filemenu.add_command(label ="Sair", command = Quit)
#Menu do buscador 
    def menu_arqs(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)

        def Quit(): self.janela.destroy()

        menubar. add_cascade(label = "Opções", menu  = filemenu)
        filemenu.add_command(label = "Voltar", command= Quit)
#Lista para o buscador
    def bus_lista(self):
        self.listaTV = ttk.Treeview(self.janela,
                                  height = 3,
                                  column = ("col1", "col2","col3"))
        self.listaTV.heading("#00", text = " ")
        self.listaTV.heading("#01", text = "Nome do Arquivo")
        self.listaTV.heading("#02", text = "Tamanho do Arquivo")
        self.listaTV.heading("#03", text = "Ultima Atualização")

        self.listaTV.column("#00", width =1)
        self.listaTV.column("#01", width = 100)
        self.listaTV.column("#02", width = 120)
        self.listaTV.column("#03", width = 150)

        self.listaTV.place(relx= 0, rely=0, relheight= 1, relwidth= 1)
        self.listaTV.bind('<Double-1>', self.doubleClick)
#
App()
