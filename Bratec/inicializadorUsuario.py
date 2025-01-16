from pyautogui import hotkey, FAILSAFE, FailSafeException
from pyperclip import paste
from time import sleep
from selenium import webdriver                         
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import utils
import pyscreeze
         

FAILSAFE = True

def inicializarUsuario():
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
    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico, options=options)
    driver.get(link)
    utils.checarFailsafe()
        
        
    sleep(2)
    try:
        usuario = driver.find_element(By.XPATH, '/html/body/app-root/app-login/po-page-login/po-page-background/div/div/div[2]/div/form/div/div[1]/div[1]/po-login/po-field-container/div/div[2]/input')
        usuario.send_keys("bot.contabil")
    except:
        driver.quit()
        sleep(1)
        hotkey("ctrl", "w")
        raise FailSafeException
    senha = driver.find_element(By.XPATH, '/html/body/app-root/app-login/po-page-login/po-page-background/div/div/div[2]/div/form/div/div[2]/div[1]/po-password/po-field-container/div/div[2]/input')
    senha.send_keys("EQSeng852@")
    logar = driver.find_element(By.XPATH, '/html/body/app-root/app-login/po-page-login/po-page-background/div/div/div[2]/div/form/div/po-button/button')
    logar.click()
    sleep(2)
    hotkey("alt", "tab", interval=0.1)
    hotkey("ctrl", "w")
    hotkey("alt", "tab", interval=0.1)
    while True:
        try:
            abriu = driver.find_element(By.XPATH, '/html/body/app-root/app-main/div/po-toolbar/div/div[2]/po-toolbar-profile/div/po-avatar/div/po-icon')
            break
        except:
            sleep(1)
    utils.checarFailsafe()

