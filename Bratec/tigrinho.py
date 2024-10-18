from pyautogui import hotkey, press, write, FAILSAFE, FailSafeException
from pydirectinput import click as mouseClique, moveTo
from selenium import webdriver                         
from selenium.webdriver.common.by import By
from pyperclip import paste, copy     
from time import sleep
import xmltodict   
import pyscreeze
import utils
import extratorXML
import tratamentoItem
import operadoresLancamento


FAILSAFE = True
contador = 0
sem_boleto = []
processo_bloqueado = []
processo_errado = []
XML_ilegivel = []
nao_lancadas = []
processos_ja_vistos = []
mensagem_sb = "Processo sem boleto."
mensagem_pb = "Processo Bloqueado."
mensagem_pe = "Processo com algum erro impeditivo de lançamento."
mensagem_xi = "Processo com um XML que não consigo ler."


cnpj_dict = {'27462720000125': '01', '27462720000397': '03', '27462720000478': '04', '27462720000559': '05', '27462720000630': '06'}


def robozinho():
    try:
        ver_documento = r'Imagens\verDocumentos.png'
        utils.insistirNoClique(ver_documento, cliques=1)
        sleep(0.4)
        insistir_no_clique = utils.encontrarImagem(ver_documento)
        if type(insistir_no_clique) == pyscreeze.Box:
            while True:
                utils.insistirNoClique(ver_documento, cliques=1)
                insistir_no_clique = utils.encontrarImagem(ver_documento)
                if type(insistir_no_clique) != pyscreeze.Box:
                    break
        hotkey("alt", "d", interval=0.1)
        sleep(0.5)
        hotkey("ctrl", "c")
        sleep(0.5)
        link = paste()
        options = webdriver.ChromeOptions()
        options.add_argument(r'user-data-dir=C:\Users\Usuario\AppData\Local\Google\Chrome\User Data\Profile Selenium')
        driver = webdriver.Chrome(options=options)
        sleep(0.5)
        driver.get(link)
        sleep(2)
        tempo_max = 0


        while True:
            try:
                elemento1 = driver.find_element(By.XPATH, '/html/body/app-root/app-main/div/app-processo-pagamento-nota-manutencao/po-page-default/po-page/div/po-page-content/div/div[2]/po-tabs/div[1]/div/div/po-tab-button[2]/div[1]/span')
                sleep(0.3)
                elemento1.click()
                
                if elemento1 != '':
                    try:
                        elemento2 = driver.find_element(By.XPATH, '/html/body/app-root/app-main/div/app-processo-pagamento-nota-manutencao/po-page-default/po-page/div/po-page-content/div/div[1]/div[1]/po-widget/div/po-container/div/div/po-info[5]/div/div[2]/span')
                        chave_de_acesso = elemento2.text
                        try:
                            verificador = processos_ja_vistos.index(chave_de_acesso)
                            utils.erroNoPortal()
                            driver.quit()
                            sleep(0.2)
                            return robozinho() 

                        except:
                            processos_ja_vistos.append(chave_de_acesso)
                            
                        elemento3 = driver.find_element(By.XPATH, '/html/body/app-root/app-main/div/app-processo-pagamento-nota-manutencao/po-page-default/po-page/div/po-page-content/div/div[2]/po-tabs/div[2]/po-tab[2]/div[1]/po-select/po-field-container/div/div[2]/select')
                        valor = elemento3.get_attribute("value")

                        if valor == 'B':
                            try:
                                elemento4 = driver.find_element(By.XPATH, '/html/body/app-root/app-main/div/app-processo-pagamento-nota-manutencao/po-page-default/po-page/div/po-page-content/div/div[2]/po-tabs/div[2]/po-tab[2]/div[2]/po-table/po-container/div/div/div/div/div/table/tbody[1]/tr/td[4]/div/span/div[3]/po-input/po-field-container/div/div[2]/input')
                                boleto = elemento4.get_attribute("value")
                                #if len(boleto) == 0:
                                #    utils.erroNoPortal()
                                #    driver.quit()
                                #    utils.acrescerLista(sem_boleto, nao_lancadas, link, mensagem_sb)
                                #    sleep(0.2)                                
                                #    return robozinho()
                                #else:
                                driver.quit() 
                                break

                            except Exception as e:
                                tempo_max += 1 
                                pass  

                        else:
                            driver.quit() 
                            break                                           

                    except Exception as e:
                        tempo_max += 1 
                        pass  

            except Exception as e:
                tempo_max += 1 
                pass
            
            if tempo_max == 15:
                press("enter")
            if tempo_max == 40:
                utils.erroNoPortal()
                driver.quit()
                sleep(0.2)
                return robozinho()  
            
        sleep(0.2)
        hotkey("ctrl", "w")
        sleep(0.3)


        caminho = "C:\\Users\\Usuario\\Desktop\\xmlFiscalio\\" + chave_de_acesso + ".xml"

        while True:
            try:
                with open(caminho) as fd:
                    doc = xmltodict.parse(fd.read())
                    break
            except UnicodeDecodeError:
                with open(caminho, encoding='utf-8') as fd:
                    doc = xmltodict.parse(fd.read())
                    break
            except FileNotFoundError:
                while True:
                    exportarXML = r'Imagens\exportarXML.png'
                    encontrar = utils.encontrarImagemLocalizada(exportarXML)
                    if type(encontrar) != tuple:  
                        utils.insistirNoClique(exportarXML)
                        sleep(2)
                        caixa_de_texto = utils.encontrarImagemLocalizada(r'Imagens\clicarServidor.png')
                        if type(caixa_de_texto) == tuple:
                            break
                    else:
                        x, y = encontrar
                        mouseClique(x,y, clicks=2)
                        break
                sleep(2)
                x, y = caixa_de_texto
                mouseClique(x,y, clicks=3, interval=0.07)
                copy("C:\\Users\\Usuario\\Desktop\\xmlFiscalio\\")
                hotkey("ctrl", "v")
                sleep(1)
                press(["tab"]*6, interval=0.5)
                press("enter")
                sleep(0.8)
                caixa_de_texto = utils.encontrarImagemLocalizada(r'Imagens\clicarServidor.png')
                if type(caixa_de_texto) == tuple:
                    botao_salvar = utils.encontrarImagemLocalizada(r'Imagens\botaoSalvar1.png')
                    x, y = botao_salvar
                    mouseClique(x,y, clicks=2)
                cont=0
                while True:
                    aparece_enter = utils.encontrarImagem(r'Imagens\XMLEnter.png')
                    if type(aparece_enter) == pyscreeze.Box:
                        press("enter")
                        sleep(0.8)
                    aparece_enter2 = utils.encontrarImagem(r'Imagens\XMLEnter2.png')
                    if type(aparece_enter2) == pyscreeze.Box:
                        break
                while type(aparece_enter2) == pyscreeze.Box:
                    press("enter")
                    sleep(0.5)
                    aparece_enter2 = utils.encontrarImagem(r'Imagens\XMLEnter2.png')
                caminho = "C:\\Users\\Usuario\\Desktop\\xmlFiscalio\\" + chave_de_acesso + ".xml"
                auxiliar = False
            except:
                with open(caminho, encoding='utf-8') as fd:
                    doc = xmltodict.parse(fd.read(), attr_prefix="@", cdata_key="#text")
                    break
        
        
        processador = extratorXML.ProcessadorXML(doc, cnpj_dict)
        valor_total_da_nf, filial_xml, parcelas = processador.processarTotaisNotaFiscal()

        const_item = 0
        while True:
            try:
                coletor_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]
                impostos_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]
                valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                break
            except KeyError:
                try:
                    coletor_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"]["prod"]
                    impostos_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"]["imposto"]
                    valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                    break
                except KeyError:
                    try:
                        coletor_xml = doc["NFe"]["infNFe"]["det"]["prod"]
                        impostos_xml = doc["NFe"]["infNFe"]["det"]["imposto"]
                        valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                        break
                    except TypeError:
                        try:
                            coletor_xml = doc["NFe"]["infNFe"]["det"][const_item]["prod"]
                            impostos_xml = doc["NFe"]["infNFe"]["det"][const_item]["imposto"]
                            valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                            const_item += 1
                        except IndexError:
                            break
                except TypeError:
                    try:
                        coletor_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"][const_item]["prod"]
                        impostos_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"][const_item]["imposto"]
                        valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                        const_item += 1
                    except IndexError:
                        break
            except TypeError:
                try:
                    coletor_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"][const_item]["prod"]
                    impostos_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"][const_item]["imposto"]
                    valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                    const_item += 1
                except IndexError:
                    break

        itens, indices_e_impostos = processador.trabalharDadosXML(valores_do_item)


        while True:
            utils.clicarDadosDaNota()
            sleep(1)
            abriu_a_tela = utils.encontrarImagemLocalizada(r'Imagens\abriuDadosDaNota.png')
            if type(abriu_a_tela) == tuple:
                break    
        while True:
            press("tab")
            sleep(0.7)
            hotkey("ctrl", "c")
            filial_pedido = paste()
            if filial_pedido == filial_xml:
                press("tab", interval=0.5)
                press("enter")
                sleep(1)
                clicar_confirmar = utils.encontrarImagemLocalizada(r'Imagens\clicarConfirmar.png')
                if type(clicar_confirmar) == tuple:
                    cont = 0
                    while cont < 5:
                        moveTo(150, 100)
                        x, y = clicar_confirmar
                        mouseClique(x,y, clicks=2, interval=0.07)
                        cont+=1
                break
            else:
                try:
                    press(["tab"]*2, interval=0.5)
                    press("enter")
                    sleep(1)
                    clicar_cancelar = utils.encontrarImagemLocalizada(r'Imagens\CancelarFilial.png')
                    if type(clicar_cancelar) == tuple:
                        while type(clicar_cancelar) == tuple:
                            moveTo(150, 100)
                            x, y = clicar_cancelar
                            mouseClique(x,y, clicks=2, interval=0.07)
                            clicar_cancelar = utils.encontrarImagemLocalizada(r'Imagens\CancelarFilial.png')  
                    utils.cancelar1()
                    utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                    return robozinho()
                except TypeError:
                    utils.clicarDadosDaNota()


        try:
            sleep(0.5)
            aparece_enter = utils.encontrarImagem(r'Imagens\AtencaoEstoque.png')
            if type(aparece_enter) == pyscreeze.Box:
                sleep(0.2)
                press("enter")
            aparece_enter2 = utils.encontrarImagem(r'Imagens\TES102.png')
            if type(aparece_enter2) == pyscreeze.Box:
                sleep(0.2)
                press("enter")
                sleep(0.2)
                press(["tab"]*2)
                sleep(0.2)
                write("102")
                sleep(0.2)
                press(["tab"]*2, interval=0.5)
                sleep(0.2)
                press("enter") 
        finally:
            pass


        tela_de_lancamento = utils.encontrarImagem(r'Imagens\AbriuOProcesso.png')
        cont = 0
        while type(tela_de_lancamento) != pyscreeze.Box:
            cont +=1

            tela_de_lancamento = utils.encontrarImagem(r'Imagens\AbriuOProcesso.png')
            lancamento_retroativo = utils.encontrarImagem(r'Imagens\LancamentoRetroativo.png')
            nota_ja_lancada = utils.encontrarImagem(r'Imagens\ProcessoJaLancado.png')
            fornecedor_bloqueado = utils.encontrarImagem(r'Imagens\FornecedorBloqueado.png')
            if type(lancamento_retroativo) == pyscreeze.Box or type(nota_ja_lancada) == pyscreeze.Box or type(fornecedor_bloqueado) == pyscreeze.Box:
                sleep(1)
                press("enter")
                sleep(1)
                if type(fornecedor_bloqueado) == pyscreeze.Box:
                    utils.acrescerLista(processo_bloqueado, nao_lancadas, link, mensagem_pb)
                cont = 0

            tela_de_lancamento = utils.encontrarImagem(r'Imagens\AbriuOProcesso.png')
            erro_esquisito = utils.encontrarImagem(r'Imagens\erroEsquisito2.png')
            if type(erro_esquisito) == pyscreeze.Box:
                sleep(1)
                press("enter")
                utils.cancelar1()
                return robozinho()
            
            tela_de_lancamento = utils.encontrarImagem(r'Imagens\AbriuOProcesso.png')
            erro_generico = utils.encontrarImagem(r'Imagens\ErroGenerico.png')
            if type(erro_generico) == pyscreeze.Box:
                sleep(1)
                press("enter", interval=2) 
                press("esc", interval=2) 
                press("enter", interval=2)    
                utils.cancelar1()
                utils.acrescerLista(processo_bloqueado, nao_lancadas, link, mensagem_pb)
                return robozinho()
            
            tela_de_lancamento = utils.encontrarImagem(r'Imagens\AbriuOProcesso.png')
            chave_nao_encontrada = utils.encontrarImagem(r'Imagens\chaveNaoEncontradaNoSefaz.png')
            nf_cancelada = utils.encontrarImagem(r'Imagens\nfCancelada.png')
            natureza_bloq = utils.encontrarImagem(r'Imagens\naturezaBloq.png')
            if type(chave_nao_encontrada) == pyscreeze.Box or type(natureza_bloq) == pyscreeze.Box or type(nf_cancelada) == pyscreeze.Box:
                sleep(1)
                press("enter")
                utils.cancelar3()
                utils.acrescerLista(processo_bloqueado, nao_lancadas, link, mensagem_pb)
                return robozinho()
            if cont == 15:
                press("enter")
                cont = 0

        sleep(0.5)
        press(["tab"]*9)
        sleep(0.8)
        press(["right"]*8)
                

        for i, ctrl_imposto in enumerate(indices_e_impostos):

            verificador, item_fracionado = operadoresLancamento.verificarValorDoItem(itens, i)
            if verificador == True:
                utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                return robozinho()
            tratamento_item = tratamentoItem.TratadorItem(item_fracionado, itens, i, ctrl_imposto)
            item = tratamento_item.tratarItem()
            cont = 0

            if ctrl_imposto == 0:
                for lista in item:
                    desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, ipi_no_item = lista
                    natureza = operadoresLancamento.copiarNatureza()
                    codigo = operadoresLancamento.selecionarCaso(natureza)
                    tes = operadoresLancamento.definirTES(codigo, ctrl_imposto)
                    if tes == True:
                        utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                        return robozinho()
                    operadoresLancamento.escreverTES(tes, natureza)
                    operadoresLancamento.inserirDesconto(desc_no_item)
                    operadoresLancamento.inserirFrete(frete_no_item)
                    operadoresLancamento.inserirSeguro(seg_no_item)
                    operadoresLancamento.inserirDespesa(desp_no_item)
                    if tes in ["102", "405", "408"]:
                        operadoresLancamento.zerarImposto()
                    elif tes in ["406", "421", "423"]:
                        operadoresLancamento.zerarImposto()
                        operadoresLancamento.zerarImposto(passos_ida=12, passos_volta=13)
                    press("down")
                    cont+=1
                    operadoresLancamento.corrigirPassosHorizontal(cont, item)
                press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SEM IMPOSTO
            elif ctrl_imposto == 1:
                for lista in item:
                    desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, bc_icms, aliq_icms, icmsST_no_item, ipi_no_item = lista
                    natureza = operadoresLancamento.copiarNatureza()
                    codigo = operadoresLancamento.selecionarCaso(natureza)
                    tes = operadoresLancamento.definirTES(codigo, ctrl_imposto)
                    if tes == True:
                        utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                        return robozinho()
                    operadoresLancamento.escreverTES(tes, natureza)
                    operadoresLancamento.inserirDesconto(desc_no_item)
                    operadoresLancamento.inserirFrete(frete_no_item)
                    operadoresLancamento.inserirSeguro(seg_no_item)
                    operadoresLancamento.inserirDespesa(desp_no_item)
                    operadoresLancamento.inserirICMS(icms_no_item, bc_icms, aliq_icms)
                    press(["left"]*9)
                    if tes in ["406", "421", "423"]:
                        operadoresLancamento.zerarImposto(passos_ida=12, passos_volta=13)
                    press("down")
                    cont+=1
                    operadoresLancamento.corrigirPassosHorizontal(cont, item)
                press("up")
                                            #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMS
            elif ctrl_imposto == 2:
                for lista in item:
                    desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item = lista
                    natureza = operadoresLancamento.copiarNatureza()
                    codigo = operadoresLancamento.selecionarCaso(natureza)
                    tes = operadoresLancamento.definirTES(codigo, ctrl_imposto)
                    if tes == True:
                        utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                        return robozinho()
                    operadoresLancamento.escreverTES(tes, natureza)
                    operadoresLancamento.inserirDesconto(desc_no_item)
                    operadoresLancamento.inserirFrete(frete_no_item)
                    operadoresLancamento.inserirSeguro(seg_no_item)
                    operadoresLancamento.inserirDespesa(desp_no_item)
                    if tes in ["102", "405", "408"]:
                        operadoresLancamento.zerarImposto()
                    elif tes in ["406", "421", "423"]:
                        operadoresLancamento.zerarImposto()
                        operadoresLancamento.zerarImposto(passos_ida=12, passos_volta=13)
                    operadoresLancamento.inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST)
                    press("down")
                    cont+=1
                    operadoresLancamento.corrigirPassosHorizontal(cont, item)
                press("up")
                                            #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMSST
            elif ctrl_imposto == 3:
                for lista in item:
                    desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi = lista
                    natureza = operadoresLancamento.copiarNatureza()
                    codigo = operadoresLancamento.selecionarCaso(natureza)
                    tes = operadoresLancamento.definirTES(codigo, ctrl_imposto)
                    if tes == True:
                        utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                        return robozinho()
                    operadoresLancamento.escreverTES(tes, natureza)
                    operadoresLancamento.inserirDesconto(desc_no_item)
                    operadoresLancamento.inserirFrete(frete_no_item)
                    operadoresLancamento.inserirSeguro(seg_no_item)
                    operadoresLancamento.inserirDespesa(desp_no_item)
                    operadoresLancamento.inserirIPI(ipi_no_item, base_ipi, aliq_ipi)
                    if tes in ["406", "421", "423", "102", "403", "411"]:
                        operadoresLancamento.zerarImposto()
                    press("down")
                    cont+=1
                    operadoresLancamento.corrigirPassosHorizontal(cont, item)
                press("up")
                                            #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA IPI
            elif ctrl_imposto == 4:
                for lista in item:
                    desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi = lista
                    natureza = operadoresLancamento.copiarNatureza()
                    codigo = operadoresLancamento.selecionarCaso(natureza)
                    tes = operadoresLancamento.definirTES(codigo, ctrl_imposto)
                    if tes == True:
                        utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                        return robozinho()
                    operadoresLancamento.escreverTES(tes, natureza)
                    operadoresLancamento.inserirDesconto(desc_no_item)
                    operadoresLancamento.inserirFrete(frete_no_item)
                    operadoresLancamento.inserirSeguro(seg_no_item)
                    operadoresLancamento.inserirDespesa(desp_no_item)
                    if tes in ["406", "421", "423", "102", "411"]:
                        operadoresLancamento.zerarImposto()
                    operadoresLancamento.inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST)
                    operadoresLancamento.inserirIPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=0)
                    press("down")
                    cont+=1
                    operadoresLancamento.corrigirPassosHorizontal(cont, item)
                press("up")
                                            #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMSST E IPI
            elif ctrl_imposto == 5:
                for lista in item:
                    desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_icms, aliq_icms, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi = lista
                    natureza = operadoresLancamento.copiarNatureza()
                    codigo = operadoresLancamento.selecionarCaso(natureza)
                    tes = operadoresLancamento.definirTES(codigo, ctrl_imposto)
                    if tes == True:
                        utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                        return robozinho()
                    operadoresLancamento.escreverTES(tes, natureza)
                    operadoresLancamento.inserirDesconto(desc_no_item)
                    operadoresLancamento.inserirFrete(frete_no_item)
                    operadoresLancamento.inserirSeguro(seg_no_item)
                    operadoresLancamento.inserirDespesa(desp_no_item)
                    operadoresLancamento.inserirICMS(icms_no_item, base_icms, aliq_icms)
                    operadoresLancamento.inserirIPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=3)
                    press("down")
                    cont+=1
                    operadoresLancamento.corrigirPassosHorizontal(cont, item)
                press("up")
                                            #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMS E IPI
            elif ctrl_imposto == 6:
                for lista in item:
                    desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item = lista
                    natureza = operadoresLancamento.copiarNatureza()
                    codigo = operadoresLancamento.selecionarCaso(natureza)
                    tes = operadoresLancamento.definirTES(codigo, ctrl_imposto)
                    if tes == True:
                        utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                        return robozinho()
                    operadoresLancamento.escreverTES(tes, natureza)
                    operadoresLancamento.inserirDesconto(desc_no_item)
                    operadoresLancamento.inserirFrete(frete_no_item)
                    operadoresLancamento.inserirSeguro(seg_no_item)
                    operadoresLancamento.inserirDespesa(desp_no_item)
                    operadoresLancamento.inserirICMS(icms_no_item, base_icms, aliq_icms)
                    operadoresLancamento.inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=0)
                    press("down")
                    cont+=1
                    operadoresLancamento.corrigirPassosHorizontal(cont, item)
                press("up")
                                            #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMS E ICMSST
            elif ctrl_imposto == 7:
                for lista in item:
                    desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi = lista
                    natureza = operadoresLancamento.copiarNatureza()
                    codigo = operadoresLancamento.selecionarCaso(natureza)
                    tes = operadoresLancamento.definirTES(codigo, ctrl_imposto)
                    if tes == True:
                        utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
                        return robozinho()
                    operadoresLancamento.escreverTES(tes, natureza)
                    operadoresLancamento.inserirDesconto(desc_no_item)
                    operadoresLancamento.inserirFrete(frete_no_item)
                    operadoresLancamento.inserirSeguro(seg_no_item)
                    operadoresLancamento.inserirDespesa(desp_no_item)
                    operadoresLancamento.inserirICMS(icms_no_item, base_icms, aliq_icms)
                    operadoresLancamento.inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=0)
                    operadoresLancamento.inserirIPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=12)
                    press("down")
                    cont+=1
                    operadoresLancamento.corrigirPassosHorizontal(cont, item)
                press("up")
                                            #SEQUENCIA LOGICA DE LANÇAMENTO PARA TODOS OS IMPOSTOS
    
            if len(indices_e_impostos) > 1:
                press("down")
            if i+1 == len(indices_e_impostos):
                press("up")
            sleep(1.5)


        aba_duplicatas = utils.encontrarImagemLocalizada(r'Imagens\AbaDuplicatas.png')
        x, y =  aba_duplicatas
        mouseClique(x,y, clicks=4, interval=0.1)
        sleep(0.6)
        lista_parc = []
        utils.clicarValorParcela()
        sleep(0.5)
        hotkey("ctrl", "c", interval=0.2)
        valor_parcela = paste()
        valor_parcela = utils.formatador4(valor_parcela)
        if valor_parcela < valor_total_da_nf:
            lista_parc.append(valor_parcela)
            while round(sum(lista_parc),2) < valor_total_da_nf:
                utils.descerECopiar()
                erro_parcela = utils.encontrarImagem(r'Imagens\ErroParcela.png')
                if type(erro_parcela) == pyscreeze.Box:
                    press("enter", interval=0.7)
                    press("enter", interval=0.7)
                    lista_parc = lista_parc[:-1]
                    valor_parc = valor_total_da_nf - round(sum(lista_parc),2)
                    valor_parc = utils.formatador2(valor_parc)
                    write(valor_parc, interval=0.03)
                    press("left")
                    lista_parc.append(float(valor_parc))
                    print(lista_parc)
                else:
                    valor_parcela = paste()
                    valor_parcela = utils.formatador4(valor_parcela)
                    lista_parc.append(valor_parcela)
            somatoria = utils.formatador2(sum(lista_parc))
            somatoria = float(somatoria)
            parcela_errada = lista_parc[-1]
            if somatoria != valor_total_da_nf:
                if lista_parc[-1] == lista_parc[-2]:
                    parcela_errada = lista_parc.pop()
                    somatoria = utils.formatador2(sum(lista_parc))
                    somatoria = float(somatoria)
                diferenca_NF_siga = valor_total_da_nf - somatoria 
                ultima_parcela = parcela_errada + diferenca_NF_siga
                ultima_parcela = "{:.2f}".format(ultima_parcela)  
                mouseClique(x,y)
                descida = len(lista_parc) - 1
                press(["down"]*descida)
                sleep(0.7)
                write(ultima_parcela, interval=0.03)
            sleep(1)
        elif valor_parcela > valor_total_da_nf:
            valor_total_da_nf = utils.formatador2(valor_total_da_nf)
            write(valor_total_da_nf)
            sleep(1)
        utils.clicarNaturezaDuplicata()
        sleep(1)
        erro_parcela = utils.encontrarImagem(r'Imagens\ErroParcela.png')
        if type(erro_parcela) == pyscreeze.Box:
            press("enter")
            utils.clicarValorParcela()
            press(["left"]*2)
            sleep(0.3)
            hotkey("ctrl", "c", interval=0.1)
            primeira_parc = paste()
            ordem_parc = []
            ordem_parc.append(primeira_parc)
            if primeira_parc == '001':
                utils.descerECopiar()
                proxima_parcela = paste()
                ordem_parc.append(proxima_parcela)
                if ordem_parc[-2] != ordem_parc[-1]:
                    while ordem_parc[-2] != ordem_parc[-1]:
                        utils.descerECopiar()
                        proxima_parcela = paste()
                        ordem_parc.append(proxima_parcela)
                    ordem_parc.pop()
                    valor_parcela = valor_total_da_nf / len(ordem_parc)
                    valor_parcela = "{:.2f}".format(valor_parcela)
                    utils.clicarValorParcela()
                    for vezes in range(len(ordem_parc)):
                        write(valor_parcela, interval=0.08)
                        press("left")
                        press("down")
                        sleep(0.8)
                    valor_parcela = utils.formatador3(valor_parcela)
                    valor_atingido = valor_parcela * len(ordem_parc)
                    sleep(2)
                    if valor_atingido != valor_total_da_nf:
                        diferenca_NF_siga = valor_atingido - valor_total_da_nf
                        valor_ultima_parcela = valor_parcela - diferenca_NF_siga
                        valor_ultima_parcela = "{:.2f}".format(valor_ultima_parcela)
                        write(valor_ultima_parcela, interval=0.08)
                        sleep(2)
            utils.clicarNaturezaDuplicata()
            sleep(0.6)
            erro_parcela = utils.encontrarImagem(r'Imagens\ErroParcela.png')
            if type(erro_parcela) == pyscreeze.Box:
                press("enter")
                utils.cancelar2()
                return robozinho()
        hotkey("ctrl", "c", interval=0.2)
        natureza_perc = paste() 
        if natureza_perc != "0,00":
            lista_perc = []
            while round(sum(lista_perc),2) < 100.0:
                natureza_perc = utils.formatador3(natureza_perc)
                lista_perc.append(natureza_perc)
                utils.descerECopiar()
                natureza_perc = paste() 
            maior_perc = max(lista_perc)
            natureza_duplicata_clique = utils.encontrarImagemLocalizada(r'Imagens\naturezaDuplicata.png')
            x, y = natureza_duplicata_clique
            mouseClique(x,y)
            press("up")
            sleep(0.2)
            hotkey("ctrl", "c", interval=0.1)
            perc_majoritario = paste()
            perc_majoritario = utils.formatador3(perc_majoritario)
            while perc_majoritario != maior_perc:
                utils.descerECopiar()
                perc_majoritario = paste()
                perc_majoritario = utils.formatador3(perc_majoritario)
            press("left")
            hotkey("ctrl", "c", interval=0.1)
            natureza_duplicata = paste()
            hotkey(["shift", "tab"]*5, interval=0.2)
            write(natureza_duplicata)
            press("tab")
            sleep(1)


        salvar = utils.encontrarImagemLocalizada(r'Imagens\salvarLancamento.png')
        salvarx, salvary = salvar
        sleep(0.7)
        mouseClique(salvarx,salvary, clicks=2, interval=0.1)
        sleep(2)
        cont = 0
        while True:
            salvar = utils.encontrarImagemLocalizada(r'Imagens\salvarLancamento.png')
            if type(salvar) == tuple:
                mouseClique(salvarx,salvary, clicks=2, interval=0.1)
                cont += 1
                sleep(1)
                if cont == 2:
                    break
            else:
                break
        erro_de_serie = utils.encontrarImagem(r'Imagens\ErroDeSerie.png')
        erro_de_modelo = utils.encontrarImagem(r'Imagens\ErroDeModulo.png')
        if type(erro_de_serie) == pyscreeze.Box or type(erro_de_modelo) == pyscreeze.Box:
            press("enter", interval=0.2) 
            espec_doc = utils.encontrarImagemLocalizada(r'Imagens\CorrigirErroDeSerie.png')
            x, y = espec_doc
            sleep(0.5)
            mouseClique(x,y, clicks=2)
            write("NF", interval=0.1)
            press("enter")
            sleep(0.5)
            mouseClique(salvarx,salvary, clicks=2)
        erro_esquisito = utils.encontrarImagem(r'Imagens\erroEsquisito.png')
        if type(erro_esquisito) == pyscreeze.Box:
            press("esc")
            quit()
        erro_quantidade = utils.encontrarImagem(r'Imagens\erroDeQuantidade.png')
        if type(erro_quantidade) == pyscreeze.Box:
            press("enter")
            utils.cancelarLancamento()
            mudar_a_selecao = utils.encontrarImagemLocalizada(imagem=r'Imagens\mudarASelecao.png')
            x, y = mudar_a_selecao
            mouseClique(x,y, clicks=2)
            sleep(0.3)
            utils.clicarMicrosiga()
            utils.acrescerLista(processo_errado, nao_lancadas, link, mensagem_pe)
            return robozinho()


        cont = 0
        etapa_final = utils.encontrarImagem(r'Imagens\etapaFinal.png')
        while type(etapa_final) != pyscreeze.Box:
            sleep(0.2)
            etapa_final = utils.encontrarImagem(r'Imagens\etapaFinal.png')
        press(["tab"]*3, interval=0.9)
        press("enter")
        sleep(1.5)
        ultimo_enter = utils.encontrarImagem(r'Imagens\finalizarLancamento.png')
        if type(ultimo_enter) != pyscreeze.Box:
            while type(ultimo_enter) != pyscreeze.Box:
                sleep(0.2)
                ultimo_enter = utils.encontrarImagem(r'Imagens\finalizarLancamento.png')
                cont +=1
                if cont == 6:
                    press("enter")
                    cont = 0
        press("tab", interval=0.9)
        press("enter")
        aux = False
        cont2 = 0
        while True:
            ultima_tela = utils.encontrarImagem(r'Imagens\ultimaTela.png')
            if type(ultima_tela) == pyscreeze.Box:
                aux = True
                while type(ultima_tela) == pyscreeze.Box:
                    ultima_tela = utils.encontrarImagem(r'Imagens\ultimaTela.png')
                    sleep(0.2)
            if aux == True:
                break
            ultimo_enter = utils.encontrarImagem(r'Imagens\finalizarLancamento.png')
            if type(ultimo_enter) == pyscreeze.Box:
                cont +=1
                if cont == 4:
                    aux = True
                    ultima_tentativa = utils.encontrarImagemLocalizada(imagem=r'Imagens\ultimaTentativa.png')
                    x, y = ultima_tentativa
                    mouseClique(x,y, clicks=2)
                    moveTo(150, 100)
            if cont2 == 5:
                break
            cont2 +=1
        

        hotkey("win", "d")
        sleep(0.2)


        abortar = False
        return sem_boleto, processo_bloqueado, processo_errado, XML_ilegivel, nao_lancadas, abortar
    except FailSafeException:
        abortar = True
        return sem_boleto, processo_bloqueado, processo_errado, XML_ilegivel, nao_lancadas, abortar

