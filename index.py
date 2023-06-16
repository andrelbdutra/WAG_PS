import csv

class Objeto:
    def __init__(self, atributos):
        self.atributos = atributos

def ler_csv(nome_arquivo, num_atributos):
    objetos = []
    with open(nome_arquivo, 'r') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor)  # Ignorar o cabeçalho
        for linha in leitor:
            atributos = linha[:num_atributos]
            novo_objeto = Objeto(atributos)
            objetos.append(novo_objeto)
    return objetos

# Lendo csv's
nome_arquivo_transacoes = 'transacoes.csv'
num_atributos_transacoes = 6
nome_arquivo_linkIds = 'linkIds.csv'
num_atributos_linkIds = 3
nome_arquivo_voucherCodes = 'voucherCodes.csv'
num_atributos_voucherCodes = 2

transacoes = ler_csv(nome_arquivo_transacoes, num_atributos_transacoes)
linkIds = ler_csv(nome_arquivo_linkIds, num_atributos_linkIds)
voucherCodes = ler_csv(nome_arquivo_voucherCodes, num_atributos_voucherCodes)

for transacao in transacoes:
    print(transacao.atributos[2])