import sqlite3
import tkinter as tk
from tkinter import messagebox

class OperacoesEstoque:
    def __init__(self):
        self.conn = sqlite3.connect('mercado.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS estoque (
                            codigo INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            quantidade INTEGER,
                            preco REAL
                            )''')
        self.conn.commit()

        self.c.execute('''CREATE VIEW IF NOT EXISTS itens_disponiveis AS
                            SELECT * FROM estoque WHERE quantidade > 0''')
        self.conn.commit()

    def inserir_produto(self, produto):
        self.c.execute('''INSERT INTO estoque (nome, quantidade, preco) 
                          VALUES (?, ?, ?)''', (produto.nome, produto.quantidade, produto.preco))
        self.conn.commit()

    def alterar_produto(self, codigo, novo_produto):
        self.c.execute('''UPDATE estoque SET nome=?, quantidade=?, preco=? WHERE codigo=?''',
                       (novo_produto.nome, novo_produto.quantidade, novo_produto.preco, codigo))
        rows_affected = self.c.execute("SELECT changes()").fetchone()[0]
        self.conn.commit()
        return rows_affected

    def pesquisar_produto_por_nome(self, nome_produto):
        resultados = []
        for col in self.c.execute('''SELECT * FROM estoque WHERE nome LIKE ?''', ('%' + nome_produto + '%',)):
            resultados.append((col[0], col[1], col[2], col[3]))
        return resultados

    def remover_produto(self, codigo):
        self.c.execute('''DELETE FROM estoque WHERE codigo=?''', (codigo,))
        rows_deleted = self.c.execute("SELECT changes()").fetchone()[0]
        self.conn.commit()
        return rows_deleted

    def mostrar_todos_itens_estoque(self):
        self.c.execute("SELECT * FROM estoque")
        estoque = self.c.fetchall()
        return estoque

class Produto:
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

class ApplicationEstoque:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gerenciamento de Estoque")
        self.operacoes_estoque = OperacoesEstoque()
        self.label = tk.Label(master, text="Escolha uma operação:")
        self.label.pack()

        self.inserir_produto_button = tk.Button(master, text="Inserir Produto", command=self.janela_inserir_produto)
        self.inserir_produto_button.pack(pady=5)

        self.alterar_produto_button = tk.Button(master, text="Alterar Produto", command=self.janela_alterar_produto)
        self.alterar_produto_button.pack(pady=5)

        self.pesquisar_produto_button = tk.Button(master, text="Pesquisar Produto", command=self.janela_pesquisar_produto)
        self.pesquisar_produto_button.pack(pady=5)

        self.pesquisar_produto_button = tk.Button(master, text="Remover Produto", command=self.janela_remover_produto)
        self.pesquisar_produto_button.pack(pady=5)

        self.mostrar_estoque_button = tk.Button(master, text="Mostrar Estoque", command=self.mostrar_estoque)
        self.mostrar_estoque_button.pack(pady=5)

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
            self.operacoes_estoque.inserir_produto(produto)
            messagebox.showinfo("Sucesso", "Produto inserido com sucesso!")
            inserir_produto_window.destroy()

        button_inserir = tk.Button(inserir_produto_window, text="Inserir", command=inserir_produto)
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
            rows_affected = self.operacoes_estoque.alterar_produto(codigo, novo_produto)
            if rows_affected == 0:
                messagebox.showinfo("ERRO", "Produto não encontrado.")
                return
            messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
            alterar_produto_window.destroy()

        button_alterar = tk.Button(alterar_produto_window, text="Alterar", command=alterar_produto)
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
        resultados_pesquisa = self.operacoes_estoque.pesquisar_produto_por_nome(nome_produto)

        if resultados_pesquisa:
            resultado_str = "Resultados da pesquisa:\n"
            for resultado in resultados_pesquisa:
                codigo, nome, quantidade, preco = resultado
                resultado_str += f"Código: {codigo}\nNome: {nome}\nQuantidade: {quantidade}\nPreço: {preco}\n"
            messagebox.showinfo("Resultados", resultado_str)
        else:
            messagebox.showinfo("ERRO", "Nenhum produto encontrado com esse nome.")

    def janela_remover_produto(self):
        remover_produto_window = tk.Toplevel(self.master)
        remover_produto_window.title("Remover produto")

        label_codigo = tk.Label(remover_produto_window, text="Código do produto:")
        label_codigo.pack()
        entry_codigo = tk.Entry(remover_produto_window)
        entry_codigo.pack()

        def remover_produto():
            codigo = int(entry_codigo.get())
            changes = self.operacoes_estoque.remover_produto(codigo)
            if changes == 0:
                messagebox.showinfo("Erro", "Produto não encontrado.")
            else: 
                messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
            remover_produto_window.destroy()

        button_remover = tk.Button(remover_produto_window, text="Remover", command=remover_produto)
        button_remover.pack()

    def mostrar_estoque(self):
        estoque = self.operacoes_estoque.mostrar_todos_itens_estoque()
        if estoque:
            resultado_str = "Código | Nome | Quantidade | Preço\n"
            for produto in estoque:
                resultado_str += " | ".join(str(item) for item in produto) + "\n"
            messagebox.showinfo("Estoque", resultado_str)
        else:
            messagebox.showinfo("ERRO", "O estoque está vazio.")

root = tk.Tk()
app_estoque = ApplicationEstoque(root)
root.mainloop()
