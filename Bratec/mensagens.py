from tkinter import messagebox

class Mensagens:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()

        self.info = "Bem-vindo ao Bot.Contabil!"
        self.texto = """A seguir, você verá a nossa interface de controle da automação, nela temos indicadores de resultados e alguns botões de controle bem intuitivos. Passarei uma breve explicação do que cada um faz. 

Botão Inicializar Usuário: Esse botão serve para que o bot possa logar no portal de compras da EQS, - Devido ao servidor trabalhar sempre no limite da capacidade necessária que a empresa demanda, essa etapa pode enfrentar instabilidade e não atingir o resultado esperado de começo. Para garantir um bom funcionamento, execute essa função 2x, primeiro aperte uma e deixe execultar, quando finalizado, aperte novamente para execultar outra vez -.
 
Botão "Play": Esse botão é o que ativa o Bot, ele só precisa ser acionado 1x, e quando acionado, tire as mãos do mouse e do teclado e deixe a mágica acontecer.
 
Os demais botões servem apenas para abrir os processos que representam."""

        self.info2 = "Fiscal IO"
        self.texto2 = """Ao lado do bot temos a plataforma Fiscal IO. Nela você baixa todos os XMLs necessários para que o bot realize os lançamentos.

Vou deixer um breve manual de como baixar os XMLs nessa plataforma."""

        self.texto3 = """Cuidado!
Isso não é o e-commerce da Koerich, não vá apertar todos os botões ao mesmo tempo, apenas um por vez!"""


        self.info4 = "Como operar"
        self.texto4 = """Modo de operar:
 
Abra o Microsiga e logue no usuário bot.contabil (Usuário: bot.contabil, Senha: EQSeng852@);
Em seguida, vá para a rotina "Processo Pagamento" no módulo Compras; faça o filtro que desejar, mas, atente-se para o tipo de nota fiscal que será lançada, o bot só realiza os lançamentos de mercadoria!
 
Aberta a rotina, clique em "Ver Documentos", isso abrirá o portal de compras da EQS; faça o login (esse processo sofre daquela instabilidade mencionada anteriormente, pode ser necessário logar 2x no portal, por via das duvidas, clique em "Ver Documentos" novamente e veja se abre o processo). Feito isso, agora é só inicializar o bot realizando o processo do botão "Inicializar Usuário"; quando concluído, basta dar o play e deixar acontecer!
 
Para interromper ou finalizar a execução do bot, basta levar o cursor do mouse até o limite do canto superior esquerdo da sua tela e aguardar 10 segundos. Não é preciso fechar a janela do bot, aliás, oriento que a fechem somente no fim do expediente ou quando não quiserem mais acionar o bot, mas o bot pode ser interrompido e reacionado quantas vezes for necessário apenas clicando no botão "Play".
Se a tela do bot estiver preta, mantenha o cursor no canto extremo do monitor e aguarde mais um pouco.
"""

        self.info5 = "Atenção!"
        self.texto5 = """Atenção!

Como mencionado anteriormente, nosso servidor está sempre sobrecarregado, o que pode gerar instabilidade no bot durante sua execução, fazendo-o "crachar" e não conseguir lançar mais nenhum processo. Se acaso perceber algum desses momentos de instabilidade do servidor, verifique se o bot continua execultando seus lançamentos ou se está travado em alguma tela. Se estiver travado, realize o procedimento de interrupção, depois inicialize o usuario novamente e então reacione o robô. Devido alguns momentos de instabilidade serem imperceptiveis, aconcelho que verifique o monitor do bot no mínimo 1x a cada duas horas."""


    def mostrarInfo(self, info, texto):
        messagebox.showinfo(info, texto)

    def mostrarAviso(self, info, texto):
        messagebox.showwarning(info, texto)

    def mostrarErro(self, texto):
        messagebox.showerror("Cuidado!", texto)
