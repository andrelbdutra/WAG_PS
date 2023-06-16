import csv

class Objeto:
    def __init__(self, atributos):
        self.atributos = atributos

class Parceiro:
    def __init__(self, nome, linkId, segmento):
        self.nome = nome
        self.linkId = linkId
        self.segmento = segmento
        self.qntVendaPorLink = 0
        self.qntVendaPorLinkApproved = 0
        self.qntVendaPorLinkRejected = 0
        self.lucroVendaPorLink = 0
        self.lucroVendaPorLinkApproved = 0
        self.lucroVendaPorLinkRejected = 0
        self.somatorioVendasCupons = 0
        self.cupons = []
        
    def imprime_geral(self):
        print("Parceiro(a): " + str(self.nome) + " - " + "QntPorLink: " + str(self.qntVendaPorLink) + " - " + "LucroPorLink: " + "$" + str(round(self.lucroVendaPorLink,2)))
    def imprime_approved(self):
        print("Parceiro(a): " + str(self.nome) + " - " + "QntPorLink: " + str(self.qntVendaPorLinkApproved) + " - " + "LucroPorLink: " + "$" + str(round(self.lucroVendaPorLinkApproved,2)))
    def imprime_rejected(self):
        print("Parceiro(a): " + str(self.nome) + " - " + "QntPorLink: " + str(self.qntVendaPorLinkRejected) + " - " + "LucroPorLink: " + "$" + str(round(self.lucroVendaPorLinkRejected,2)))


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

# converte dolar para float
def dolar_para_float():
    for transacao in transacoes:
        transacao.atributos[2] = transacao.atributos[2].replace("$", "")
        transacao.atributos[2] = transacao.atributos[2].replace(",", ".")
dolar_para_float()

# salva parceiros
parceiros = []
for linkId in linkIds:
    novo_parceiro = Parceiro(linkId.atributos[0], linkId.atributos[1], linkId.atributos[2])
    parceiros.append(novo_parceiro)


# pega quantidade de vendas por link (total, approved e rejected) dos parceiros
for transacao in transacoes:
    for parceiro in parceiros:
        if(transacao.atributos[4] == parceiro.linkId ):
            parceiro.qntVendaPorLink = parceiro.qntVendaPorLink + 1
            parceiro.lucroVendaPorLink = parceiro.lucroVendaPorLink + float(transacao.atributos[2])
        if(transacao.atributos[4] == parceiro.linkId and transacao.atributos[5] == "Approved"):
            parceiro.qntVendaPorLinkApproved = parceiro.qntVendaPorLinkApproved + 1
            parceiro.lucroVendaPorLinkApproved = parceiro.lucroVendaPorLinkApproved + float(transacao.atributos[2])
        if(transacao.atributos[4] == parceiro.linkId and transacao.atributos[5] == "Rejected"):
            parceiro.qntVendaPorLinkRejected = parceiro.qntVendaPorLinkRejected + 1
            parceiro.lucroVendaPorLinkRejected = parceiro.lucroVendaPorLinkRejected + float(transacao.atributos[2])

# imprime a quantidade que cada parceiro vendeu nos seus respectivos links associados e o lucro total
print("\n" * 15)
print("__GERAL:__ ")
for parceiro in parceiros:
    parceiro.imprime_geral()
print("----------------------------------------------------------------")
print("__APPROVED:__ ")
for parceiro in parceiros:
    parceiro.imprime_approved()
print("----------------------------------------------------------------")
print("__REJECTED:__ ")
for parceiro in parceiros:
    parceiro.imprime_rejected()