import sqlite3
import tkinter as tk
from tkinter import messagebox

import OperacoesCRUD
import Produto
import Cliente

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gerenciamento do Mercado")
        self.operacoes_crud = OperacoesCRUD()

        self.label = tk.Label(master, text="Escolha uma operação:")
        self.label.pack()

        # Produtos
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

        self.realizar_compra_button = tk.Button(self.produtos_frame, text="Realizar Compra", command=self.realizar_compra)
        self.realizar_compra_button.pack(pady=5)

        # Clientes
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

        # Relatório
        self.relatorio_button = tk.Button(master, text="Relatório do Sistema", command=self.janela_relatorio)
        self.relatorio_button.pack(pady=10)
        
        # Botão para exibir informações do cliente
        self.exibir_cliente_button = tk.Button(master, text="Exibir Informações do Cliente", command=self.exibir_informacoes_cliente)
        self.exibir_cliente_button.pack(pady=10)

        self.filtrar_produtos_button = tk.Button(self.produtos_frame, text="Filtrar Produtos com Menos de 5 Unidades", command=self.janela_filtrar_produtos)
        self.filtrar_produtos_button.pack(pady=5)
        
    def janela_filtrar_produtos(self):
        filtrar_produtos_window = tk.Toplevel(self.master)
        filtrar_produtos_window.title("Filtrar Produtos com Menos de 5 Unidades")

        # Chamar a função na classe OperacoesCRUD para obter os produtos com menos de 5 unidades
        produtos_com_poucas_unidades = self.operacoes_crud.filtrar_produtos_com_poucas_unidades()

        if produtos_com_poucas_unidades:
            resultado_str = "Produtos com Menos de 5 Unidades:\n"
            for produto in produtos_com_poucas_unidades:
                codigo, nome, quantidade, preco = produto
                resultado_str += f"Código: {codigo}\nNome: {nome}\nQuantidade: {quantidade}\nPreço: {preco}\n\n"
            messagebox.showinfo("Produtos", resultado_str)
        else:
            messagebox.showinfo("Produtos", "Não há produtos com menos de 5 unidades.")

    def exibir_informacoes_cliente(self):
        # Criar a janela para inserir o código do cliente
        exibir_cliente_window = tk.Toplevel(self.master)
        exibir_cliente_window.title("Exibir Informações do Cliente")

        label_codigo = tk.Label(exibir_cliente_window, text="Digite o código do cliente:")
        label_codigo.pack()

        entry_codigo = tk.Entry(exibir_cliente_window)
        entry_codigo.pack()

        def mostrar_cliente():
            codigo_cliente = int(entry_codigo.get())
            cliente = self.operacoes_crud.obter_cliente_por_codigo(codigo_cliente)
            if cliente:
                cliente_info = f"Código: {cliente[0]}\nNome: {cliente[1]}\nTelefone: {cliente[2]}\nEndereço: {cliente[3]}"
                messagebox.showinfo("Informações do Cliente", cliente_info)
            else:
                messagebox.showinfo("Erro", "Cliente não encontrado!")

        button_mostrar_cliente = tk.Button(exibir_cliente_window, text="Mostrar Cliente", command=mostrar_cliente)
        button_mostrar_cliente.pack()

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

        label_torce_flamengo = tk.Label(inserir_cliente_window, text="Você torce para o Flamengo? (Sim/Não):")
        label_torce_flamengo.pack()
        entry_torce_flamengo = tk.Entry(inserir_cliente_window)
        entry_torce_flamengo.pack()

        label_assiste_one_piece = tk.Label(inserir_cliente_window, text="Você assiste One Piece? (Sim/Não):")
        label_assiste_one_piece.pack()
        entry_assiste_one_piece = tk.Entry(inserir_cliente_window)
        entry_assiste_one_piece.pack()

        label_de_sousa = tk.Label(inserir_cliente_window, text="Você é de Sousa? (Sim/Não):")
        label_de_sousa.pack()
        entry_de_sousa = tk.Entry(inserir_cliente_window)
        entry_de_sousa.pack()

        def inserir_cliente():
            nome = entry_nome.get()
            telefone = entry_telefone.get()
            endereco = entry_endereco.get()
            torce_flamengo = entry_torce_flamengo.get()
            assiste_one_piece = entry_assiste_one_piece.get()
            de_sousa = entry_de_sousa.get()
            cliente = Cliente(nome, telefone, endereco, torce_flamengo, assiste_one_piece, de_sousa)
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
        pesquisar_produto_window.title("Pesquisar produto de forma avançada")

        # Campos de pesquisa
        label_nome = tk.Label(pesquisar_produto_window, text="Digite o nome do produto:")
        label_nome.pack()
        entry_nome = tk.Entry(pesquisar_produto_window)
        entry_nome.pack()

        label_faixa_preco = tk.Label(pesquisar_produto_window, text="Faixa de preço:")
        label_faixa_preco.pack()
        faixa_preco_var = tk.StringVar(pesquisar_produto_window)
        faixa_preco_var.set('abaixo de 100 reais')
        dropdown_faixa_preco = tk.OptionMenu(pesquisar_produto_window, faixa_preco_var, 'abaixo de 100 reais', 'acima de 100 reais')
        dropdown_faixa_preco.pack()

        label_categoria = tk.Label(pesquisar_produto_window, text="Categoria:")
        label_categoria.pack()
        categoria_var = tk.StringVar(pesquisar_produto_window)
        categoria_var.set('alimento')
        dropdown_categoria = tk.OptionMenu(pesquisar_produto_window, categoria_var, 'alimento', 'itens diversos')
        dropdown_categoria.pack()

        label_fabricado_em_mari = tk.Label(pesquisar_produto_window, text="Fabricado em Mari:")
        label_fabricado_em_mari.pack()
        fabricado_em_mari_var = tk.StringVar(pesquisar_produto_window)
        fabricado_em_mari_var.set('sim')
        dropdown_fabricado_em_mari = tk.OptionMenu(pesquisar_produto_window, fabricado_em_mari_var, 'sim', 'não')
        dropdown_fabricado_em_mari.pack()

        def pesquisar():
            nome_produto = entry_nome.get()
            faixa_preco = faixa_preco_var.get()
            categoria = categoria_var.get()
            fabricado_em_mari = fabricado_em_mari_var.get()
            resultados = self.operacoes_crud.pesquisar_produto_por_nome(nome_produto, faixa_preco, categoria, fabricado_em_mari)
            if resultados:
                resultado_str = "Resultados da pesquisa:\n"
                for resultado in resultados:
                    codigo, nome, quantidade, preco = resultado
                    resultado_str += f"Código: {codigo}\nNome: {nome}\nQuantidade: {quantidade}\nPreço: {preco}\n\n"
                messagebox.showinfo("Resultados", resultado_str)
            else:
                messagebox.showinfo("Resultados", "Nenhum produto encontrado com esses critérios.")

        button_pesquisar = tk.Button(pesquisar_produto_window, text="Pesquisar", command=pesquisar)
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

    def janela_realizar_compra(self):
        realizar_compra_window = tk.Toplevel(self.master)
        realizar_compra_window.title("Realizar compra")

        label_codigo_produto = tk.Label(realizar_compra_window, text="Código do produto:")
        label_codigo_produto.pack()
        entry_codigo_produto = tk.Entry(realizar_compra_window)
        entry_codigo_produto.pack()

        label_quantidade = tk.Label(realizar_compra_window, text="Quantidade:")
        label_quantidade.pack()
        entry_quantidade = tk.Entry(realizar_compra_window)
        entry_quantidade.pack()

        label_codigo_cliente = tk.Label(realizar_compra_window, text="Código do cliente:")
        label_codigo_cliente.pack()
        entry_codigo_cliente = tk.Entry(realizar_compra_window)
        entry_codigo_cliente.pack()

    def realizar_compra(self):
        # Criar a janela para inserir o código do cliente
        codigo_cliente_window = tk.Toplevel(self.master)
        codigo_cliente_window.title("Inserir Código do Cliente")

        label_codigo_cliente = tk.Label(codigo_cliente_window, text="Digite o código do cliente:")
        label_codigo_cliente.pack()

        entry_codigo_cliente = tk.Entry(codigo_cliente_window)
        entry_codigo_cliente.pack()

        def iniciar_compra():
            codigo_cliente = int(entry_codigo_cliente.get())
            # Verificar se o código do cliente é válido
            cliente = self.operacoes_crud.obter_cliente_por_codigo(codigo_cliente)
            if cliente:
                # Se o cliente existe, abrir a janela de realização da compra
                realizar_compra_window = tk.Toplevel(self.master)
                realizar_compra_window.title("Realizar compra")

                # Adicionar opções de forma de pagamento
                formas_pagamento = ['Cartão', 'Boleto', 'Pix', 'Berries']
                pagamento_var = tk.StringVar(realizar_compra_window)
                pagamento_var.set(formas_pagamento[0])  # Definir a primeira opção como padrão

                label_pagamento = tk.Label(realizar_compra_window, text="Escolha a forma de pagamento:")
                label_pagamento.grid(row=0, column=0)
                dropdown_pagamento = tk.OptionMenu(realizar_compra_window, pagamento_var, *formas_pagamento)
                dropdown_pagamento.grid(row=0, column=1)

                label_codigo_produto = tk.Label(realizar_compra_window, text="Código do produto:")
                label_codigo_produto.grid(row=1, column=0)
                entry_codigo_produto = tk.Entry(realizar_compra_window)
                entry_codigo_produto.grid(row=1, column=1)

                label_quantidade = tk.Label(realizar_compra_window, text="Quantidade:")
                label_quantidade.grid(row=2, column=0)
                entry_quantidade = tk.Entry(realizar_compra_window)
                entry_quantidade.grid(row=2, column=1)

                label_itens_compra = tk.Label(realizar_compra_window, text="Itens da Compra:")
                label_itens_compra.grid(row=3, column=0, columnspan=2)

                itens_compra_listbox = tk.Listbox(realizar_compra_window)
                itens_compra_listbox.grid(row=4, column=0, columnspan=2)

                def adicionar_item():
                    codigo_produto = int(entry_codigo_produto.get())
                    quantidade = int(entry_quantidade.get())

                    # Verificar se a quantidade disponível é suficiente
                    produto = self.operacoes_crud.obter_produto_por_codigo(codigo_produto)
                    if produto and produto[2] >= quantidade:
                        # Atualizar a quantidade no banco de dados
                        nova_quantidade = produto[2] - quantidade
                        self.operacoes_crud.alterar_quantidade_produto(codigo_produto, nova_quantidade)

                        # Adicionar o item à lista de itens da compra
                        itens_compra_listbox.insert(tk.END, f"Produto {codigo_produto}: {quantidade} unidades")
                        entry_codigo_produto.delete(0, tk.END)
                        entry_quantidade.delete(0, tk.END)
                    else:
                        messagebox.showerror("Erro", "Quantidade insuficiente do produto!")

                def finalizar_compra():
                    # Aqui você pode adicionar a lógica para finalizar a compra,
                    # calcular o total, relacionar a compra com o cliente, etc.
                    forma_pagamento_escolhida = pagamento_var.get()
                    messagebox.showinfo("Compra realizada", f"Compra realizada com sucesso!\nForma de pagamento: {forma_pagamento_escolhida}")
                    realizar_compra_window.destroy()

                button_adicionar_item = tk.Button(realizar_compra_window, text="Adicionar Item", command=adicionar_item)
                button_adicionar_item.grid(row=5, column=0, pady=10)

                button_finalizar_compra = tk.Button(realizar_compra_window, text="Finalizar Compra", command=finalizar_compra)
                button_finalizar_compra.grid(row=5, column=1, pady=10)
            else:
                # Se o cliente não existe, exibir mensagem de erro
                messagebox.showerror("Erro", "Cliente não encontrado!")

        button_iniciar_compra = tk.Button(codigo_cliente_window, text="Iniciar Compra", command=iniciar_compra)
        button_iniciar_compra.pack()



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