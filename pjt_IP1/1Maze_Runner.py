import pygame
from pygame.locals import *
from sys import exit
import random

import os
print(os.getcwd())

# início
pygame.init()

# ngm merece jogo sem musica
som_dado = pygame.mixer.Sound("dado.wav")
pygame.mixer.music.set_volume(0.5)
musica_de_fundo = pygame.mixer.music.load('background.mp3') #musica de fundo
pygame.mixer.music.play(-1) #toca a musica de fundo em loop (-1) diz sobre o loop infinito)

# tudo sobre os jogadores
hp = {"P1": 10, "P2": 10} 
pos_jgr = {"P1": 0, "P2": 0} #posicao dos jogadores, ou seja, a casa onde eles estão
ordem_def = False #se a ordem dos jogadores já foi definida, ou seja, se eles já jogaram o dado pra definir quem começa
p_atual = None #jogador atual, ou seja, o jogador que tem a vez de jogar, isso é definido depois que os jogadores jogam o dado pra definir a ordem, o jogador que tirar o número mais alto começa, e se os dois jogadores tirarem o mesmo número no dado, entao a definição dos jogadores é refeita, ou seja, os jogadores jogam o dado de novo até que um dos jogadores tire um número mais alto
resP1 = None #resultado do dado do jogador 1, ou seja, o número que ele tirou no dado
resP2 = None #resultado do dado do jogador 2, ou seja, o número que ele tirou no dado
jogador_preso = {"P1": False, "P2": False} #se ele ta preso (casa amarela)
jogador_extra_turno = {"P1": False, "P2": False} #efeito da casa azul, que o jogador joga dnv
resultado_turno = None 
p_atual_anterior = None
mensagens_de_log= []

def reiniciar_jogo(): #resetar todas as variaveis para poder reiniciar o jogo
    global hp, pos_jgr, ordem_def, p_atual, resP1, resP2
    global jogador_preso, jogador_extra_turno, resultado_turno, p_atual_anterior, mensagens_de_log

    hp = {"P1": 10, "P2": 10}
    pos_jgr = {"P1": 0, "P2": 0}
    ordem_def = False
    p_atual = None
    resP1 = None
    resP2 = None
    jogador_preso = {"P1": False, "P2": False}
    jogador_extra_turno = {"P1": False, "P2": False}
    resultado_turno = None
    p_atual_anterior = None
    mensagens_de_log = []

cores = {"vermelho": (255, 0, 0), "verde": (112, 173, 71),
        "azul": (68, 114, 196), "amarelo": (255, 192, 0),
        "preto": (0, 0, 0),"preto_simples":(20, 20, 20), "cinza":(100, 100, 100), "branco": (255, 255, 255),
        "bege": (245, 245, 220), "cinza_azulado":(67, 82, 107), "dourado":(212, 175, 55),
        "azul_escuro": (10, 25, 50), "azul_claro": (100, 160, 255), "verde_escuro": (10, 40, 20), "verde_claro": (100, 200, 100), "cinza_escuro": (30, 30, 30),
        "azul_petroleo": (20, 40, 60), "marrom_escuro": (50, 30, 10), "verde_musgo":(85, 107, 47), "roxo_escuro": (20, 10, 40), "roxo_medio": (50, 20, 80), 
        "rosa_neon": (255, 0, 128), "cinza_escuro_neutro": (45, 45, 45), "azul_escuro_discreto": (30, 40, 60), "cinza_claro": (180, 180, 180)}

COR_FUNDO = (41, 49, 51)
COR_PAINEL = (35, 40, 43)
COR_BORDA = (77, 63, 50)

largura_painel = 260
largura_tela = 700 + largura_painel
altura_tela = 520

tamanho_quadrado = 60

# nome do jogo

nome_jogo = f'Maze Runner'

# posição dos quadrado inicial
x_quadrado = 50
y_quadrado = 50

# fonte usada no numero e nas palavras "Início" e "Fim"
fonte = pygame.font.SysFont("arial", 12, True, False)

# fontes titulo
fonte_titulo = pygame.font.Font(r"SketchRockwell-Bold.ttf", 25) # é preciso instalar a fonte manualmente no dispositivo, senão, precisará colocar todo o diretório do arquivo

# posição onde será desenhado o texto "Início"
pos_inicio = (x_quadrado + 2, y_quadrado + 2)

# listas que vão guardar as posições dos quadrados e dos números deles
posicoes_quadrados = []
posicoes_numero_quadrado = []

# linha de cima
for i in range(10):
    posicoes_quadrados.append((x_quadrado, y_quadrado))
    posicoes_numero_quadrado.append((x_quadrado + 2, y_quadrado + 2))
    x_quadrado += tamanho_quadrado

x_quadrado -= tamanho_quadrado

# descendo à direita
for i in range(1, 7):
    y_quadrado += tamanho_quadrado
    posicoes_quadrados.append((x_quadrado, y_quadrado))
    posicoes_numero_quadrado.append((x_quadrado + 2, y_quadrado + 2))

# linha de baixo, da direita pra esquerda
for i in range(1, 10):
    x_quadrado -= tamanho_quadrado
    posicoes_quadrados.append((x_quadrado, y_quadrado))
    posicoes_numero_quadrado.append((x_quadrado + 2, y_quadrado + 2))

# subindo à esquerda
for i in range(1, 4):
    y_quadrado -= tamanho_quadrado
    posicoes_quadrados.append((x_quadrado, y_quadrado))
    posicoes_numero_quadrado.append((x_quadrado + 2, y_quadrado + 2))

# posição onde será desenhado o texto "Fim"
pos_fim = (x_quadrado + 2, y_quadrado + 2)

# cores de cada quadrado, em ordem que serão desenhados
casa = [cores["preto"], cores["branco"], cores["vermelho"], cores["verde"], cores["branco"], cores["azul"], cores["branco"], cores["amarelo"], cores["branco"], cores["vermelho"],
        
        cores["verde"], cores["preto"], cores["azul"], cores["branco"], cores["branco"], cores["vermelho"],

        cores["verde"], cores["branco"], cores["amarelo"], cores["branco"], cores["vermelho"], cores["verde"], cores["branco"], cores["azul"], cores["vermelho"],

        cores["amarelo"], cores["verde"], cores["preto"]]

# atribui o texto que será desenhado às variáveis
texto_inicio = "Início"
texto_fim = "Fim"

# gera o texto
inicio = fonte.render(texto_inicio, True, cores["branco"])
fim = fonte.render(texto_fim, True, cores["branco"])

# tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
# nome da aba
pygame.display.set_caption("Maze Runner")

relogio = pygame.time.Clock()


# função q desenha eles como circulos
def desenhar_jogadores():
    # usa as coordenadas da casa atual
    x1, y1 = posicoes_quadrados[pos_jgr["P1"]]
    x2, y2 = posicoes_quadrados[pos_jgr["P2"]]
    # nao podem estar exatamente encima do outro
    if pos_jgr["P1"] == pos_jgr["P2"]:
        # p1 + pra cima
        pygame.draw.circle(tela, (0, 0, 255), (x1 + tamanho_quadrado//2, y1 + tamanho_quadrado//2 - 10), 18)
        tela.blit(fonte.render("P1", True, cores["branco"]), (x1 + tamanho_quadrado//2 - 12, y1 + tamanho_quadrado//2 - 18))
        # p2 + embaixo
        pygame.draw.circle(tela, (255, 0, 0), (x2 + tamanho_quadrado//2, y2 + tamanho_quadrado//2 + 10), 18)
        tela.blit(fonte.render("P2", True, cores["branco"]), (x2 + tamanho_quadrado//2 - 12, y2 + tamanho_quadrado//2 + 2))
    else:
         # círculos normais
        pygame.draw.circle(tela, (0, 0, 255), (x1 + tamanho_quadrado//2, y1 + tamanho_quadrado//2), 20)
        tela.blit(fonte.render("P1", True, cores["branco"]), (x1 + tamanho_quadrado//2 - 12, y1 + tamanho_quadrado//2 - 10))

        pygame.draw.circle(tela, (255, 0, 0), (x2 + tamanho_quadrado//2, y2 + tamanho_quadrado//2), 20)
        tela.blit(fonte.render("P2", True, cores["branco"]), (x2 + tamanho_quadrado//2 - 12, y2 + tamanho_quadrado//2 - 10))

# dado pra definir quase tudo no jogo.
def jogar_dado():
    return random.randint(1, 6)

# função pra mostrar o texto na tela, vai facilitar muito a nossa vida, pq ai nao precisa ficar criando uma fonte nova toda hora pra mostrar um texto diferente, é só chamar essa função passando o texto, a posição e a cor que vc quer
def mostrar_txt(texto , x, y, cor=(0,0,0), tamanho = 20):
    fonte_temp = pygame.font.SysFont("arial", tamanho, True, False)
    render = fonte_temp.render(texto, True, cor)
    tela.blit(render, (x, y))

def desenhar_log(): # def das mensagens de log no painel lateral -m
    x_log = 710
    y_inicio_log = 80
    altura_linha = 18
    max_linhas = 21  # quantas cabem no painel


    # pega só as últimas mensagens que cabem
    msgs_visiveis = mensagens_de_log[-max_linhas:]

    for i, msg in enumerate(msgs_visiveis):
        # alterna cor pra facilitar leitura
        cor = cores["cinza_claro"] if i % 2 == 0 else cores["branco"]
        mostrar_txt(msg, x_log, y_inicio_log + i * altura_linha, cor, 13)

# efeitos das casas
def efeito_casa(jogador):
    indice = pos_jgr[jogador]
    cor_casa = casa[indice]
    # Ignorar início (0) e fim (27)
    if indice == 0 or indice == len(casa) - 1:
        return #a função retorna nada e acaba aqui, pq a inicio e fim são pretas e pode interferir no jogo

    if cor_casa == cores["branco"]:
        pass
    elif cor_casa == cores["vermelho"]:
        hp[jogador] -= 3
        mensagens_de_log.append(f"{jogador} perdeu 3 HP! ({hp[jogador]} restante)")
        pygame.mixer.Sound("som_vermelho.wav").play() # som de grito do Tom (tom e jerry)

    elif cor_casa == cores["verde"]:
        if hp[jogador] == 10:
            pass
            mensagens_de_log.append(f'{jogador} já está com a vida cheia!')
        else:
            hp[jogador] += 1
            mensagens_de_log.append(f"{jogador} ganhou 1 HP! ({hp[jogador]} total)")
            pygame.mixer.Sound("som_verde.wav").play() # som da poção do minecraft

    elif cor_casa == cores["amarelo"]:
        jogador_preso[jogador] = True
        mensagens_de_log.append(f"{jogador} ficou preso!")
        pygame.mixer.Sound("som_amarelo.wav").play() # som de uma cela fechando

    elif cor_casa == cores["azul"]:
        jogador_extra_turno[jogador] = True
        mensagens_de_log.append(f"{jogador} joga de novo!")
        pygame.mixer.Sound("som_azul.wav").play()

    elif cor_casa == cores["preto"]:
        pos_jgr[jogador] = 0  # volta para o inicio
        mensagens_de_log.append(f"{jogador} voltou ao início!")
        pygame.mixer.Sound("som_preto.wav").play() # som do FAHH

def fim_jogo():
    vencedor = None
    # fim por hp(morte)
    if hp["P1"] <=0:
        vencedor = "P2"
    elif hp["P2"] <=0:
        vencedor = "P1"
    # fim por chegar na última casa
    elif pos_jgr["P1"] >= len(casa) - 1:
        vencedor = "P1"
    elif pos_jgr["P2"] >= len(casa) - 1:
        vencedor = "P2"
    if vencedor:
        mostrar_txt(f"VENCEDOR: {vencedor}", 250, 300, cores["bege"], 30)    
        pygame.mixer.Sound("som_vencedor.wav").play() #Som YOU WIN!
        return True  # indica que o jogo acabou
    return False # jogo continua

while True:
    # fps
    relogio.tick(30)

    # cor da tela
    tela.fill(COR_FUNDO)

    pygame.draw.rect(tela, COR_PAINEL, (700, 0, 260, 960))
    pygame.draw.rect(tela, COR_BORDA, (705, 5, 250, 510), 4)
    pygame.draw.rect(tela, COR_BORDA, (5, 5, 690, 510), 4)
    texto_formatado = fonte_titulo.render(nome_jogo, True, cores['branco'])
    tela.blit(texto_formatado, (743, 30))



    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        if evento.type == KEYDOWN:
            # Jogador 1(p1) usa SPACE
            if evento.key == K_SPACE and not ordem_def:
                if resP1 is None:  # primeira vez que P1 rola
                    som_dado.play() 
                    resP1 = jogar_dado()

            # Jogador 2(p2) usa  ENTER
            if evento.key == K_RETURN and not ordem_def:
                if resP2 is None:  #primeira vez que P2 rola
                    som_dado.play()
                    resP2 = jogar_dado()

            # confirmar ordem só quando apertar TAB, para os jogadores terem tempo de ver o resultado do dado, e só se a ordem ainda não tiver sido definida, ou seja, se os jogadores ainda não tiverem confirmado a ordem
            if evento.key == K_TAB and not ordem_def:
                if resP1 is not None and resP2 is not None:
                    if resP1 > resP2:
                        p_atual = "P1" # p1 começa
                        ordem_def = True
                    elif resP2 > resP1:
                        p_atual = "P2" # p2 começa
                        ordem_def = True
                    else:
                        # empate: mostrar mensagem e resetar para nova rodada
                        resP1, resP2 = None, None
            # depois da ordem definida esse if define a movimentação a cada rodada.
            if evento.type == KEYDOWN and ordem_def:
                if (evento.key == K_SPACE and p_atual == "P1") or (evento.key == K_RETURN and p_atual == "P2"): # se o evento for espaço ou enter e a ordem tiver correta, entra dentro desse if. isso garante que um jogador não jogue dentro da rodada do outro.
                    if jogador_preso[p_atual]: # verifica se o jogador atual tá preso
                        mensagens_de_log.append(f"{p_atual} está preso e perdeu a vez!") # se estiver preso registra no log
                        jogador_preso[p_atual] = False # seta false novamente
                        p_atual = "P1" if p_atual == "P2" else "P2" # reseta
                    else: # caso não esteja segue o rumo normal
                        som_dado.play()
                        resultado_turno = jogar_dado() # resultado do turno do jogador que estiver com a vez
                        p_atual_anterior = p_atual # guardar a informação em outra variavel para mostrar depois
                        pos_jgr[p_atual] = min(pos_jgr[p_atual] + resultado_turno, len(casa) - 1) # atualiza a movimentação do jogador mais não deixar ultrapassar a ultima casa com o min(). 
                        mensagens_de_log.append(f"{p_atual} tirou {resultado_turno}") # log
                        efeito_casa(p_atual) # executa o efeito da casa que o jogador caiu

                        if jogador_extra_turno[p_atual]: # referente a casa azul
                            jogador_extra_turno[p_atual] = False

                        else: # outros tipos de casa
                            p_atual = "P1" if p_atual == "P2" else "P2" 

    # desenha os quadrados
    for i in range(len(posicoes_quadrados)):
        pygame.draw.rect(tela, casa[i], (posicoes_quadrados[i][0], posicoes_quadrados[i][1], tamanho_quadrado, tamanho_quadrado))
        # desenha os contornos
        pygame.draw.rect(tela, cores["preto"], (posicoes_quadrados[i][0], posicoes_quadrados[i][1], tamanho_quadrado, tamanho_quadrado), 1)

        # desenha os número das casas ignorando a primeira e a última
        if 0 < i < 27:
            numero = f"{i}"

            # quando a casa não for preta, o texto será preto
            if casa[i] != cores["preto"]:
                numeracao = fonte.render(numero, True, cores["preto"])
                tela.blit(numeracao, (posicoes_numero_quadrado[i][0], posicoes_numero_quadrado[i][1]))
            
            # quando a casa for preta, o texto será branco
            else:
                numeracao = fonte.render(numero, True, cores["branco"])
                tela.blit(numeracao, (posicoes_numero_quadrado[i][0], posicoes_numero_quadrado[i][1]))
                numeracao = fonte.render(numero, True, cores["preto"])
    
    # desenha os textos "Início" e "Fim" no primeiro e último quadrado
    tela.blit(inicio, (pos_inicio[0], pos_inicio[1]))
    tela.blit(fim, (pos_fim[0], pos_fim[1]))

    desenhar_jogadores()
    desenhar_log()
    # uns texto pra definição dos jogadores e pra mostrar o turno atual, ou seja, qual jogador tem a vez de jogar, e também pra mostrar o resultado do dado de cada jogador, ou seja, o número que eles tiraram no dado, e também pra mostrar quem ganhou a definição dos jogadores e começa jogando primeiro, ou seja, o jogador que tirou o número mais alto no dado, e se os dois jogadores tirarem o mesmo número no dado, entao a definição dos jogadores é refeita, ou seja, os jogadores jogam o dado de novo até que um dos jogadores tire um número mais alto
    # mostrar mensagens na tela
    if not ordem_def:
        mostrar_txt("Controle dos jogadores", 210, 150, cores["bege"], 24)
        mostrar_txt("P1 (SPACE)         P2 (ENTER)", 200, 190, cores["bege"], 22)

        if resP1 is not None:
            mostrar_txt(f"P1 tirou {resP1}", 250, 240, cores["bege"], 22)
        if resP2 is not None:
            mostrar_txt(f"P2 tirou {resP2}", 250, 270, cores["bege"], 22)
        if resP1 == resP2 and resP1 is not None and resP2 is not None:
            mostrar_txt("Empate! Rolem o dado novamente.", 200, 320, cores["bege"], 22)
        if resP1 is not None and resP2 is not None:
            mostrar_txt("Aperte TAB", 200, 350, cores["bege"], 22)
    else: 
        mostrar_txt(f"Turno atual: {p_atual}", 250, 200, cores["bege"], 22)
        mostrar_txt(f"HP P1: {hp['P1']}   HP P2: {hp['P2']}", 250, 240, cores["bege"], 20)
        if resultado_turno is not None: # mostra quanto cada p tirou em cada rodada.
            mostrar_txt(f"{p_atual_anterior} tirou {resultado_turno}", 250, 270, cores["bege"], 20)

    # Verifica se o jogo terminou
    if fim_jogo():
        pygame.display.update()
        pygame.time.delay(3000)  # pausa para mostrar o vencedor
        esperando = True
        while esperando:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit()
                    exit()
                if ev.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # verifica se clicou dentro do botão (retângulo 300x50 centralizado)
                    if 712 <= x <= 948 and 455 <= y <= 505: # intervalo onde pode ser clicado
                        reiniciar_jogo()
                        esperando = False

            # desenha o botão
            pygame.draw.rect(tela, cores["verde"], (712, 455, 236, 50))
            mostrar_txt("JOGAR DE NOVO", 737, 468, cores["branco"], 22)
            pygame.draw.rect(tela, cores["branco"], (712, 455, 236, 50), 5)
            pygame.display.update()
            relogio.tick(30)

    # atualização da aba
    pygame.display.update()
