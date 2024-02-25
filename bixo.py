import sqlite3
import tkinter as tk
from tkinter import messagebox

class OperacoesCRUD:
    def __init__(self):
        self.conn = sqlite3.connect('mercado.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS estoque (
                            codigo INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            quantidade INTEGER,
                            preco REAL
                            )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                            codigo INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            telefone TEXT,
                            endereco TEXT
                            )''')
        self.conn.commit()

    def inserir_estoque(self, produto):
        self.c.execute('''INSERT INTO estoque (nome, quantidade, preco) 
                          VALUES (?, ?, ?)''', (produto.nome, produto.quantidade, produto.preco))
        self.conn.commit()

    def inserir_cliente(self, cliente):
        self.c.execute('''INSERT INTO clientes (nome, telefone, endereco) 
                          VALUES (?, ?, ?)''', (cliente.nome, cliente.telefone, cliente.endereco))
        self.conn.commit()

    def alterar_estoque(self, codigo, novo_produto):
        self.c.execute('''UPDATE estoque SET nome=?, quantidade=?, preco=? WHERE codigo=?''',
                       (novo_produto.nome, novo_produto.quantidade, novo_produto.preco, codigo))
        self.conn.commit()

    def alterar_cliente(self, codigo, novo_cliente):
        self.c.execute('''UPDATE clientes SET nome=?, telefone=?, endereco=? WHERE codigo=?''',
                       (novo_cliente.nome, novo_cliente.telefone, novo_cliente.endereco, codigo))
        self.conn.commit()

    def pesquisar_por_nome(self, nome):
        resultados = []
        for row in self.c.execute('''SELECT * FROM estoque WHERE nome LIKE ?''', ('%' + nome + '%',)):
            resultados.append(Produto(row[1], row[2], row[3]))
        for row in self.c.execute('''SELECT * FROM clientes WHERE nome LIKE ?''', ('%' + nome + '%',)):
            resultados.append(Cliente(row[1], row[2], row[3]))
        return resultados

    def remover_estoque(self, codigo):
        self.c.execute('''DELETE FROM estoque WHERE codigo=?''', (codigo,))
        self.conn.commit()

    def remover_cliente(self, codigo):
        self.c.execute('''DELETE FROM clientes WHERE codigo=?''', (codigo,))
        self.conn.commit()

    def listar_todos_estoque(self):
        resultados = []
        for row in self.c.execute('''SELECT * FROM estoque'''):
            resultados.append(Produto(row[1], row[2], row[3]))
        return resultados

    def listar_todos_clientes(self):
        resultados = []
        for row in self.c.execute('''SELECT * FROM clientes'''):
            resultados.append(Cliente(row[1], row[2], row[3]))
        return resultados

class Produto:
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

class Cliente:
    def __init__(self, nome, telefone, endereco):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gerenciamento do Mercado")

        self.operacoes_crud = OperacoesCRUD()

        self.label = tk.Label(master, text="Escolha uma operação:")
        self.label.pack()
        self.screen = tk.Canvas(master,height=20, width=200)
        self.screen.pack()

        self.inserir_produto_button = tk.Button(master, text="Inserir Produto", command=self.janela_inserir_produto)
        self.inserir_produto_button.pack()

        self.inserir_cliente_button = tk.Button(master, text="Inserir Cliente", command=self.janela_inserir_cliente)
        self.inserir_cliente_button.pack()

        self.alterar_produto_button = tk.Button(master, text="Alterar Produto", command=self.janela_alterar_produto)
        self.alterar_produto_button.pack()

        self.alterar_cliente_button = tk.Button(master, text="Alterar Cliente", command=self.janela_alterar_cliente)
        self.alterar_cliente_button.pack()

        self.remover_produto_button = tk.Button(master, text="Remover Produto", command=self.janela_remover_produto)
        self.remover_produto_button.pack()

        self.remover_cliente_button = tk.Button(master, text="Remover Cliente", command=self.janela_remover_cliente)
        self.remover_cliente_button.pack()

        self.pesquisar_button = tk.Button(master, text="Pesquisar", command=self.janela_pesquisar)
        self.pesquisar_button.pack()

    def janela_inserir_produto(self):
        inserir_produto_window = tk.Toplevel(self.master)
        inserir_produto_window.title("Inserir Produto")

        label_nome = tk.Label(inserir_produto_window, text="Nome:")
        label_nome.pack()
        entry_nome = tk.Entry(inserir_produto_window)
        entry_nome.pack()

        label_quantidade = tk.Label(inserir_produto_window, text="Quantidade:")
        label_quantidade.pack()
        entry_quantidade = tk.Entry(inserir_produto_window)
        entry_quantidade.pack()

        label_preco = tk.Label(inserir_produto_window, text="Preço:")
        label_preco.pack()
        entry_preco = tk.Entry(inserir_produto_window)
        entry_preco.pack()

        def inserir_produto():
            nome = entry_nome.get()
            quantidade = int(entry_quantidade.get())
            preco = float(entry_preco.get())
            produto = Produto(nome, quantidade, preco)
            self.operacoes_crud.inserir_estoque(produto)
            messagebox.showinfo("Sucesso", "Produto inserido com sucesso!")
            inserir_produto_window.destroy()

        button_inserir = tk.Button(inserir_produto_window, text="Inserir", command=inserir_produto)
        button_inserir.pack()

    def janela_inserir_cliente(self):
        inserir_cliente_window = tk.Toplevel(self.master)
        inserir_cliente_window.title("Inserir Cliente")

        label_nome = tk.Label(inserir_cliente_window, text="Nome:")
        label_nome.pack()
        entry_nome = tk.Entry(inserir_cliente_window)
        entry_nome.pack()

        label_telefone = tk.Label(inserir_cliente_window, text="Telefone:")
        label_telefone.pack()
        entry_telefone = tk.Entry(inserir_cliente_window)
        entry_telefone.pack()

        label_endereco = tk.Label(inserir_cliente_window, text="Endereço:")
        label_endereco.pack()
        entry_endereco = tk.Entry(inserir_cliente_window)
        entry_endereco.pack()

        def inserir_cliente():
            nome = entry_nome.get()
            telefone = entry_telefone.get()
            endereco = entry_endereco.get()
            cliente = Cliente(nome, telefone, endereco)
            self.operacoes_crud.inserir_cliente(cliente)
            messagebox.showinfo("Sucesso", "Cliente inserido com sucesso!")
            inserir_cliente_window.destroy()

        button_inserir = tk.Button(inserir_cliente_window, text="Inserir", command=inserir_cliente)
        button_inserir.pack()

    def janela_alterar_produto(self):
        alterar_produto_window = tk.Toplevel(self.master)
        alterar_produto_window.title("Alterar Produto")

        label_codigo = tk.Label(alterar_produto_window, text="Código do Produto:")
        label_codigo.pack()
        entry_codigo = tk.Entry(alterar_produto_window)
        entry_codigo.pack()

        label_nome = tk.Label(alterar_produto_window, text="Novo Nome:")
        label_nome.pack()
        entry_nome = tk.Entry(alterar_produto_window)
        entry_nome.pack()

        label_quantidade = tk.Label(alterar_produto_window, text="Nova Quantidade:")
        label_quantidade.pack()
        entry_quantidade = tk.Entry(alterar_produto_window)
        entry_quantidade.pack()

        label_preco = tk.Label(alterar_produto_window, text="Novo Preço:")
        label_preco.pack()
        entry_preco = tk.Entry(alterar_produto_window)
        entry_preco.pack()

        def alterar_produto():
            codigo = int(entry_codigo.get())
            nome = entry_nome.get()
            quantidade = int(entry_quantidade.get())
            preco = float(entry_preco.get())
            novo_produto = Produto(nome, quantidade, preco)
            self.operacoes_crud.alterar_estoque(codigo, novo_produto)
            messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
            alterar_produto_window.destroy()

        button_alterar = tk.Button(alterar_produto_window, text="Alterar", command=alterar_produto)
        button_alterar.pack()

    def janela_alterar_cliente(self):
        alterar_cliente_window = tk.Toplevel(self.master)
        alterar_cliente_window.title("Alterar Cliente")

        label_codigo = tk.Label(alterar_cliente_window, text="Código do Cliente:")
        label_codigo.pack()
        entry_codigo = tk.Entry(alterar_cliente_window)
        entry_codigo.pack()

        label_nome = tk.Label(alterar_cliente_window, text="Novo Nome:")
        label_nome.pack()
        entry_nome = tk.Entry(alterar_cliente_window)
        entry_nome.pack()

        label_telefone = tk.Label(alterar_cliente_window, text="Novo Telefone:")
        label_telefone.pack()
        entry_telefone = tk.Entry(alterar_cliente_window)
        entry_telefone.pack()

        label_endereco = tk.Label(alterar_cliente_window, text="Novo Endereço:")
        label_endereco.pack()
        entry_endereco = tk.Entry(alterar_cliente_window)
        entry_endereco.pack()

        def alterar_cliente():
            codigo = int(entry_codigo.get())
            nome = entry_nome.get()
            telefone = entry_telefone.get()
            endereco = entry_endereco.get()
            novo_cliente = Cliente(nome, telefone, endereco)
            self.operacoes_crud.alterar_cliente(codigo, novo_cliente)
            messagebox.showinfo("Sucesso", "Cliente alterado com sucesso!")
            alterar_cliente_window.destroy()

        button_alterar = tk.Button(alterar_cliente_window, text="Alterar", command=alterar_cliente)
        button_alterar.pack()

    def janela_remover_produto(self):
        remover_produto_window = tk.Toplevel(self.master)
        remover_produto_window.title("Remover Produto")

        label_codigo = tk.Label(remover_produto_window, text="Código do Produto:")
        label_codigo.pack()
        entry_codigo = tk.Entry(remover_produto_window)
        entry_codigo.pack()

        def remover_produto():
            codigo = int(entry_codigo.get())
            self.operacoes_crud.remover_estoque(codigo)
            messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
            remover_produto_window.destroy()

        button_remover = tk.Button(remover_produto_window, text="Remover", command=remover_produto)
        button_remover.pack()

    def janela_remover_cliente(self):
        remover_cliente_window = tk.Toplevel(self.master)
        remover_cliente_window.title("Remover Cliente")

        label_codigo = tk.Label(remover_cliente_window, text="Código do Cliente:")
        label_codigo.pack()
        entry_codigo = tk.Entry(remover_cliente_window)
        entry_codigo.pack()

        def remover_cliente():
            codigo = int(entry_codigo.get())
            self.operacoes_crud.remover_cliente(codigo)
            messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")
            remover_cliente_window.destroy()

        button_remover = tk.Button(remover_cliente_window, text="Remover", command=remover_cliente)
        button_remover.pack()

    def janela_pesquisar(self):
        pesquisar_window = tk.Toplevel(self.master)
        pesquisar_window.title("Pesquisar")

        label_nome = tk.Label(pesquisar_window, text="Nome:")
        label_nome.pack()
        entry_nome = tk.Entry(pesquisar_window)
        entry_nome.pack()

        def pesquisar():
            nome = entry_nome.get()
            resultados = self.operacoes_crud.pesquisar_por_nome(nome)
            if resultados:
                resultado_str = ""
                for resultado in resultados:
                    if isinstance(resultado, Produto):
                        resultado_str += f"Produto - Nome: {resultado.nome}, Quantidade: {resultado.quantidade}, Preço: {resultado.preco}\n"
                    elif isinstance(resultado, Cliente):
                        resultado_str += f"Cliente - Nome: {resultado.nome}, Telefone: {resultado.telefone}, Endereço: {resultado.endereco}\n"
                messagebox.showinfo("Resultados", resultado_str)
            else:
                messagebox.showinfo("Resultados", "Nenhum resultado encontrado.")
            pesquisar_window.destroy()

        button_pesquisar = tk.Button(pesquisar_window, text="Pesquisar", command=pesquisar)
        button_pesquisar.pack()

root = tk.Tk()
app = Application(root)
root.mainloop()
