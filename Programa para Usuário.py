import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class ApplicationSelecaoProdutos:
    def __init__(self, master):
        self.master = master
        self.itens_carrinho = {}
        
        self.frame_selecao = tk.Frame(master)
        self.frame_selecao.pack(padx=10, pady=10)
        
        self.label_produto = tk.Label(self.frame_selecao, text="Selecione o produto:")
        self.label_produto.pack()
        
        self.combobox_produtos = ttk.Combobox(self.frame_selecao, width=30)
        self.combobox_produtos.pack()
        
        self.label_quantidade = tk.Label(self.frame_selecao, text="Selecione a quantidade:")
        self.label_quantidade.pack()
        
        self.entry_quantidade = tk.Entry(self.frame_selecao)
        self.entry_quantidade.pack(side=tk.LEFT)
        
        self.button_incrementar = tk.Button(self.frame_selecao, text="+", width=2, command=self.incrementar_quantidade)
        self.button_incrementar.pack(side=tk.LEFT)
        
        self.button_decrementar = tk.Button(self.frame_selecao, text="-", width=2, command=self.decrementar_quantidade)
        self.button_decrementar.pack(side=tk.LEFT)
        
        self.button_adicionar = tk.Button(self.frame_selecao, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho)
        self.button_adicionar.pack()
        
        self.button_mostrar_carrinho = tk.Button(self.master, text="Mostrar Carrinho", command=self.mostrar_carrinho)
        self.button_mostrar_carrinho.pack()
        
        self.treeview_produtos = ttk.Treeview(self.master, columns=("Nome", "Preço"))
        self.treeview_produtos.heading("#0", text="ID")
        self.treeview_produtos.heading("#1", text="Nome")
        self.treeview_produtos.heading("#2", text="Preço")
        self.treeview_produtos.pack(padx=10, pady=10)
        
        self.conn = sqlite3.connect('mercado.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM itens_disponiveis")
        disponiveis = self.c.fetchall()
                
        self.combobox_produtos['values'] = [f"{item[1]}" for item in disponiveis]  
        
        for produto in disponiveis:
            self.treeview_produtos.insert("", tk.END, text=produto[0], values=(produto[1], f"R${produto[3]:.2f}"))

    def incrementar_quantidade(self):
        quantidade_atual = int(self.entry_quantidade.get())
        self.entry_quantidade.delete(0, tk.END)
        self.entry_quantidade.insert(0, str(quantidade_atual + 1))
    
    def decrementar_quantidade(self):
        quantidade_atual = int(self.entry_quantidade.get())
        if quantidade_atual > 1:
            self.entry_quantidade.delete(0, tk.END)
            self.entry_quantidade.insert(0, str(quantidade_atual - 1))

    
    def adicionar_ao_carrinho(self):
        produto_selecionado = self.combobox_produtos.get().split(" - ")[0]
        quantidade = int(self.entry_quantidade.get())
        
        self.c.execute("SELECT preco FROM itens_disponiveis WHERE nome=?", (produto_selecionado,))
        preco_unitario = self.c.fetchone()[0]
        
        if produto_selecionado in self.itens_carrinho:
            
            self.itens_carrinho[produto_selecionado]["quantidade"] += quantidade
        else:
            self.itens_carrinho[produto_selecionado] = {"quantidade": quantidade, "preco_unitario": preco_unitario}
        
        print(f"Produto: {produto_selecionado}, Quantidade: {quantidade} - Adicionado ao carrinho")
    
    def mostrar_carrinho(self):
        if self.itens_carrinho:
            self.carrinho_window = tk.Toplevel(self.master)
            self.carrinho_window.title("Carrinho de Compras")
            carrinho = CarrinhoCompra(self.carrinho_window, self.itens_carrinho)
        else:
            messagebox.showinfo("ERRO", "O carrinho está vazio.")

class CarrinhoCompra:
    def __init__(self, master, itens_carrinho):
        self.master = master
        self.itens_carrinho = itens_carrinho
        
        self.frame_carrinho = tk.Frame(master)
        self.frame_carrinho.pack(padx=10, pady=10)
        
        self.label_carrinho = tk.Label(self.frame_carrinho, text="Itens no Carrinho:")
        self.label_carrinho.pack()
        
        self.treeview_carrinho = ttk.Treeview(self.frame_carrinho, columns=("Quantidade", "Preço Unitário", "Valor Parcial"))
        self.treeview_carrinho.heading("#0", text="Produto")
        self.treeview_carrinho.heading("#1", text="Quantidade")
        self.treeview_carrinho.heading("#2", text="Preço Unitário")
        self.treeview_carrinho.heading("#3", text="Valor Parcial")
        self.treeview_carrinho.pack()
        
        for produto, info in self.itens_carrinho.items():
            preco_unitario = info["preco_unitario"]
            quantidade = info["quantidade"]
            parcial = info["preco_unitario"] * info["quantidade"]
            self.treeview_carrinho.insert("", tk.END, text=produto, values=(quantidade, f"R${preco_unitario:.2f}", f"R${parcial:.2f}"))
        
        self.button_identificar_cliente = tk.Button(master, text="Identificar Cliente", command=self.identificar_cliente)
        self.button_identificar_cliente.pack(pady=10)

        self.button_identificar_cliente = tk.Button(master, text="Finalizar Pedido", command=self.finalizar_compra)
        self.button_identificar_cliente.pack(pady=10)
    
    def identificar_cliente(self):
        messagebox.showinfo("ERRO", "TA PRONTO NÃO.")
    
    def finalizar_compra(self):
        conn = sqlite3.connect('mercado.db')
        c = conn.cursor()

        codigo_pedido = c.lastrowid
        c.execute("INSERT INTO pedidos (codigo, codigo_cliente, data) VALUES (?, ?, CURRENT_DATE)", (codigo_pedido, 123,))  # Substitua 123 pelo código do cliente
            
        for produto, info in self.itens_carrinho.items():
            quantidade = info["quantidade"]
            parcial = info["preco_unitario"] * info["quantidade"]
            c.execute("INSERT INTO itens_pedido (codigo_pedido, codigo_pedido, produto, parcial) VALUES (?, ?, ?, ?)",
          (codigo_pedido, codigo_pedido, produto, parcial))
            
        conn.commit()

root = tk.Tk()
app = ApplicationSelecaoProdutos(root)
root.mainloop()
