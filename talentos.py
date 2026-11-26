import random
import pygame

# ---------------------------------------------------------------
# DADOS: raridades e talentos
# ---------------------------------------------------------------
# "cor"        = cor da borda das cartas (fundo escuro)
# "cor_escura" = versão mais escura, para ler no painel creme
# "peso"       = chance relativa de sair (quanto maior, mais comum)
RARIDADES = {
    "Comum":    {"cor": (140, 133, 119), "cor_escura": (110, 104, 92),  "peso": 50},
    "Incomum":  {"cor": (60, 200, 120),  "cor_escura": (30, 130, 75),   "peso": 30},
    "Raro":     {"cor": (170, 100, 255), "cor_escura": (120, 60, 200),  "peso": 15},
    "Lendário": {"cor": (255, 190, 60),  "cor_escura": (170, 105, 10),  "peso": 5},
}

# "bonus" = (mínimo, máximo) de % de Qi a mais
TALENTOS = [
    {"nome": "Dom Inato",                 "chines": "天赋",  "raridade": "Comum",    "bonus": (3, 6)},
    {"nome": "Compreensão",               "chines": "悟性",  "raridade": "Comum",    "bonus": (3, 6)},
    {"nome": "Raiz da Sabedoria",         "chines": "慧根",  "raridade": "Comum",    "bonus": (4, 7)},
    {"nome": "Sentido Divino",            "chines": "神识",  "raridade": "Incomum",  "bonus": (6, 10)},
    {"nome": "Olho Celestial",            "chines": "天眼",  "raridade": "Incomum",  "bonus": (6, 10)},
    {"nome": "Coração de Espada",         "chines": "剑心",  "raridade": "Incomum",  "bonus": (7, 11)},
    {"nome": "Corpo do Dao",              "chines": "道体",  "raridade": "Raro",     "bonus": (10, 16)},
    {"nome": "Veia do Dragão",            "chines": "龙脉",  "raridade": "Raro",     "bonus": (11, 17)},
    {"nome": "Caverna-Paraíso",           "chines": "洞天",  "raridade": "Raro",     "bonus": (12, 18)},
    {"nome": "Raiz Espiritual Celestial", "chines": "天灵根", "raridade": "Lendário", "bonus": (20, 28)},
    {"nome": "Corpo do Caos",             "chines": "混沌体", "raridade": "Lendário", "bonus": (22, 32)},
    {"nome": "Corpo Estelar",             "chines": "星辰体", "raridade": "Lendário", "bonus": (24, 35)},
]


def sortear_talento():
    """Sorteia primeiro a raridade (pelo peso) e depois o talento e a porcentagem."""
    raridade = random.choices(list(RARIDADES), weights=[r["peso"] for r in RARIDADES.values()])[0]
    talento = random.choice([t for t in TALENTOS if t["raridade"] == raridade])
    minimo, maximo = talento["bonus"]
    percentual = round(random.uniform(minimo, maximo), 1)
    return talento, percentual


# ---------------------------------------------------------------
# CONFIGURAÇÃO VISUAL
# ---------------------------------------------------------------
FONTE_CHINES = "fontes/NotoSansSC-Bold.ttf"
FONTE_TEXTO = "fontes/Cinzel-VariableFont_wght.ttf"

MARROM = pygame.Color("#4B261C")
DOURADO = pygame.Color("#BC9148")
CLARINHO = pygame.Color("#DECC9A")
FUNDO_CARTA = (32, 26, 20)
FUNDO_FITA = (22, 18, 14)

LARGURA_CARTA = 200
ALTURA_CARTA = 190
ESPACO = 12
TOTAL_CARTAS = 45        # tamanho da "fita" que passa na roleta
POS_VENCEDOR = 38        # posição da fita onde o talento sorteado para
DURACAO = 4500           # ms que a roleta gira


def quebrar_texto(texto, fonte, largura_max):
    """Divide o texto em linhas que cabem na largura dada."""
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = f"{atual} {palavra}".strip()
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    linhas.append(atual)
    return linhas


class RoletaTalentos:
    def __init__(self, area_fita, area_resultado):
        self.area = area_fita                  # retângulo da roleta (onde as cartas passam)
        self.area_resultado = area_resultado   # retângulo onde aparece o talento sorteado

        # fontes (criadas uma vez)
        self.f_chines_carta = pygame.font.Font(FONTE_CHINES, 48)
        self.f_nome = pygame.font.Font(FONTE_TEXTO, 19)
        self.f_raridade = pygame.font.Font(FONTE_TEXTO, 16)
        self.f_aviso = pygame.font.Font(FONTE_TEXTO, 30)
        self.f_rar_res = pygame.font.Font(FONTE_TEXTO, 24)
        self.f_chines_res = pygame.font.Font(FONTE_CHINES, 80)
        self.f_nome_res = pygame.font.Font(FONTE_TEXTO, 38)
        self.f_pct = pygame.font.Font(FONTE_TEXTO, 52)

        # cartas e sombras (desenhadas uma vez)
        self.cartas = {t["nome"]: self._criar_carta(t) for t in TALENTOS}
        self.sombra_esq = self._criar_sombra()
        self.sombra_dir = pygame.transform.flip(self.sombra_esq, True, False)

        # estado
        self.fita = [random.choice(TALENTOS) for _ in range(15)]
        self.indice_centro = 3          # carta que está no centro agora
        self.folga = 0                  # quanto a carta do centro está deslocada do meio exato
        self.deslocamento = self._desloc_para(3, 0)
        self.girando = False
        self.resultado = None
        self.indice_vencedor = None
        self.textos_resultado = []
        self.t_inicio = 0
        self.t_fim = 0
        self.desloc_inicial = 0
        self.alvo = 0

    # ---------- preparação ----------
    def _criar_carta(self, talento):
        cor = RARIDADES[talento["raridade"]]["cor"]
        sup = pygame.Surface((LARGURA_CARTA, ALTURA_CARTA), pygame.SRCALPHA)
        pygame.draw.rect(sup, FUNDO_CARTA, (0, 0, LARGURA_CARTA, ALTURA_CARTA), border_radius=10)
        pygame.draw.rect(sup, cor, (0, 0, LARGURA_CARTA, ALTURA_CARTA), 3, border_radius=10)

        chines = self.f_chines_carta.render(talento["chines"], True, CLARINHO)
        sup.blit(chines, chines.get_rect(center=(LARGURA_CARTA // 2, 62)))

        y = 120
        for linha in quebrar_texto(talento["nome"], self.f_nome, LARGURA_CARTA - 24):
            img = self.f_nome.render(linha, True, CLARINHO)
            sup.blit(img, img.get_rect(center=(LARGURA_CARTA // 2, y)))
            y += img.get_height() + 1

        rar = self.f_raridade.render(talento["raridade"], True, cor)
        sup.blit(rar, rar.get_rect(center=(LARGURA_CARTA // 2, ALTURA_CARTA - 18)))
        return sup

    def _criar_sombra(self):
        """Degradê escuro nas bordas da roleta, para as cartas 'entrarem' suavemente."""
        largura = 140
        sup = pygame.Surface((largura, self.area.height), pygame.SRCALPHA)
        for x in range(largura):
            alpha = int(230 * (1 - x / largura) ** 1.5)
            pygame.draw.line(sup, (*FUNDO_FITA, alpha), (x, 0), (x, self.area.height))
        return sup

    def _desloc_para(self, indice, folga):
        """Deslocamento da fita para a carta 'indice' ficar no meio da roleta."""
        passo = LARGURA_CARTA + ESPACO
        return indice * passo + LARGURA_CARTA / 2 - self.area.width / 2 + folga

    # ---------- ação ----------
    def girar(self):
        """Inicia um giro. Devolve False se já estiver girando."""
        if self.girando:
            return False

        talento, percentual = sortear_talento()

        # nova fita: mantém as cartas visíveis agora (sem pulo) e sorteia o resto
        c = self.indice_centro
        janela = self.fita[c - 3:c + 4]
        nova = list(janela) + [random.choice(TALENTOS) for _ in range(TOTAL_CARTAS - len(janela))]
        nova[POS_VENCEDOR] = talento
        self.fita = nova

        self.desloc_inicial = self._desloc_para(3, self.folga)
        self.folga = random.uniform(-0.35, 0.35) * LARGURA_CARTA    # para em ponto diferente da carta
        self.alvo = self._desloc_para(POS_VENCEDOR, self.folga)
        self.indice_centro = POS_VENCEDOR

        self.resultado = {"talento": talento, "percentual": percentual}
        self.indice_vencedor = None
        self.textos_resultado = []
        self.girando = True
        self.t_inicio = pygame.time.get_ticks()
        return True

    def _atualizar(self):
        if not self.girando:
            return
        agora = pygame.time.get_ticks()
        t = min(1, (agora - self.t_inicio) / DURACAO)
        suave = 1 - (1 - t) ** 4        # começa rápido e vai freando
        self.deslocamento = self.desloc_inicial + (self.alvo - self.desloc_inicial) * suave
        if t >= 1:
            self.girando = False
            self.indice_vencedor = POS_VENCEDOR
            self.t_fim = agora
            self._montar_textos_resultado()

    def _montar_textos_resultado(self):
        talento = self.resultado["talento"]
        cor = RARIDADES[talento["raridade"]]["cor_escura"]
        pct = f"{self.resultado['percentual']:.1f}".replace(".", ",")
        # (imagem, distância do topo da área de resultado)
        self.textos_resultado = [
            (self.f_rar_res.render(f"— {talento['raridade']} —", True, cor), 20),
            (self.f_chines_res.render(talento["chines"], True, MARROM), 82),
            (self.f_nome_res.render(talento["nome"], True, MARROM), 150),
            (self.f_pct.render(f"+{pct}% de Qi", True, cor), 205),
        ]

    # ---------- desenho ----------
    def desenhar(self, tela):
        self._atualizar()
        self._desenhar_fita(tela)
        self._desenhar_resultado(tela)

    def _desenhar_fita(self, tela):
        passo = LARGURA_CARTA + ESPACO
        pygame.draw.rect(tela, FUNDO_FITA, self.area, border_radius=8)

        tela.set_clip(self.area)
        y = self.area.centery - ALTURA_CARTA // 2
        primeira = max(0, int(self.deslocamento // passo))
        ultima = min(len(self.fita) - 1, int((self.deslocamento + self.area.width) // passo) + 1)
        for i in range(primeira, ultima + 1):
            x = self.area.x - self.deslocamento + i * passo
            carta = self.cartas[self.fita[i]["nome"]]
            tela.blit(carta, (int(x), y))
            if i == self.indice_vencedor:                      # destaque pulsante no vencedor
                pulso = abs((pygame.time.get_ticks() % 1000) - 500) / 500
                cor = RARIDADES[self.fita[i]["raridade"]]["cor"]
                destaque = pygame.Rect(int(x), y, LARGURA_CARTA, ALTURA_CARTA).inflate(6 + 6 * pulso, 6 + 6 * pulso)
                pygame.draw.rect(tela, cor, destaque, 3, border_radius=12)
        tela.blit(self.sombra_esq, self.area.topleft)
        tela.blit(self.sombra_dir, (self.area.right - self.sombra_dir.get_width(), self.area.y))
        tela.set_clip(None)

        # moldura e marcador do meio
        pygame.draw.rect(tela, DOURADO, self.area, 3, border_radius=8)
        cx = self.area.centerx
        pygame.draw.line(tela, DOURADO, (cx, self.area.top), (cx, self.area.bottom), 2)
        pygame.draw.polygon(tela, DOURADO, [(cx - 12, self.area.top), (cx + 12, self.area.top), (cx, self.area.top + 16)])
        pygame.draw.polygon(tela, DOURADO, [(cx - 12, self.area.bottom), (cx + 12, self.area.bottom), (cx, self.area.bottom - 16)])

    def _desenhar_resultado(self, tela):
        r = self.area_resultado
        if self.girando:
            aviso = self.f_aviso.render("Girando...", True, MARROM)
            tela.blit(aviso, aviso.get_rect(center=r.center))
        elif self.resultado is None:
            aviso = self.f_aviso.render("Gire a roleta para receber um talento", True, MARROM)
            tela.blit(aviso, aviso.get_rect(center=r.center))
        else:
            alfa = min(255, int((pygame.time.get_ticks() - self.t_fim) / 500 * 255))   # aparece suave
            for imagem, dy in self.textos_resultado:
                imagem.set_alpha(alfa)
                tela.blit(imagem, imagem.get_rect(center=(r.centerx, r.y + dy)))