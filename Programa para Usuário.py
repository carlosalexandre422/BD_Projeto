import sqlite3
import tkinter as tk
from tkinter import ttk

class ApplicationselectProdutos:
    def __init__(self, master):
        self.master = master
        self.master.title("Seleção de Produtos")
        
        self.frame_disponiveis = tk.Frame(master)
        self.frame_disponiveis.pack(padx=10, pady=10)
        
        self.label_disponiveis = tk.Label(self.frame_disponiveis, text="Itens Disponíveis:")
        self.label_disponiveis.pack()
        
        self.lista_disponiveis = tk.Listbox(self.frame_disponiveis, width=50)
        self.lista_disponiveis.pack()
        
        self.conn = sqlite3.connect('mercado.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM itens_disponiveis")
        disponiveis = self.c.fetchall()
        for item in disponiveis:
            self.lista_disponiveis.insert(tk.END, f"{item[1]}: {item[2]} disponíveis - Preço: R${item[3]}")
        
        self.frame_select = tk.Frame(master)
        self.frame_select.pack(padx=10, pady=10)
        
        self.label_produto = tk.Label(self.frame_select, text="Selecione o produto:")
        self.label_produto.pack()
        
        self.combobox_produtos = ttk.Combobox(self.frame_select)
        self.combobox_produtos['values'] = [item[1] for item in disponiveis]  # Preenche a ComboBox com os nomes dos produtos disponíveis
        self.combobox_produtos.pack()
        
        self.label_quantidade = tk.Label(self.frame_select, text="Selecione a quantidade:")
        self.label_quantidade.pack()
        
        self.entry_quantidade = tk.Entry(self.frame_select)
        self.entry_quantidade.pack()
        
        self.button_adicionar = tk.Button(self.frame_select, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho)
        self.button_adicionar.pack()
        
        self.button_mostrar_carrinho = tk.Button(self.master, text="Mostrar Carrinho", command=self.mostrar_carrinho)
        self.button_mostrar_carrinho.pack(pady=10)
        
        self.itens_carrinho = []
    
    def adicionar_ao_carrinho(self):
        produto_selecionado = self.combobox_produtos.get()
        quantidade = int(self.entry_quantidade.get())
        
        for i, (produto, j) in enumerate(self.itens_carrinho): #j é a quantidade ja no carrinho
            if produto == produto_selecionado:
                self.itens_carrinho[i] = (produto, j + quantidade)
                break
        else:
            self.itens_carrinho.append((produto_selecionado, quantidade))
        
        print(f"Produto: {produto_selecionado}, Quantidade: {quantidade} - Adicionado ao carrinho")

    def mostrar_carrinho(self):
        if self.itens_carrinho:
            self.carrinho_window = tk.Toplevel(self.master)
            self.carrinho_window.title("Carrinho de Compras")

            tree = ttk.Treeview(self.carrinho_window, columns=("Produto", "Quantidade", "Preço"))

            tree.heading("#0", text="Produto")
            tree.heading("#1", text="Quantidade")
            tree.heading("#2", text="Preço")

            for i, (produto, quantidade) in enumerate(self.itens_carrinho):
                preco_produto = 10
                tree.insert("", i, text=produto, values=(quantidade, preco_produto))

            tree.pack(expand=True, fill="both")
        else:
            print("O carrinho está vazio.")
#######################################################AJEITAR O PREÇO

root = tk.Tk()
app = ApplicationselectProdutos(root)
root.mainloop()
