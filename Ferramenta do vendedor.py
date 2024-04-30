import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class OperacoesClientes:
    def __init__(self):
        self.conn = sqlite3.connect('mercado.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                            codigo INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            telefone TEXT,
                            endereco TEXT
                            )''')
        self.conn.commit()

    def inserir_cliente(self, cliente):
        self.c.execute('''INSERT INTO clientes (nome, telefone, endereco) 
                          VALUES (?, ?, ?)''', (cliente.nome, cliente.telefone, cliente.endereco))
        self.conn.commit()

    def alterar_cliente(self, codigo, telefone, endereco):
        try:
            self.c.execute('''UPDATE clientes SET telefone=?, endereco=? WHERE codigo=?''',
                        (telefone, endereco, codigo))
            rows_affected = self.c.rowcount
            self.conn.commit()
            return rows_affected
        except sqlite3.Error as e:
            print("Erro ao alterar cliente:", e)
            return 0

    def pesquisar_cliente(self, nome_cliente):
        resultados = []
        for col in self.c.execute('''SELECT * FROM clientes WHERE nome LIKE ?''', ('%' + nome_cliente + '%',)):
            resultados.append((col[0], col[1], col[2], col[3]))
        return resultados

    def listar_clientes(self):
        self.c.execute("SELECT * FROM clientes")
        clientes = self.c.fetchall()
        return clientes

class OperacoesPedidos:
    def __init__(self):
        self.conn = sqlite3.connect('mercado.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                            codigo INTEGER PRIMARY KEY,
                            codigo_cliente INTEGER,
                            nome_vendedor TEXT,
                            data DATE
                            )''')
        self.conn.commit()

    def criar_pedido(self, codigo_cliente, nome_vendedor, data):
        self.c.execute('''INSERT INTO pedidos (codigo_cliente, nome_vendedor, data) VALUES (?, ?, ?)''', (codigo_cliente, nome_vendedor, data))
        codigo_pedido = self.c.lastrowid
        self.conn.commit()
        return codigo_pedido

    def listar_pedidos(self):
        self.c.execute("SELECT * FROM pedidos")
        pedidos = self.c.fetchall()
        return pedidos

    def buscar_pedido_por_codigo(self, codigo):
        self.c.execute("SELECT * FROM pedidos WHERE codigo=?", (codigo,))
        pedido = self.c.fetchone()
        return pedido

    def alterar_pedido(self, codigo, novo_codigo_cliente, novo_nome_vendedor, nova_data):
        self.c.execute('''UPDATE pedidos SET codigo_cliente=?, nome_vendedor=?, data=? WHERE codigo=?''',
                       (novo_codigo_cliente, novo_nome_vendedor, nova_data, codigo))
        rows_affected = self.c.execute("SELECT changes()").fetchone()[0]
        self.conn.commit()
        return rows_affected
        
class OperacoesItensPedido:
    def __init__(self):
        self.conn = sqlite3.connect('mercado.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS itens_pedido (
                            codigo INTEGER PRIMARY KEY,
                            codigo_pedido INTEGER,
                            codigo_produto INTEGER,
                            quantidade INTEGER,
                            FOREIGN KEY (codigo_pedido) REFERENCES pedidos(codigo)
                            )''')
        self.conn.commit()

class Cliente:
    def __init__(self, nome, telefone, endereco):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco

class Pedido:
    def __init__(self, codigo_cliente, data):
        self.codigo_cliente = codigo_cliente
        self.data = data

class ItemPedido:
    def __init__(self, codigo_pedido, codigo_produto, quantidade):
        self.codigo_pedido = codigo_pedido
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade

class ApplicationClientes:
    def __init__(self, master):
        self.master = master
        self.operacoes_clientes = OperacoesClientes()
        self.label = tk.Label(master, text="Escolha uma operação:")
        self.label.pack()

        self.inserir_cliente_button = tk.Button(master, text="Inserir Cliente", command=self.janela_inserir_cliente)
        self.inserir_cliente_button.pack(pady=5)

        self.alterar_cliente_button = tk.Button(master, text="Alterar Cliente", command=self.janela_alterar_cliente)
        self.alterar_cliente_button.pack(pady=5)

        self.pesquisar_cliente_button = tk.Button(master, text="Pesquisar Cliente", command=self.janela_pesquisar_cliente)
        self.pesquisar_cliente_button.pack(pady=5)

        self.mostrar_clientes_button = tk.Button(master, text="Mostrar Clientes", command=self.listar_clientes)
        self.mostrar_clientes_button.pack(pady=5)

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
            self.operacoes_clientes.inserir_cliente(nome, telefone, endereco)
            messagebox.showinfo("Sucesso", "Cliente inserido com sucesso!")
            inserir_cliente_window.destroy()

        button_inserir_cliente = tk.Button(inserir_cliente_window, text="Inserir Cliente", command=inserir_cliente)
        button_inserir_cliente.pack()

    def listar_clientes(self):
        clientes = self.operacoes_clientes.listar_clientes()
        if clientes:
            resultado_str = "Código | Nome | Telefone | Endereço\n"
            for cliente in clientes:
                resultado_str += " | ".join(str(item) for item in cliente) + "\n"
            messagebox.showinfo("Lista de Clientes", resultado_str)
        else:
            messagebox.showinfo("Lista de Clientes", "Nenhum cliente encontrado.")

    def janela_alterar_cliente(self):
        alterar_cliente_window = tk.Toplevel(self.master)
        alterar_cliente_window.title("Alterar Cliente")

        label_codigo = tk.Label(alterar_cliente_window, text="Código do cliente:")
        label_codigo.pack()
        entry_codigo = tk.Entry(alterar_cliente_window)
        entry_codigo.pack()

        label_telefone = tk.Label(alterar_cliente_window, text="Novo Telefone:")
        label_telefone.pack()
        entry_telefone = tk.Entry(alterar_cliente_window)
        entry_telefone.pack()

        label_endereco = tk.Label(alterar_cliente_window, text="Novo Endereço:")
        label_endereco.pack()
        entry_endereco = tk.Entry(alterar_cliente_window)
        entry_endereco.pack()

        def alterar_cliente():
            codigo = entry_codigo.get()
            telefone = entry_telefone.get()
            endereco = entry_endereco.get()
            if not codigo:
                messagebox.showerror("Erro", "Por favor, insira o código do cliente.")
                return
            self.operacoes_clientes.alterar_cliente(codigo, telefone, endereco)
            messagebox.showinfo("Sucesso", "Cliente alterado com sucesso!")
            alterar_cliente_window.destroy()

        button_alterar_cliente = tk.Button(alterar_cliente_window, text="Alterar Cliente", command=alterar_cliente)
        button_alterar_cliente.pack()

    def janela_pesquisar_cliente(self):
        pesquisar_cliente_window = tk.Toplevel(self.master)
        pesquisar_cliente_window.title("Pesquisar Cliente")

        label_nome = tk.Label(pesquisar_cliente_window, text="Nome do cliente:")
        label_nome.pack()
        entry_nome = tk.Entry(pesquisar_cliente_window)
        entry_nome.pack()

        def pesquisar_cliente():
            nome = entry_nome.get()
            clientes = self.operacoes_clientes.pesquisar_cliente(nome)
            if clientes:
                resultado_str = "Código | Nome | Telefone | Endereço\n"
                for cliente in clientes:
                    resultado_str += " | ".join(str(item) for item in cliente) + "\n"
                messagebox.showinfo("Resultado da Pesquisa", resultado_str)
            else:
                messagebox.showinfo("Resultado da Pesquisa", "Nenhum cliente encontrado com esse nome.")

        button_pesquisar_cliente = tk.Button(pesquisar_cliente_window, text="Pesquisar Cliente", command=pesquisar_cliente)
        button_pesquisar_cliente.pack()
        
class ApplicationPedidos:
    def __init__(self, master):
        self.master = master
        self.operacoes_pedidos = OperacoesPedidos()

        self.button_criar_pedido = tk.Button(self.master, text="Criar Pedido", command=self.janela_criar_pedido)
        self.button_criar_pedido.pack(pady=10)

        self.button_listar_pedidos = tk.Button(self.master, text="Listar Pedidos", command=self.listar_pedidos)
        self.button_listar_pedidos.pack(pady=10)

    def janela_criar_pedido(self):
        criar_pedido_window = tk.Toplevel(self.master)
        criar_pedido_window.title("Iniciar pedido")

        label_codigo_cliente = tk.Label(criar_pedido_window, text="Código do Cliente:")
        label_codigo_cliente.pack()
        entry_codigo_cliente = tk.Entry(criar_pedido_window)
        entry_codigo_cliente.pack()

        label_nome_vendedor = tk.Label(criar_pedido_window, text="Nome do Vendedor:")
        label_nome_vendedor.pack()
        entry_nome_vendedor = tk.Entry(criar_pedido_window)
        entry_nome_vendedor.pack()

        label_data = tk.Label(criar_pedido_window, text="Data:")
        label_data.pack()
        entry_data = tk.Entry(criar_pedido_window)
        entry_data.pack()
        
        def criar_pedido(self):
            codigo_cliente = int(self.entry_codigo_cliente.get())
            nome_vendedor = self.entry_nome_vendedor.get()
            data = self.entry_data.get()
            self.operacoes_pedidos.criar_pedido(codigo_cliente, nome_vendedor, data)
            messagebox.showinfo("Sucesso", "Pedido criado com sucesso!")

        button_criar_pedido = tk.Button(criar_pedido_window, text="Adicionar Itens")
        button_criar_pedido.pack()

    def listar_pedidos(self):
        pedidos = self.operacoes_pedidos.listar_pedidos()
        if pedidos:
            pedidos_str = "Lista de Pedidos:\n"
            for pedido in pedidos:
                pedidos_str += f"Código: {pedido[0]}, Código do Cliente: {pedido[1]}, Nome do Vendedor: {pedido[2]}, Data: {pedido[3]}\n"
            messagebox.showinfo("Pedidos", pedidos_str)
        else:
            messagebox.showinfo("Pedidos", "Nenhum pedido encontrado.")

def main():
    root = tk.Tk()
    root.title("Gerenciamento de Clientes e Pedidos")

    tab_control = ttk.Notebook(root)
    tab_clientes = ttk.Frame(tab_control)
    tab_pedidos = ttk.Frame(tab_control)

    tab_control.add(tab_clientes, text="Clientes")
    tab_control.add(tab_pedidos, text="Pedidos")

    tab_control.pack(expand=1, fill="both")

    app_clientes = ApplicationClientes(tab_clientes)
    app_pedidos = ApplicationPedidos(tab_pedidos)

    root.mainloop()

if __name__ == "__main__":
    main()
