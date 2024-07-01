## ----------- Bibliotecas ------------- ##
import os
import sys
import time


## --------------- Informações do jogo --------------- ##
assets_jogo = {
    "valor_tesouro": 0,
    "nomes_jogadores": [],
    "oxigenio": 0,
    "distancia_sorteada": 0,
    "SimOuNao": ('S', 'N', 'SIM', 'NAO', 'NÃO'),
    "profundidade_mapa": 0,
    "tesouros_capturados": [], #Blocklist
}



## ------ Constantes de cores para personalização do terminal ------ ##

cores = {
    "azul_claro": '\033[1;34m',
    "verde_agua": '\033[1;36m',
    "amarelo": '\033[1;33m',
    "roxo": '\033[1;35m',
    "verde": '\033[1;32m',
    "reset_cor": '\033[0m'
}


## -------------------- Artes ASCII ------------------------ ##

submarino =r"""    
                     '.|                                 
     _-   _-    _-  _-||    _-    _-  _-   _-    _-    _-
       _-    _-   - __||___    _-       _-    _-    _-   
    _-   _-    _-  |   _   |       _-   _-    _-         
      _-    _-    /_) (_) (_\        _-    _-       _-   
              _.-'           `-._      ________       _- 
        _..--`                   `-..'       .'          
    _.-'  o/o                     o/o`-..__.'        ~  ~
 .-'      o|o                     o|o      `.._.  // ~  ~
 `-._     o|o                     o|o        |||<|||~  ~ 
     `-.__o\o                     o|o       .'-'  \\ ~  ~
          `-.______________________\_...-``'.       ~  ~ 
                                    `._______`.          """
                                    
                                    
deep_sea = r"""
________                           _________              
\______ \   ____   ____ ______    /   _____/ ____ _____   
 |    |  \_/ __ \_/ __ \\____ \   \_____  \_/ __ \\__  \  
 |    `   \  ___/\  ___/|  |_> >  /        \  ___/ / __ \_
/_______  /\___  >\___  >   __/  /_______  /\___  >____  /
        \/     \/     \/|__|             \/     \/     \/ 
       
        """
        
        
## -------------- Textos utilizados no programa ------------------ ##

historia = 'Um grupo de pobres exploradores com a esperança de ficarem ricos dirigem-se rapidamente para recuperar tesouros de algumas ruínas submarinas.\nEles são todos rivais, mas seus orçamentos forçam-os a compartilhar um único submarino alugado.\nNo submarino alugado, todos eles têm de compartilhar um único tanque de ar.\nSe eles não voltarem para o submarino antes de ficar sem ar, eles soltarão todo o seu tesouro.\nAgora é hora de ver quem pode trazer para casa os maiores riquezas.'
regras = """
1. O jogo deve ser jogado entre 4 e 6 pessoas.
2. O mapa (de 15, 30 ou 45 metros) e a quantidade de tanques de oxigenio (45 ou 120) são escolhidos pelo(s) jogador(res).
3. O jogo segue até que o oxigenio chegue a 0.
3. A cada rodada, cada player recebera um número aleatório que representara a distancia a ser percorrida no mapa.
4. Cada posição do mapa tem um unico tesouro e o valor do tesouro é medido em kg. Cada tesouro tem seu valor defenido pela parte do
mapa em que ele se encontra, a cada 1/3 de profundidade do mapa o tesouro que iniciamente tem o valor 1 dobra de valor.
6. Os tanques de oxigenios são compartilhados entre todos os jogadores.
7. O consumo de oxigenio por rodada excede em 1 unidade o peso dos tesouros que o jogador está carregando.
8. A cada rodada, o jogador pode optar por pegar ou não pegar o tesouro.
9. Um tesouro em uma posição pode ser capturado apenas uma vez. Após isso essa posição fica sem tesouros.
10. A cada rodada, o jogador pode optar por começar a subir de volta ao submarino ou continuar descendo.
11. Para vencer o jogo, o jogador deve ter a maior quantidade de tesouros e estar no submarino ao fim do oxigenio.
"""


## ---------------- Funções para a aparencia e apresentação do jogo) --------------------- ##

def exibir_cabecalho(cores: dict, submarino: str, deep_sea: str, ) -> None:
    # Cabeçalho com o submarino e a logo deep sea.
    print(f'{cores["verde_agua"]}{submarino}')
    print(f'{cores["roxo"]}{deep_sea}{cores["reset_cor"]}')
    

def limpar_tela() -> None:
    # Limpa a tela do console, de acordo com o sistema operacional.
    os.system('cls' if os.name == 'nt' else 'clear')
    

def reiniciar_programa() -> None:
    # Reinicia o programa.
    limpar_tela()
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
    
def exibir_menu_inicial(cores: dict, submarino: str, deep_sea: str, historia: str, regras: str) -> None:
    # Menu inicial do jogo e ponte entre as opções
    exibir_cabecalho(cores, submarino, deep_sea)
    print('^' * 60)
    print(f'{cores["amarelo"]}Bem vindo ao fantástico jogo de exploração oceânica em linha de comando!')
    print(""" 
        [1] História (Veja a história do jogo)
        [2] Regras e como jogar
        [3] Jogar
        [4] Sair (Fechar o jogo)
        """)
    print(f'{cores["reset_cor"]}-' * 61)
    escolher_opcao(cores, historia, submarino, deep_sea, regras)
    
def exibir_informacoes(cores: dict, submarino: str, deep_sea: str, assets_jogo: dict, jogador: int, total_tesouros: int, situacao_jogador: str) -> None:
    # Exibe informações do jogo a cada rodada
    exibir_cabecalho(cores, submarino, deep_sea)
    print("^" * 45)
    print(f'{cores["verde_agua"]}Vez do player: {assets_jogo["nomes_jogadores"][jogador]}.')
    print(f'Oxigênio total: {assets_jogo["oxigenio"]} tanques.')
    print(f'Seus valor total de tesouros: {total_tesouros}kg.')
    print(f'Sua posição atual: {assets_jogo["posicoes"][jogador]}m de profundidade.')
    print(f'Sua situação atual: {situacao_jogador}.{cores["reset_cor"]}')
    print("-" * 45)
    print(f'{cores["verde"]}Sorteando seu número...')
    time.sleep(2)


##-------------------Funções do jogo----------------##

def cadastrar_jogadores(cores: dict, assets_jogo: dict, submarino: str, deep_sea: str):
    
    while True:
        limpar_tela()
        exibir_cabecalho(cores, submarino, deep_sea)
        num_de_jogadores = input(f'{cores["amarelo"]}Insira a quantidade de jogadores (Mínimo de 4 e máximo de 6.): {cores["reset_cor"]}')
        
        if num_de_jogadores.isdigit():
            num_de_jogadores = int(num_de_jogadores)
            
            if num_de_jogadores in {4, 5, 6}:
                limpar_tela()
                break

    exibir_cabecalho(cores, submarino, deep_sea)
    assets_jogo.update({
        "num_de_jogadores": num_de_jogadores,
        "voltar_ao_submarino": ['N'] * num_de_jogadores,
        "tesouros_com_o_jogador": [0] * num_de_jogadores,
        "posicoes": [0] * num_de_jogadores,
        "submarino_tesouros": [0] * num_de_jogadores
    })
    assets_jogo["nomes_jogadores"] = obter_nomes_jogadores(assets_jogo, cores)

def escolher_opcao(cores: dict, historia: str, submarino: str, deep_sea: str, regras: str) -> None:
    # Opção para o usuário escolher uma opção do menu inicial
    escolha = str(input(f'{cores["amarelo"]}Por favor, selecione uma opção (1, 2, 3 ou 4).: {cores["reset_cor"]}'))
    match escolha:
        case '1': # História
            print('^' * 60)
            print(f'{cores["verde"]}{historia}{cores["reset_cor"]}')
            print('^'* 60)
            input(f'{cores["amarelo"]}Pressione enter para voltar ao menu inicial: {cores["reset_cor"]}')
            limpar_tela()
            exibir_menu_inicial(cores, submarino, deep_sea, historia, regras)
            
        case '2': # Regras e como jogar
           
            print('^' * 60)
            print(f'{cores["verde"]}{historia}{cores["reset_cor"]}')
            print('^' * 60)
            input(f'{cores["amarelo"]}Pressione enter para voltar ao menu inicial: {cores["reset_cor"]}')
            limpar_tela()
            exibir_menu_inicial(cores, submarino, deep_sea, historia, regras)
            
            
        case '3': # Jogar
            time.sleep(1)
            limpar_tela()
            exibir_cabecalho(cores, submarino, deep_sea)
            
        case '4': #Sair 
            sys.exit()
            
        case _: # Entrada inválida
            limpar_tela()
            exibir_menu_inicial(cores, submarino, deep_sea, historia, regras)


def escolher_mapa(cores: dict) -> int:
    # Escolha do mapa pelo usuário antes de começar o jogo.
    print('^' * 45)
    print(f'{cores["amarelo"]}Selecione um mapa para iniciar o jogo.')
    print('Mapas disponíveis: ')
    print(f'[1] 15 Metros\n[2] 30 Metros\n[3] 45 Metros{cores["reset_cor"]}')
    print(f'-' * 45)
    mapa_escolhido = 0
    while mapa_escolhido not in ['1', '2', '3']:
        mapa_escolhido = str(input(f'{cores["amarelo"]}Escolha um mapa: (1, 2 ou 3): {cores["reset_cor"]}'))
        
    else: 
        profundidade_mapa = int(mapa_escolhido) * 15
    return profundidade_mapa


def escolher_oxigenio(cores: dict) -> int:
    # Escolha do oxigenio pelo usuário antes de começar o jogo.
    oxigenio = 0
    while oxigenio not in [45, 120]:
        oxigenio = input(f'{cores["amarelo"]}Selecione a quantidade de tanques de oxigênio inicial dessa partida (45 a 120): {cores["reset_cor"]}')
        if oxigenio.isdigit():
            oxigenio = int(oxigenio)
            if oxigenio in [45, 120]:
                return oxigenio



def obter_nomes_jogadores(assets_jogo: dict, cores: dict) -> list:
    # Obtém o nome dos 4 johadores obrigatórios para iniciar o jogo
    nomes = []
    for i in range(assets_jogo["num_de_jogadores"]):
        
        jogador_novo = ""
        while not jogador_novo:
            jogador_novo = str(input(f'{cores["amarelo"]}Por favor, insira o nome do player {i + 1}: {cores["reset_cor"]}'))
        nomes.append(jogador_novo)
    return nomes



def calcular_valor_tesouro(assets_jogo: dict, jogador: int) -> int:
    # Retorna o valor do tesouro no mapa, é usada apenas quando o jogador opta por capturar um tesouro.
    if assets_jogo["posicoes"][jogador] < assets_jogo["profundidade_mapa"] * (1/3):
        return 1
    elif assets_jogo["posicoes"][jogador] < assets_jogo["profundidade_mapa"] * (2/3):
        return 2
    else: # 3/3
        return 4


def retornar_vencedores(assets_jogo: dict) -> list:
    # Função para definir os vencedores, retorna uma lista com o nome dos vencedores
    vencedores = []
    tesouros = assets_jogo["submarino_tesouros"]
    max_tesouros = max(assets_jogo["submarino_tesouros"])
    for i, tesouros in enumerate(assets_jogo["submarino_tesouros"]):
        if tesouros == max_tesouros and assets_jogo["posicoes"][i] == 0:
            vencedores.append(assets_jogo["nomes_jogadores"][i])
    return vencedores
