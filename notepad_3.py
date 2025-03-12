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
    
    def limpar_entry(self):
        self.cod = self.cod_entry.delete(0, END)
        self.texto = self.content.delete("1.0", END)

    def createTable(self):
        self.conecta_db(); print(" Conectado ao servidor e banco de dados.")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS notes(
                          id_arq integer primary key,
                          nome_arq char(40),
                          conteudo_arq text,
                          datatime date);""")
        self.conn.commit(); print(" Tabela criada/já existente")

    def variaveis(self):
        if self.cod_entry:
            self.cod = self.cod_entry.get()
        else:
            self.cod = 1
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
        self.limpar_entry()
        self.desconecta_db()

    def apagar_arq(self):
        self.conecta_db()
        self.variaveis()
        self.cursor.execute("""DELETE FROM notes WHERE id_arq = ?""", (self.cod,))
        self.conn.commit(); print(" Arquivos apagados." + self.cod)
        self.desconecta_db()
        self.limpar_entry()
        self.listagem_fr2()

    def abrir_arq(self):
        self.conecta_db()
        self.conn.execute("""SELECT nome_arq, conteudo_arq FROM notes
                          ORDER BY nome_arq""")
        self.limpar_entry()
        self.desconecta_db()

    def alterar_arq(self):
        self.conecta_db()
        self.variaveis()
        self.cursor.execute("""UPDATE notes
                            SET nome_arq = ?, conteudo_arq = ?, datatime = ?
                            WHERE id_arq = ?""", (self.nome, self.texto, self.datetime, self.cod))
        self.conn.commit(); print(" Dados alterados.")
        self.listagem_fr2()
        self.limpar_entry()
        self.desconecta_db()

    def listagem_fr2(self):
        self.conecta_db()
        self.listaTV.delete(*self.listaTV.get_children())
        lista2 = self.cursor.execute("""SELECT id_arq, nome_arq, length(conteudo_arq), datatime 
                                    FROM notes
                                    ORDER BY nome_arq;""")
        for i in lista2:
            self.listaTV.insert('', END, values = i)
        self.limpar_entry()
        self.desconecta_db()
    
    def doubleClick(self, event):
        self.limpar_entry()
        self.listaTV.selection()
        for i in self.listaTV.selection():
            col1,col2,col3,col4 = self.listaTV.item(i, "values")
            self.cod_entry.insert(END, col1)
            self.content.insert(END, col2)


class App(Func):
#Função de iniciação
    def __init__(self):
        self.root = root
        self.janela = None
        self.frames()
        self.nota()
        self.menu()
        self.createTable()
        self.buscador()
        self.tela()
        self.variaveis()
        print("FUNCIONANDO>.....................")
        root.mainloop()

#Widget principal
    def tela(self):
        self.root.title("Holdplace")
        self.root.configure(background="#ffffff")
        self.root.geometry("1020x720")
        self.root.resizable(True, True)
        self.root.maxsize(width = 1020, height = 640)
        self.root.minsize(width = 480, height = 640)
    #Chama as funções da janela principal
        self.janela.withdraw()

#Widget do buscador 
    def buscador(self):
        self.janela = Toplevel(self.root)
        self.janela.title("ARQUIVOS NO DATABASE")
        self.janela.configure(background="#ffffff")
        self.janela.geometry("480x640")
        self.janela.resizable(False, False)
        self.janela.maxsize(width = 1020, height = 640)
        self.janela.minsize(width = 480, height = 640)
    #Chamadas de funções da janela do buscador 
        self.janela.deiconify()
        self.menu_arqs()
        self.widgets_2()
        self.bus_lista()
        self.listagem_fr2()
        self.janela.protocol("WM_DELETE_WINDOW", self.janela.withdraw)

#Frame principal
    def frames(self):
        self.frame = Frame(
            self.root,
            bd = 2,
            bg = "#0a0a0a",
            highlightbackground= "#d3d3d3",
            highlightthickness= 2)
        self.frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        
#Widgets janela 
    def widgets_2(self):
        self.frame2 = Frame(
            self.janela,
            bd = 2,
            bg = "#ffffff",
            highlightbackground= "#20b2aa")
        self.frame2.place(relx= 0, rely= 0, relheight= 1, relwidth= 1)
        self.cod_entry = Entry(self.frame2, 
                                bd = 0,
                                bg = "#f3f3f3")
        self.cod_entry.place(relx = 0,rely = 0,relwidth = 0.1, relheight = 0.03)
        self.pesq_entry = Entry(self.frame2,
                                bd = 0,
                                bg = "#f3f3f3")
        self.pesq_entry.place(relx = 0.12,rely = 0,relwidth = 0.15, relheight = 0.03)
        self.variaveis()

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
        filemenu.add_command(label = "Abrir Configurações", command = self.buscador)
        filemenu.add_command(label ="Sair", command = Quit)

#Menu do buscador 
    def menu_arqs(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)

        def Quit(): 
            self.janela.destroy()
            print("funcionando2>..................")

        menubar.add_cascade(label = "Opções", menu  = filemenu)
        filemenu.add_command(label = "Apagar", command = self.apagar_arq)
        filemenu.add_command(label = "Salvar", command = self.alterar_arq)
        filemenu.add_command(label = "Voltar", command= Quit)

#Lista para o buscador
    def bus_lista(self):
        self.listaTV = ttk.Treeview(self.janela,
                                  height = 3,
                                  column = ("col1", "col2","col3","col4"))
        self.listaTV.heading("#00", text = " ")
        self.listaTV.heading("#01", text = "ID")
        self.listaTV.heading("#02", text = "Nome do Arquivo")
        self.listaTV.heading("#03", text = "Tamanho do Arquivo")
        self.listaTV.heading("#04", text = "Ultima Atualização")

        self.listaTV.column("#00", width = 1)
        self.listaTV.column("#01", width = 15)
        self.listaTV.column("#02", width = 100)
        self.listaTV.column("#03", width = 120)
        self.listaTV.column("#04", width = 150)

        self.listaTV.place(relx= 0, rely=0.04, relheight= 1, relwidth= 1)
        self.listaTV.bind('<Button-1>', self.doubleClick)
        self.listaTV.bind('<Return>', self.doubleClick)
#
App()
