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

    def pesquisar_produto_por_nome(self, nome_produto):
        resultados = []
        for col in self.c.execute('''SELECT * FROM estoque WHERE nome LIKE ?''', ('%' + nome_produto + '%',)):
            resultados.append((col[0], col[1], col[2], col[3]))
        return resultados
    
    def pesquisar_cliente_por_nome(self, nome_cliente):
        resultados = []
        for col in self.c.execute('''SELECT * FROM clientes WHERE nome LIKE ?''', ('%' + nome_cliente + '%',)):
            resultados.append((col[0], col[1], col[2], col[3]))
        return resultados

    def remover_estoque(self, codigo):
        self.c.execute('''DELETE FROM estoque WHERE codigo=?''', (codigo,))
        self.conn.commit()

    def remover_cliente(self, codigo):
        self.c.execute('''DELETE FROM clientes WHERE codigo=?''', (codigo,))
        self.conn.commit()

    def mostrar_todos_itens_estoque(self):
        self.c.execute("SELECT * FROM estoque")
        estoque = self.c.fetchall()
        return estoque

    def listar_todos_clientes(self):
        self.c.execute("SELECT * FROM clientes")
        clientes = self.c.fetchall()
        return clientes
    

    def quantidade_produtos_inseridos(self):
        try:
            quantidade = self.c.execute("SELECT COUNT(*) FROM estoque").fetchone()[0]
            return quantidade
        except sqlite3.OperationalError:
            return 0

    def quantidade_clientes_inseridos(self):
        try:
            quantidade = self.c.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
            return quantidade
        except sqlite3.OperationalError:
            return 0

    def soma_total_valores_produtos(self):
        try:
            self.c.execute("SELECT SUM(preco) FROM estoque")
            total_valores = self.c.fetchone()[0] or 0  # P lidar c valores nulos
            return total_valores
        except sqlite3.OperationalError:
            return 0

    def soma_total_quantidades_produtos(self):
        try:
            self.c.execute("SELECT SUM(quantidade) FROM estoque")
            total_quantidades = self.c.fetchone()[0] or 0  # P lidar c valores nulos
            return total_quantidades
        except sqlite3.OperationalError:
            return 0

    def relatorio_sistema(self):
        
        quantidade_produtos = self.quantidade_produtos_inseridos()

        quantidade_clientes = self.quantidade_clientes_inseridos()

        total_valores_produtos = self.soma_total_valores_produtos()
        
        total_quantidades_produtos = self.soma_total_quantidades_produtos()

        # Criar o texto do relatório
        relatorio_text = f"Quantidade de produtos inseridos: {quantidade_produtos}\n"
        relatorio_text += f"Quantidade de clientes inseridos: {quantidade_clientes}\n"
        relatorio_text += f"Preço total dos produtos: {total_valores_produtos}\n"
        relatorio_text += f"Quantidade total dos produtos: {total_quantidades_produtos}\n"

        return relatorio_text

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

        #Produtos
        self.produtos_frame = tk.Frame(master)
        self.produtos_frame.pack(side=tk.LEFT, padx=10)

        self.produtos_label = tk.Label(self.produtos_frame, text="Produtos:")
        self.produtos_label.pack()

        self.inserir_produto_button = tk.Button(self.produtos_frame, text="Inserir Produto", command=self.janela_inserir_produto)
        self.inserir_produto_button.pack(pady=5)

        self.alterar_produto_button = tk.Button(self.produtos_frame, text="Alterar Produto", command=self.janela_alterar_produto)
        self.alterar_produto_button.pack(pady=5)

        self.pesquisar_produto_button = tk.Button(self.produtos_frame, text="Pesquisar Produto", command=self.janela_pesquisar_produto)
        self.pesquisar_produto_button.pack(pady=5)

        self.remover_produto_button = tk.Button(self.produtos_frame, text="Remover Produto", command=self.janela_remover_produto)
        self.remover_produto_button.pack(pady=5)

        self.mostrar_estoque_button = tk.Button(self.produtos_frame, text="Mostrar Estoque", command=self.mostrar_estoque)
        self.mostrar_estoque_button.pack(pady=5)

        #Clientes
        self.clientes_frame = tk.Frame(master)
        self.clientes_frame.pack(side=tk.RIGHT, padx=10)

        self.clientes_label = tk.Label(self.clientes_frame, text="Clientes:")
        self.clientes_label.pack()

        self.inserir_cliente_button = tk.Button(self.clientes_frame, text="Inserir Cliente", command=self.janela_inserir_cliente)
        self.inserir_cliente_button.pack(pady=5)

        self.alterar_cliente_button = tk.Button(self.clientes_frame, text="Alterar Cliente", command=self.janela_alterar_cliente)
        self.alterar_cliente_button.pack(pady=5)

        self.pesquisar_cliente_button = tk.Button(self.clientes_frame, text="Pesquisar Cliente", command=self.janela_pesquisar_cliente)
        self.pesquisar_cliente_button.pack(pady=5)

        self.remover_cliente_button = tk.Button(self.clientes_frame, text="Remover Cliente", command=self.janela_remover_cliente)
        self.remover_cliente_button.pack(pady=5)

        self.mostrar_clientes_button = tk.Button(self.clientes_frame, text="Mostrar Clientes", command=self.mostrar_clientes)
        self.mostrar_clientes_button.pack(pady=5)

        #Relatório
        self.relatorio_button = tk.Button(master, text="Relatório do Sistema", command=self.janela_relatorio)
        self.relatorio_button.pack(pady=10)

    def janela_inserir_produto(self):
        inserir_produto_window = tk.Toplevel(self.master)
        inserir_produto_window.title("Inserir produto")

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
        inserir_cliente_window.title("Inserir cliente")

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
        alterar_produto_window.title("Alterar produto")

        label_codigo = tk.Label(alterar_produto_window, text="Código do produto:")
        label_codigo.pack()
        entry_codigo = tk.Entry(alterar_produto_window)
        entry_codigo.pack()

        label_nome = tk.Label(alterar_produto_window, text="Novo nome:")
        label_nome.pack()
        entry_nome = tk.Entry(alterar_produto_window)
        entry_nome.pack()

        label_quantidade = tk.Label(alterar_produto_window, text="Nova quantidade:")
        label_quantidade.pack()
        entry_quantidade = tk.Entry(alterar_produto_window)
        entry_quantidade.pack()

        label_preco = tk.Label(alterar_produto_window, text="Novo preço:")
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
        alterar_cliente_window.title("Alterar cliente")

        label_codigo = tk.Label(alterar_cliente_window, text="Código do cliente:")
        label_codigo.pack()
        entry_codigo = tk.Entry(alterar_cliente_window)
        entry_codigo.pack()

        label_nome = tk.Label(alterar_cliente_window, text="Novo nome:")
        label_nome.pack()
        entry_nome = tk.Entry(alterar_cliente_window)
        entry_nome.pack()

        label_telefone = tk.Label(alterar_cliente_window, text="Novo telefone:")
        label_telefone.pack()
        entry_telefone = tk.Entry(alterar_cliente_window)
        entry_telefone.pack()

        label_endereco = tk.Label(alterar_cliente_window, text="Novo endereço:")
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

    def janela_pesquisar_produto(self):
        pesquisar_produto_window = tk.Toplevel(self.master)
        pesquisar_produto_window.title("Pesquisar produto")

        label_pesquisar = tk.Label(pesquisar_produto_window, text="Digite o nome do produto:")
        label_pesquisar.pack()

        entry_pesquisar = tk.Entry(pesquisar_produto_window)
        entry_pesquisar.pack()

        button_pesquisar = tk.Button(pesquisar_produto_window, text="Pesquisar", command=lambda: self.pesquisar_produto(entry_pesquisar.get()))
        button_pesquisar.pack()

    def pesquisar_produto(self, nome_produto):
        resultados_pesquisa = self.operacoes_crud.pesquisar_produto_por_nome(nome_produto)

        if resultados_pesquisa:
            resultado_str = "Resultados da pesquisa:\n"
            for resultado in resultados_pesquisa:
                codigo, nome, quantidade, preco = resultado
                resultado_str += f"Código: {codigo}\nNome: {nome}\nQuantidade: {quantidade}\nPreço: {preco}\n"
            messagebox.showinfo("Resultados", resultado_str)
        else:
            messagebox.showinfo("Resultados", "Nenhum produto encontrado com esse nome.")

    def janela_pesquisar_cliente(self):
        pesquisar_cliente_window = tk.Toplevel(self.master)
        pesquisar_cliente_window.title("Pesquisar cliente")

        label_pesquisar = tk.Label(pesquisar_cliente_window, text="Digite o nome do cliente:")
        label_pesquisar.pack()

        entry_pesquisar = tk.Entry(pesquisar_cliente_window)
        entry_pesquisar.pack()

        button_pesquisar = tk.Button(pesquisar_cliente_window, text="Pesquisar", command=lambda: self.pesquisar_cliente(entry_pesquisar.get()))
        button_pesquisar.pack()

    def pesquisar_cliente(self, nome_cliente):
        resultados_pesquisa = self.operacoes_crud.pesquisar_cliente_por_nome(nome_cliente)

        if resultados_pesquisa:
            resultado_str = "Resultados da pesquisa:\n"
            for resultado in resultados_pesquisa:
                codigo, nome, telefone, endereco = resultado
                resultado_str += f"Código: {codigo}\nNome: {nome}\nTelefone: {telefone}\nEndereço: {endereco}\n"
            messagebox.showinfo("Resultados", resultado_str)
        else:
            messagebox.showinfo("Resultados", "Nenhum cliente encontrado com esse nome.")

    def janela_remover_produto(self):
        remover_produto_window = tk.Toplevel(self.master)
        remover_produto_window.title("Remover produto")

        label_codigo = tk.Label(remover_produto_window, text="Código do produto:")
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
        remover_cliente_window.title("Remover cliente")

        label_codigo = tk.Label(remover_cliente_window, text="Código do cliente:")
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

    def mostrar_estoque(self):
        resultados = self.operacoes_crud.mostrar_todos_itens_estoque()
        
        if resultados:
            resultado_str = "Código | Nome | Quantidade | Preço\n"
            for resultado in resultados:
                resultado_str += " | ".join(str(item) for item in resultado) + "\n"
            messagebox.showinfo("Estoque", resultado_str)
        else:
            messagebox.showinfo("Estoque", "O estoque está vazio.")
            
    def mostrar_clientes(self):
        resultados = self.operacoes_crud.listar_todos_clientes()

        if resultados:
            resultado_str = "Código | Nome | Telefone | Endereço\n"
            for resultado in resultados:
                resultado_str += " | ".join(str(item) for item in resultado) + "\n"
            messagebox.showinfo("Clientes", resultado_str)
        else:
            messagebox.showinfo("Clientes", "Nenhum cliente encontrado.")

    def janela_relatorio(self):
        relatorio_window = tk.Toplevel(self.master)
        relatorio_window.title("Relatório do sistema")

        relatorio_text = self.operacoes_crud.relatorio_sistema()

        label_relatorio = tk.Label(relatorio_window, text=relatorio_text)
        label_relatorio.pack(padx=10, pady=10)

            
root = tk.Tk()
app = Application(root)
root.mainloop()
