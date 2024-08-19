from pyautogui import hotkey, press, write, FAILSAFE, FailSafeException
from pyperclip import paste
from time import sleep
from selenium import webdriver                         
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import utils
import pyscreeze
         

FAILSAFE = False

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
    options.add_argument(r'user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data\Perfil Selenium')
    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico, options=options)
    driver.get(link)
    utils.checarFailsafe()
        
        
    sleep(2)
    press(["tab"]*3)
    write("bot.contabil")
    press("tab")
    write("EQSeng852@")
    press("enter")
    sleep(2)
    hotkey("alt", "tab", interval=0.1)
    hotkey("ctrl", "w")
    hotkey("alt", "tab", interval=0.1)
    sleep(7)
    utils.checarFailsafe()

