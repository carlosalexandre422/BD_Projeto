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
                            endereco TEXT,
                            torce_para_flamengo TEXT,
                            assiste_one_piece TEXT,
                            de_sousa TEXT
                            )''')
        self.conn.commit()

    def inserir_estoque(self, produto):
        self.c.execute('''INSERT INTO estoque (nome, quantidade, preco) 
                          VALUES (?, ?, ?)''', (produto.nome, produto.quantidade, produto.preco))
        self.conn.commit()

    def filtrar_produtos_com_poucas_unidades(self):
        self.c.execute("SELECT * FROM estoque WHERE quantidade < 5")
        produtos_com_poucas_unidades = self.c.fetchall()
        return produtos_com_poucas_unidades

    def obter_produto_por_codigo(self, codigo):
        self.c.execute('''SELECT * FROM estoque WHERE codigo=?''', (codigo,))
        produto = self.c.fetchone()
        return produto

    def obter_quantidade_em_estoque(self, codigo_produto):
        self.c.execute('''SELECT quantidade FROM estoque WHERE codigo=?''', (codigo_produto,))
        quantidade = self.c.fetchone()
        if quantidade:
            return quantidade[0]
        else:
            return 0
        
    def alterar_quantidade_produto(self, codigo, nova_quantidade):
        # Verificar se a nova quantidade é maior ou igual a zero
        if nova_quantidade >= 0:
            # Atualizar a quantidade do produto no banco de dados
            self.c.execute('''UPDATE estoque SET quantidade=? WHERE codigo=?''', (nova_quantidade, codigo))
            self.conn.commit()
        else:
            # Se a nova quantidade for menor que zero, lançar uma exceção ou lidar com o erro de acordo com sua lógica
            raise ValueError("A nova quantidade não pode ser menor que zero.")

    def inserir_cliente(self, cliente):
        self.c.execute('''INSERT INTO clientes (nome, telefone, endereco, torce_para_flamengo, assiste_one_piece, de_sousa) 
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                          (cliente.nome, cliente.telefone, cliente.endereco, cliente.torce_para_flamengo, cliente.assiste_one_piece, cliente.de_sousa))
        self.conn.commit()

    def alterar_estoque(self, codigo, novo_produto):
        self.c.execute('''UPDATE estoque SET nome=?, quantidade=?, preco=? WHERE codigo=?''',
                       (novo_produto.nome, novo_produto.quantidade, novo_produto.preco, codigo))
        self.conn.commit()

    def alterar_cliente(self, codigo, novo_cliente):
        self.c.execute('''UPDATE clientes SET nome=?, telefone=?, endereco=? WHERE codigo=?''',
                       (novo_cliente.nome, novo_cliente.telefone, novo_cliente.endereco, codigo))
        self.conn.commit()

    def pesquisar_produto_por_nome(self, nome_produto, faixa_preco, categoria, fabricado_em_mari):
        resultados = []
        query = '''SELECT * FROM estoque WHERE nome LIKE ?'''
        params = ('%' + nome_produto + '%',)

        # Filtrar pela faixa de preço
        if faixa_preco == 'abaixo de 100 reais':
            query += ' AND preco < 100'
        elif faixa_preco == 'acima de 100 reais':
            query += ' AND preco >= 100'

        # Filtrar pela categoria
        if categoria == 'alimento':
            query += ' AND categoria = "alimento"'
        elif categoria == 'itens diversos':
            query += ' AND categoria = "itens diversos"'

        # Filtrar pelo local de fabricação
        if fabricado_em_mari == 'sim':
            query += ' AND fabricado_em_mari = 1'
        elif fabricado_em_mari == 'não':
            query += ' AND fabricado_em_mari = 0'

        for col in self.c.execute(query, params):
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
    
    def obter_cliente_por_codigo(self, codigo):
        self.c.execute('''SELECT * FROM clientes WHERE codigo=?''', (codigo,))
        cliente = self.c.fetchone()
        return cliente