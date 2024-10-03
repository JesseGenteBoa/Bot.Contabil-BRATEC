from pyautogui import hotkey, press, write, FAILSAFE, FailSafeException
from pyperclip import paste
from time import sleep
import pyscreeze
import utils


FAILSAFE = False

def escreverValorUnit(valor_unit_convertido, passos=6):
    press(["right"]*passos)
    valor_unit_convertido = utils.formatador(valor_unit_convertido, casas_decimais="{:.6f}")
    sleep(0.2)
    write(valor_unit_convertido)
    sleep(0.2)
    press(["right"]*3)
    utils.checarFailsafe()
 
 
def verificarValorDoItem(lista, indiceX):
    cancelar_lancamento = False
    razoes = []
    sleep(0.7)
    press(["right"]*4)
    sleep(0.7)
    hotkey("ctrl", "c")
    sleep(0.7)
    utils.checarFailsafe()
    valor_do_item_no_siga = paste()
    valor_do_item_no_siga = utils.formatador4(valor_do_item_no_siga)
    valor_do_item_na_NF = lista[indiceX][0]
    valor_do_item_na_NF = utils.formatador3(valor_do_item_na_NF)
    if valor_do_item_no_siga != valor_do_item_na_NF:
        write(lista[indiceX][0])
        sleep(0.8)
        encontrar = utils.encontrarImagem(r'_internal\Imagens\valitenErrado.png')
        utils.checarFailsafe()
        if type(encontrar) == pyscreeze.Box:
            press("enter")
            sleep(0.5)
            encontrar = utils.encontrarImagem(r'_internal\Imagens\valitenErrado.png')
            utils.checarFailsafe()
            if type(encontrar) == pyscreeze.Box:
                press("enter")
            press("esc")
            press(["left"]*5)
            sleep(0.2)
            hotkey("ctrl", "c", interval=0.5)
            utils.checarFailsafe()
            quantidade_siga = paste()
            quantidade_siga = utils.formatador4(quantidade_siga)
            quantidade_NF = lista[indiceX][1]
            quantidade_NF = utils.formatador3(quantidade_NF)
            valor_unit_NF = lista[indiceX][2]
            valor_unit_NF = utils.formatador3(valor_unit_NF)
            if quantidade_siga == quantidade_NF:
                escreverValorUnit(valor_unit_NF, passos=1)
                utils.checarFailsafe()
            else:
                press(["left"]*5)
                sleep(0.2)
                hotkey("ctrl", "c", interval=0.5)
                utils.checarFailsafe()
                desc_prod = paste()
                desc_prod = desc_prod.lower()
                if "abracadeira" in desc_prod:
                    quantidade_convertida = quantidade_NF * 100
                    if quantidade_convertida == quantidade_siga:
                        valor_unit_convertido = valor_unit_NF / 100
                        escreverValorUnit(valor_unit_convertido)
                        utils.checarFailsafe()
                    else:
                        razoes, cancelar_lancamento = utils.contarItemFracionado(quantidade_siga, valor_unit_convertido, quantidade_convertida)
                elif "pilha" in desc_prod or "tubo isolante" in desc_prod:
                    quantidade_convertida = quantidade_NF * 2
                    if quantidade_convertida == quantidade_siga:
                        valor_unit_convertido = valor_unit_NF / 2
                        escreverValorUnit(valor_unit_convertido)
                        utils.checarFailsafe()
                    else:
                        razoes, cancelar_lancamento = utils.contarItemFracionado(quantidade_siga, valor_unit_convertido, quantidade_convertida)
                elif "gas" in desc_prod:
                    press("left")
                    hotkey("ctrl", "c", interval=0.5)
                    cod_do_item = paste()
                    press("right")
                    utils.checarFailsafe()
                    if cod_do_item == "0651000053":
                        razoes, cancelar_lancamento = utils.contarItemFracionado(quantidade_siga, valor_unit_NF, quantidade_NF)
                    else:
                        valor_unit_convertido = valor_do_item_na_NF / quantidade_siga
                        escreverValorUnit(valor_unit_convertido)
                        utils.checarFailsafe()
                elif "pedrisco" in desc_prod or "cabo" in desc_prod[:4] or "manta" in desc_prod or "lona" in desc_prod:
                    valor_unit_convertido = valor_do_item_na_NF / quantidade_siga
                    escreverValorUnit(valor_unit_convertido)
                    utils.checarFailsafe()
                else:
                    razoes, cancelar_lancamento = utils.contarItemFracionado(quantidade_siga, valor_unit_NF, quantidade_NF)
        else:
            press("left")
        utils.checarFailsafe()
    return cancelar_lancamento, razoes

def corrigirPassosHorizontal(cont, item):
    if len(item) > 1:
        press(["right"]*4)
        sleep(1)
        if cont == len(item):
            press(["left"]*4)

def copiarNatureza():
    press("right", interval=0.7)
    hotkey("ctrl", "c")
    sleep(0.7)
    natureza = paste()
    if natureza == "2020081":
        natureza = "2050006"
        utils.escreverNatureza(natureza)
    elif natureza == "2020060":
        natureza = "2050004"
        utils.escreverNatureza(natureza)
    elif natureza in ["2020082", "2020083"]:
        natureza = "2050008"
        utils.escreverNatureza(natureza)
    utils.checarFailsafe()
    return natureza


def selecionarCaso(natureza):
    codigo = {
    "2020067": 0, "2020085": 0, "2020047": 0, "2020049": 0, "2020055": 0,
    "2020045": 0, "2020006": 0, "2020041": 0, "2020048": 0, "2020042": 0,
    "2020046": 0, "2020030": 0, "2020031": 0, "2020074": 0, "2020019": 0,
    "2020040": 0, "2020056": 0, "2020075": 0, "2010016": 0,
    "2010005": 1, "2020027": 1, "2020036": 1,
    "2050003": 2, "2050004": 2, "2050005": 2, "2050006": 2,
    "2050007": 2, "2050008": 2, "2050009": 2,
    "2050001": 3,
    "2040005": 4,
    "2020029": 5, "2020053": 5,
    "2020018": 6, "2040001": 6, "2040003": 6, "2020101": 6
}
    return codigo.get(natureza, 7)


def definirTES(codigo, ctrl_imposto):
    press(["left"]*10)
    global tes
    if codigo == 0:
        if ctrl_imposto != 0:
            tes = "438"
        else:
            tes = "420"
    elif codigo == 1:
        if ctrl_imposto == 0:
            tes = "402"
        elif ctrl_imposto in [6,1,2]:
            tes = "433"
        elif ctrl_imposto == 7:
            tes = "435"
        else:
            tes = "434"
    elif codigo == 2:
        if ctrl_imposto not in [7, 5, 4, 3]:
            tes = "436"
        else:
            tes = "437"
    elif codigo == 3:
        tes = "423"
    elif codigo == 4:
        if ctrl_imposto not in [7, 5, 4, 3]:
            tes = "102"
        else:
            tes = "432"
    elif codigo == 5:
        hotkey("ctrl", "c", interval=0.5)
        tes_padrao = paste()
        if tes_padrao == "406" or tes_padrao == "439":
            tes = "439"
        else:
            if ctrl_imposto == 0:
                tes = "402"
            elif ctrl_imposto == 7:
                tes = "435"
            elif ctrl_imposto in [6,1,2]:
                tes = "433"
            else:
                tes = "434"
    elif codigo == 6:
        hotkey("ctrl", "c", interval=0.5)
        tes_padrao = paste()
        if tes_padrao == "406" or tes_padrao == "439":
            tes = "439"
        else:
            press(["left"]*2)
            sleep(0.7)
            hotkey("ctrl", "c", interval=0.5)
            item_especifico = paste()
            press(["right"]*2)
            if item_especifico in ["0207000001", "1312000156", "999920091200", "999949011000", "1303102887", "1302578", "1303100449", "1303100601", "1303100602", "1303100603", "1312000122", "1312000124", "1312000125", "1312000126", "1312000144", "1308002", "1312024", "1303100550", "1303100600", "1303101290", "1303101291", "1303103835", "1303103836", "1303103837", "1312000141"]:
                if ctrl_imposto != 0:
                    tes = "438"
                else:
                    tes = "420"
            else:
                if ctrl_imposto == 0:
                    tes = "402"
                elif ctrl_imposto in [6,1,2]:
                    tes = "433"
                elif ctrl_imposto == 7:
                    tes = "435"
                else:
                    tes = "434"
    elif codigo == 7:
        cancelar_lancamento = True
        utils.cancelarLancamento()
        utils.voltarEDescer()
        sleep(0.3)
        tes = cancelar_lancamento
    utils.checarFailsafe()
    return tes
    

def zerarImposto(passos_ida=7, passos_volta=8):
    press(["right"]*passos_ida)
    press("enter")
    press("backspace")
    press("enter")
    press(["left"]*passos_volta)
    utils.checarFailsafe()


def escreverTES(tes, natureza):
    press("enter", interval=0.3)
    write(tes)
    press(["right"]*9)
    write(natureza)
    press("enter", interval=0.3)
    press(["left"]*6)
    utils.checarFailsafe()


def inserirDesconto(desc_no_item):
    press(["right"]*3)
    sleep(0.5)
    press("enter")
    desc_no_item = utils.formatador2(desc_no_item)
    write(desc_no_item, interval=0.02)
    sleep(0.5)
    utils.checarFailsafe()


def inserirFrete(frete_no_item):
    press(["right"]*105)
    sleep(0.6)
    press("enter")
    frete_no_item = utils.formatador2(frete_no_item)
    write(frete_no_item, interval=0.05)
    sleep(0.6)
    utils.checarFailsafe()


def inserirSeguro(seg_no_item):
    sleep(0.3)
    press("enter")
    seg_no_item = utils.formatador2(seg_no_item)
    write(seg_no_item, interval=0.05)
    sleep(0.6)
    utils.checarFailsafe()


def inserirDespesa(desp_no_item):
    sleep(0.3)
    press("enter")
    desp_no_item = utils.formatador2(desp_no_item)
    write(desp_no_item, interval=0.05)
    sleep(0.6)
    press(["left"]*112)
    utils.checarFailsafe()


def inserirICMS(icms_no_item, bc_icms, aliq_icms):
    press(["right"]*7)
    sleep(0.5)
    press("enter")
    bc_icms = utils.formatador2(bc_icms)
    write(bc_icms)
    press(["right"]*8)
    sleep(0.5)
    press("enter")
    utils.checarFailsafe()
    write(aliq_icms)
    sleep(0.5)
    press(["left"]*9)
    sleep(0.5)
    press("enter")
    icms_no_item = utils.formatador2(icms_no_item)
    write(icms_no_item)
    utils.checarFailsafe()


def inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=9):
    press(["right"]*passosST)
    sleep(0.5)
    press("enter")
    base_icms_ST = utils.formatador2(base_icms_ST)
    write(base_icms_ST)
    sleep(0.5)
    press("enter")
    utils.checarFailsafe()
    write(aliq_icms_ST)
    sleep(0.5)
    press("enter")
    icmsST_no_item = utils.formatador2(icmsST_no_item)
    write(icmsST_no_item)
    press(["left"]*12)    
    utils.checarFailsafe()


def inserirIPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=12):
    press(["right"]*passosIPI)
    sleep(0.5)
    press("enter")
    base_ipi = utils.formatador2(base_ipi)
    write(base_ipi)
    press(["right"]*5)
    sleep(0.5)
    press("enter")
    utils.checarFailsafe()
    write(aliq_ipi)
    press(["left"]*6)
    sleep(0.5)
    press("enter")
    ipi_no_item = utils.formatador2(ipi_no_item)
    write(ipi_no_item)
    press(["left"]*14)
    utils.checarFailsafe()

