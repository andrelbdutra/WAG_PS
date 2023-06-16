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
        self.somatorioVendasVouchers = 0
        self.vouchers = []
        self.vouchersSUM = {}
        
    def imprime_geral_links(self):
        print("Parceiro(a): " + str(self.nome) + " | " + "Qnt_Por_Link: " + str(self.qntVendaPorLink) + " | " + "Valor_Por_Link: " + str("${:,.2f}".format(self.lucroVendaPorLink,2)))
    def imprime_approved_links(self):
        print("Parceiro(a): " + str(self.nome) + " | " + "Qnt_Por_Link: " + str(self.qntVendaPorLinkApproved) + " | " + "Valor_Por_Link: " + "$" + str(round(self.lucroVendaPorLinkApproved,2)))
    def imprime_rejected_links(self):
        print("Parceiro(a): " + str(self.nome) + " | " + "Qnt_Por_Link: " + str(self.qntVendaPorLinkRejected) + " | " + "Valor_Por_Link: " + "$" + str(round(self.lucroVendaPorLinkRejected,2)))
    def imprime_somatorio_Vendas_Vouchers(self):
        print("Parceiro(a): " + str(self.nome) + " | " + "Vouchers: " + str(self.vouchers) + " | " + "Somatorio: " + str("${:,.2f}".format(self.somatorioVendasVouchers)))
    def imprime_somatorio_vendas_cada_voucher(self):
        for key, value in self.vouchersSUM.items():
            print("Parceiro(a): " + str(self.nome) + " | " + "Voucher: " + str(key) + " | " + "Somatorio: " + str("${:,.2f}".format(value)))

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

def gerar_csv(nome_arquivo, tuplas):
    with open('outputData/'+nome_arquivo, 'w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerows(tuplas)

# Lendo csv's
nome_arquivo_transacoes = 'inputData/transacoes.csv'
num_atributos_transacoes = 6
nome_arquivo_linkIds = 'inputData/linkIds.csv'
num_atributos_linkIds = 3
nome_arquivo_voucherCodes = 'inputData/voucherCodes.csv'
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

# salva os vouchers de cada parceiro
for parceiro in parceiros:
    for voucherCode in voucherCodes:
        if(parceiro.nome == voucherCode.atributos[0]):
            parceiro.vouchers.append(voucherCode.atributos[1])
            parceiro.vouchersSUM[voucherCode.atributos[1]] = 0

# realiza o somatorio dos valores dos vouchers
for parceiro in parceiros:
    for key, value in parceiro.vouchersSUM.items():
        for transacao in transacoes:
            if(transacao.atributos[3] == key):
                parceiro.vouchersSUM[key] = parceiro.vouchersSUM[key] + float(transacao.atributos[2])

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

# inicializando segmentos e analizando seus valores
segmentos = {}
for parceiro in parceiros:
    segmentos[parceiro.segmento] = 0
for parceiro in parceiros:
    segmentos[parceiro.segmento] = segmentos[parceiro.segmento] + parceiro.lucroVendaPorLink
segmentosSorted = sorted(segmentos.items(), key=lambda x: x[1], reverse=True)


# impressão questão 1, imprime no console e gera um arquivo csv
def impressao_geral_links():
    print("\n" * 15)
    print("__VENDAS_POR_PARCEIRO (Decrescente):__ ")
    parceiros.sort(key=lambda x: x.lucroVendaPorLink, reverse=True)
    tuplasVPP = [('Parceiro(a)', 'Qnt_Por_Link', 'Valor_Por_Link')]
    for parceiro in parceiros:
        tuplasVPP.append((parceiro.nome, parceiro.qntVendaPorLink, str("${:,.2f}".format(parceiro.lucroVendaPorLink))))
        parceiro.imprime_geral_links()
    gerar_csv("VENDAS_POR_PARCEIRO", tuplasVPP)

# impressao extras (não requisitadas, porém relevantes), imprime no console e gera um arquivo csv
def impressoes_extras():
    print("----------------------------------------------------------------")
    print("__APPROVED_TRANSACTIONS (Decrescente):__ ")
    parceiros.sort(key=lambda x: x.lucroVendaPorLinkApproved, reverse=True)
    tuplasAT = [('Parceiro(a)', 'Qnt_Por_Link', 'Valor_Por_Link')]
    for parceiro in parceiros:
        tuplasAT.append((parceiro.nome, parceiro.qntVendaPorLinkApproved, str("${:,.2f}".format(parceiro.lucroVendaPorLinkApproved))))
        parceiro.imprime_approved_links()
    gerar_csv("APPROVED_TRANSACTIONS", tuplasAT)
    print("----------------------------------------------------------------")
    print("__REJECTED_TRANSACTIONS (Decrescente):__ ")
    parceiros.sort(key=lambda x: x.lucroVendaPorLinkRejected, reverse=True)
    tuplasRT = [('Parceiro(a)', 'Qnt_Por_Link', 'Valor_Por_Link')]
    for parceiro in parceiros:
        parceiro.imprime_rejected_links()
        tuplasRT.append((parceiro.nome, parceiro.qntVendaPorLinkApproved, str("${:,.2f}".format(parceiro.lucroVendaPorLinkApproved))))
    gerar_csv("REJECTED_TRANSACTIONS", tuplasRT)
    print("----------------------------------------------------------------")
    print("__VOUCHERS_SUM:__ ")
    for parceiro in parceiros:
        parceiro.imprime_somatorio_vendas_cada_voucher()
    print("----------------------------------------------------------------")
    print("__VENDAS_POR_SEGMENTO (Decrescente):__ ")
    tuplasVPS = [('Segmento', 'SUM')]
    for i in segmentosSorted:
        tuplasVPS.append((str(i[0]), str("${:,.2f}".format(i[1]))))
        print("Segmento: " + str(i[0]) + " | " + "Valores: " + str("${:,.2f}".format(i[1])))
    gerar_csv("VENDAS_POR_SEGMENTO", tuplasVPS)

# imprime o somatorio individual de vendas de cada voucher associado aos parceiros, imprime no console e gera um arquivo csv
def impressao_vendas_vouchers():
    print("----------------------------------------------------------------")
    print("__VOUCHERS_TOTAL_SUM (Decrescente):__ ")
    tuplasVouchers = []
    for parceiro in parceiros:
        parceiro.somatorioVendasVouchers = sum(parceiro.vouchersSUM.values())
    parceiros.sort(key=lambda x: x.somatorioVendasVouchers, reverse=True)
    tuplasVouchers.append(("Parceiro(a)", "Vouchers", "SUM"))
    for parceiro in parceiros:
        tuplasVouchers.append((parceiro.nome, parceiro.vouchers, str("${:,.2f}".format((parceiro.somatorioVendasVouchers)))))
        parceiro.imprime_somatorio_Vendas_Vouchers()
    gerar_csv("VOUCHERS_TOTAL_SUM", tuplasVouchers)

impressao_geral_links()
impressao_vendas_vouchers()
impressoes_extras()
