##########################################################
################ Python Version: 3.12.3 ##################
##########################################################

## ----------- Bibliotecas ------------- ##
import time
import random
from utilidades import *


## --------------- Apresentação ------------------- ##

limpar_tela()
exibir_menu_inicial(cores, submarino, deep_sea, historia, regras)



## ------------ Configurações do jogo ------------- ##

## Cadastro dos jogadores ##
cadastrar_jogadores(cores, assets_jogo, submarino, deep_sea)
limpar_tela()
exibir_cabecalho(cores, submarino, deep_sea)

## Escolha do mapa, quantidade de tanquues de oxigenio e profundidade do mapa ##
assets_jogo["profundidade_mapa"] = escolher_mapa(cores)
assets_jogo["oxigenio"] = escolher_oxigenio(cores)

## -------------- Tela pré-jogo ---------------- ##

## Exibição de informações ##
limpar_tela()
exibir_cabecalho(cores, submarino, deep_sea)
print("^" * 45)
print(f"""{cores["amarelo"]}| ### Informações do jogo ###
| Tanques de oxigenio: {assets_jogo["oxigenio"]}.
| Quantidade de players: {assets_jogo["num_de_jogadores"]}.
| Players: {", ".join(assets_jogo["nomes_jogadores"])}
| Profundidade do mapa: {assets_jogo["profundidade_mapa"]} metros.{cores["reset_cor"]}""")
print("-" * 45)
time.sleep(2)

## Opção de iniciar o jogo ##
comecar = str(input(f'{cores["amarelo"]}Pressione enter para começar o jogo ou digite "Sair" para cancelar: {cores["reset_cor"]}')).upper()
match comecar:
        case 'SAIR':
            reiniciar_programa()
        
        case '': # Enter (falsy value)
            time.sleep(1)
            
        case _: # Digitou outra coisa
            while comecar != 'SAIR' and comecar:
                comecar = str(input(f'{cores["amarelo"]}Pressione enter para começar o jogo ou digite "Sair" para cancelar: {cores["reset_cor"]}')).upper()
                
            if not comecar:
                time.sleep(1)
        
            else:
                reiniciar_programa()


## ------------ Jogo principal -------------- ##

## Condição de parada/fim do jogo ##
while assets_jogo["oxigenio"] > 0:

## Loop das rodadas do jogo, onde cada player joga uma vez. Ao fim de cada rodada, o programa volta para o while e verifica a condição de parada. ##
    for jogador in range(assets_jogo["num_de_jogadores"]):
        
        if assets_jogo["oxigenio"] <= 0: # Verifica a cada loop do for se o oxigenio acabou, evitando assim que o jogo continua caso o oxigenio acabe antes do fim de uma rodada
            break
        
        limpar_tela()
        time.sleep(1.0)
        
        ## Reseta as variaveis a cada loop ##
        pegar_tesouro = ''
        voltar_jogador = ''
        total_tesouros = assets_jogo["tesouros_com_o_jogador"][jogador] + assets_jogo["submarino_tesouros"][jogador]
        
        if assets_jogo["voltar_ao_submarino"][jogador] == 'N':
            
            situacao_jogador = 'Mergulhando'
            exibir_informacoes(cores, submarino, deep_sea, assets_jogo, jogador, total_tesouros, situacao_jogador)
            assets_jogo["distancia_sorteada"] = random.randint(0, 3)
            assets_jogo["posicoes"][jogador] += assets_jogo["distancia_sorteada"]
            print(f'Número sorteado: {assets_jogo["distancia_sorteada"]}. Você desceu {assets_jogo["distancia_sorteada"]}m no fundo do mar.')
            print(f'Sua nova posição: {assets_jogo["posicoes"][jogador]}m de profundidade. {cores["reset_cor"]}')
            print('-' * 45)

            # Capturar tesouro
            while pegar_tesouro not in assets_jogo["SimOuNao"]:
                pegar_tesouro = str(input(f'{cores["amarelo"]}Deseja pegar o tesouro que está na posição {assets_jogo["posicoes"][jogador]}? Sim ou Não: {cores["reset_cor"]}')).upper()

            if pegar_tesouro in ['SIM', 'S']:
                
                
                if assets_jogo["posicoes"][jogador] not in assets_jogo["tesouros_capturados"]:
                    assets_jogo["valor_tesouro"] = calcular_valor_tesouro(assets_jogo, jogador)
                    assets_jogo["tesouros_com_o_jogador"][jogador] += assets_jogo["valor_tesouro"]
                    tesouros_jogador = assets_jogo["tesouros_com_o_jogador"][jogador]
                    oxigenio_consumido = tesouros_jogador + 1
                    assets_jogo["oxigenio"] -= oxigenio_consumido
                    print('-' * 45)
                    print(f'{cores["verde"]}Valor do tesouro capturado: {assets_jogo["valor_tesouro"]} KG.{cores["reset_cor"]}')
                    assets_jogo["tesouros_capturados"].append(assets_jogo["posicoes"][jogador])
                    
                    
                else:
                    tesouros_jogador = assets_jogo["tesouros_com_o_jogador"][jogador]
                    oxigenio_consumido = tesouros_jogador + 1
                    assets_jogo["oxigenio"] -= oxigenio_consumido
                    print(f'-' * 45)
                    print(f'{cores["verde"]}Esse tesouro já foi capturado, Por isso você não pode captura-lo.')
                    print(f'{cores["reset_cor"]}-' * 45)
                    
            else: # Optou por não pegar o tesouro  
                
                tesouros_jogador = assets_jogo["tesouros_com_o_jogador"][jogador]
                oxigenio_consumido = tesouros_jogador + 1
                assets_jogo["oxigenio"] -= oxigenio_consumido
                print('-' * 45)
                print(f'{cores["verde"]}Você optou por não pegar tesouros.')
                print(f'{cores["reset_cor"]}-' * 45)
                
            # Voltar ao submarino
            voltar_jogador = ''
            while voltar_jogador not in assets_jogo["SimOuNao"]:
                voltar_jogador = str(input(f'{cores["amarelo"]}Deseja começar a voltar ao submarino? Sim ou Não: {cores["reset_cor"]}')).upper()
                
            if voltar_jogador in ['SIM', 'S']:
                assets_jogo["voltar_ao_submarino"][jogador] = 'S'
                
        elif assets_jogo["voltar_ao_submarino"][jogador] == 'S' and assets_jogo["posicoes"][jogador] > 0: # Jogador já está com a flag que indica que ele está voltando ao submarino
            situacao_jogador = 'Emergindo'
            assets_jogo["distancia_sorteada"] = random.randint(1, 3)
            exibir_informacoes(cores, submarino, deep_sea, assets_jogo, jogador, total_tesouros, situacao_jogador)
            assets_jogo["posicoes"][jogador] -= assets_jogo["distancia_sorteada"]
            
            if assets_jogo["posicoes"][jogador] <= 0: # Feito para evitar que o jogador fique em posições negativas
                assets_jogo["posicoes"][jogador] = 0
                
            
            
            print(f'{cores["verde"]}Número sorteado: {assets_jogo["distancia_sorteada"]}. Você subiu {assets_jogo["distancia_sorteada"]}m em direção ao submarino.')
            print(f'Sua nova posição: {assets_jogo["posicoes"][jogador]}m de profundidade{cores["reset_cor"]}')
            print('-' * 45)
            input(f'{cores["amarelo"]}Pressione enter para continuar: {cores["reset_cor"]}')

            # Jogador chegou ao submarino
            if assets_jogo["posicoes"][jogador] == 0:
                
                assets_jogo["submarino_tesouros"][jogador] += assets_jogo["tesouros_com_o_jogador"][jogador]
                print(f'{cores["verde"]}Você chegou ao submarino!')
                voltar_a_descer = "" # Reseta a flag
                
                while voltar_a_descer not in assets_jogo["SimOuNao"]:
                    voltar_a_descer = str(input(f'{cores["amarelo"]}Seus tesouros foram depositados no submarino! Deseja voltar a descer no mar? (Sim ou Não): ')).upper()
                    
                if voltar_a_descer in ['SIM', 'S']:
                    assets_jogo["voltar_ao_submarino"][jogador] = 'N'
                    
            assets_jogo["oxigenio"] -= (assets_jogo["tesouros_com_o_jogador"][jogador] + 1)
            
        else:   # Jogador está no submarino
            situacao_jogador = 'Emergindo'
                
            exibir_informacoes(cores, submarino, deep_sea, assets_jogo, jogador, total_tesouros, situacao_jogador)
            print(f'{cores["reset_cor"]}-' * 45)
            print(f'{cores["verde"]}Você está no submarino!{cores["reset_cor"]}')
            input(f'{cores["amarelo"]}Pressione enter para continuar: {cores["reset_cor"]}')
            voltar_a_descer = "" # Reseta a flag
            
            while voltar_a_descer not in assets_jogo["SimOuNao"]:
                voltar_a_descer = str(input(f'{cores["amarelo"]}Seus tesouros estão depositados no submarino! Deseja voltar a descer no mar? (Sim ou Não): {cores["reset_cor"]}')).upper()
                
            if voltar_a_descer in ['SIM', 'S']:
                assets_jogo["voltar_ao_submarino"][jogador] = 'N'
                
            assets_jogo["oxigenio"] -= (assets_jogo["tesouros_com_o_jogador"][jogador] + 1)
            
# Oxigenio acabou            

limpar_tela()
exibir_cabecalho(cores, submarino, deep_sea)
print("^" * 45)
print(f'{cores["amarelo"]}Os tanques de oxigênio se acabaram. O jogo acabou.{cores["reset_cor"]}')
print("-" * 45)
time.sleep(2)
vencedores = retornar_vencedores(assets_jogo)

if len(vencedores) == 0:
    print(f'{cores["verde"]}Sem vencedores, todos os jogadores morreram antes de chegar ao submarino.')
elif len(vencedores) == 1:
    print(f'{cores["verde"]}O vencedor é: {cores["roxo"]}{vencedores[0]}')
else:
    print(f'{cores["verde"]}Os vencedores são: {cores["roxo"]}{", ".join(vencedores)}!')
    
time.sleep(1.5)
input(f'{cores["amarelo"]}Pressione enter para voltar ao menu principal: {cores["reset_cor"]}')
reiniciar_programa()
