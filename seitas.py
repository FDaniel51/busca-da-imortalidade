import pygame

# =====================================================================
#  ABA DAS SEITAS  -  módulo independente (precisa só do pygame)
#
#  Como usar no jogo:
#      from seitas import AbaSeitas
#      aba_seitas = AbaSeitas(pygame.Rect(400, 140, 1200, 800))
#      aba_seitas.tratar_evento(evento)        # nos eventos de clique
#      aba_seitas.desenhar(tela)               # no desenho da aba
#      aba_seitas.seita_atual                  # id da seita (ou None)
# =====================================================================

# ---------------------------------------------------------------------
# CONFIGURAÇÃO VISUAL
# ---------------------------------------------------------------------
FONTE_CHINES = "fontes/NotoSansSC-Bold.ttf"
FONTE_TEXTO = "fontes/Cinzel-VariableFont_wght.ttf"

MARROM = pygame.Color("#4B261C")
DOURADO = pygame.Color("#BC9148")
CLARINHO = pygame.Color("#DECC9A")
FUNDO_CARTA = (70, 64, 58)       # fundo das cartas e do painel de detalhes
TEXTO_SUAVE = (206, 198, 176)
COR_BONUS = (120, 220, 150)

LARG_CARTA = 340
ALT_CARTA = 150
ESPACO_CARTAS = 12

# ---------------------------------------------------------------------
# DADOS
# ---------------------------------------------------------------------
# Os três lados. "cor" é a cor viva (usada sobre fundo escuro),
# "cor_escura" é a versão para ler sobre o painel creme.
LADOS = [
    {"id": "ortodoxo",     "nome": "Ortodoxo",     "chines": "正派",
     "cor": (90, 160, 235), "cor_escura": (30, 90, 160)},
    {"id": "nao_ortodoxo", "nome": "Não Ortodoxo", "chines": "邪派",
     "cor": (90, 190, 115), "cor_escura": (30, 120, 60)},
    {"id": "demoniaco",    "nome": "Demoníaco",    "chines": "魔教",
     "cor": (225, 75, 75),  "cor_escura": (150, 30, 30)},
]

# Tipos de bônus (mesmas chaves do inventário): chave -> (nome mostrado, é porcentagem?)
NOMES_BONUS = {
    "qi_clique":        ("Qi por clique", False),
    "qi_segundo":       ("Qi por segundo", False),
    "qi_pct":           ("Qi total", True),
    "qi_segundo_pct":   ("Qi por segundo", True),
    "custo_refino_pct": ("Custo de refino", True),
    "sorte_pct":        ("Sorte", True),
}

# As 9 seitas. Cada lado mostra suas seitas na ordem em que aparecem aqui.
# "bonus" vale enquanto o jogador for membro (os valores são sugestões, mude à vontade).
SEITAS = [
    # ---------------- ORTODOXO ----------------
    {"id": "shaolin", "nome": "Seita Shaolin", "chines": "少林寺", "pinyin": "Shàolín Sì",
     "lado": "ortodoxo",
     "resumo": "Monges guerreiros que unem o Dharma ao corpo de aço.",
     "descricao": "Em seu templo ancestral, os monges forjam corpo e mente com disciplina "
                  "rigorosa. Cada golpe é uma oração, e cada oração, uma lição de força.",
     "bonus": {"qi_clique": 2}},
    {"id": "monte_hua", "nome": "Seita do Monte Hua", "chines": "华山派", "pinyin": "Huàshān Pài",
     "lado": "ortodoxo",
     "resumo": "Espadachins que treinam em picos cobertos de névoa.",
     "descricao": "Nos penhascos mais íngremes do Monte Hua, seus discípulos aprendem que a "
                  "espada mais afiada é a que sabe esperar o momento certo.",
     "bonus": {"custo_refino_pct": -5}},
    {"id": "wudang", "nome": "Seita Wudang", "chines": "武当派", "pinyin": "Wǔdāng Pài",
     "lado": "ortodoxo",
     "resumo": "Mestres taoístas da harmonia entre Yin e Yang.",
     "descricao": "Seguidores do Dao, os mestres de Wudang acreditam que a suavidade vence a "
                  "dureza. Seu Qi flui como a água, sem pressa e sem fim.",
     "bonus": {"qi_segundo_pct": 5}},

    # ---------------- NÃO ORTODOXO ----------------
    {"id": "floresta_verde", "nome": "Floresta Verde", "chines": "绿林", "pinyin": "Lǜlín",
     "lado": "nao_ortodoxo",
     "resumo": "Bandos livres de foras-da-lei que seguem o próprio código.",
     "descricao": "Escondidos entre as árvores, estes andarilhos não devem lealdade a trono "
                  "nem a templo. Confiam na astúcia, no acaso e uns nos outros.",
     "bonus": {"sorte_pct": 6}},
    {"id": "cla_tang", "nome": "Clã Tang", "chines": "唐门", "pinyin": "Táng Mén",
     "lado": "nao_ortodoxo",
     "resumo": "Família mestra em venenos e armas ocultas.",
     "descricao": "Poucos viram um Tang lutando, e menos ainda sobreviveram para contar. "
                  "Seus segredos passam de pai para filho e jamais saem da família.",
     "bonus": {"qi_pct": 3}},
    {"id": "pavilhao_sombras", "nome": "Pavilhão das Sombras", "chines": "暗影阁", "pinyin": "Ànyǐng Gé",
     "lado": "nao_ortodoxo",
     "resumo": "Rede de assassinos e espiões que vendem segredos.",
     "descricao": "Ninguém sabe onde fica o pavilhão, mas todos sabem que ele sabe de tudo. "
                  "Quem paga o preço certo recebe a informação, ou a lâmina.",
     "bonus": {"sorte_pct": 4, "qi_clique": 1}},

    # ---------------- DEMONÍACO ----------------
    {"id": "demonio_celestial", "nome": "Culto do Demônio Celestial", "chines": "天魔教", "pinyin": "Tiānmó Jiào",
     "lado": "demoniaco",
     "resumo": "Fiéis do poder absoluto, que desafiam o Céu.",
     "descricao": "Para o culto, o Céu é apenas uma jaula. Seus fiéis buscam um poder sem "
                  "limites e rejeitam qualquer lei que tente contê-los.",
     "bonus": {"qi_pct": 6}},
    {"id": "seita_sangue", "nome": "Seita do Sangue", "chines": "血宗", "pinyin": "Xuè Zōng",
     "lado": "demoniaco",
     "resumo": "Cultivam a força através do sangue e do sacrifício.",
     "descricao": "Cada ferida aberta é uma porta, e cada sacrifício, uma chave. A seita "
                  "ensina que só quem sangra por poder o merece de verdade.",
     "bonus": {"qi_clique": 3}},
    {"id": "sol_e_lua", "nome": "Culto do Sol e da Lua", "chines": "日月神教", "pinyin": "Rìyuè Shénjiào",
     "lado": "demoniaco",
     "resumo": "Culto místico dividido entre a luz e a escuridão.",
     "descricao": "Entre o brilho do dia e o silêncio da noite, seus devotos encontram um "
                  "poder duplo. Dizem que o culto nunca dorme, apenas troca de rosto.",
     "bonus": {"qi_segundo_pct": 7}},
]


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
    return [l for l in linhas if l]


def formatar_bonus(chave, valor):
    nome, percentual = NOMES_BONUS.get(chave, (chave, False))
    numero = f"{valor:+g}".replace(".", ",")
    return f"{numero}{'%' if percentual else ''} {nome}"


# ---------------------------------------------------------------------
# CLASSE PRINCIPAL
# ---------------------------------------------------------------------
class AbaSeitas:
    def __init__(self, area, ao_mudar=None):
        """
        area    : Rect do painel onde a aba é desenhada
        ao_mudar: função opcional ao_mudar(id_antiga, id_nova), chamada quando o jogador
                  entra, troca ou sai de uma seita (id None = sem seita)
        """
        self.area = area
        self.ao_mudar = ao_mudar
        self.seita_atual = None        # id da seita em que o jogador entrou
        self.selecionada = None        # id da carta clicada (mostra os detalhes)

        self.lados = {l["id"]: l for l in LADOS}
        self.seitas = {s["id"]: s for s in SEITAS}

        # fontes (criadas uma vez)
        self.f_cab_chines = pygame.font.Font(FONTE_CHINES, 40)
        self.f_cab_nome = pygame.font.Font(FONTE_TEXTO, 24)
        self.f_card_chines = pygame.font.Font(FONTE_CHINES, 30)
        self.f_card_nome = pygame.font.Font(FONTE_TEXTO, 22)
        self.f_card_resumo = pygame.font.Font(FONTE_TEXTO, 15)
        self.f_det_chines = pygame.font.Font(FONTE_CHINES, 58)
        self.f_pinyin = pygame.font.Font(FONTE_CHINES, 16)      # pinyin usa a fonte chinesa (tem os acentos de tom)
        self.f_det_nome = pygame.font.Font(FONTE_TEXTO, 30)
        self.f_det_texto = pygame.font.Font(FONTE_TEXTO, 17)
        self.f_rotulo = pygame.font.Font(FONTE_TEXTO, 16)
        self.f_bonus = pygame.font.Font(FONTE_TEXTO, 18)
        self.f_botao = pygame.font.Font(FONTE_TEXTO, 22)
        self.f_aviso = pygame.font.Font(FONTE_TEXTO, 26)

        self._calcular_layout()
        self.cartas = {s["id"]: self._criar_carta(s) for s in SEITAS}
        self.detalhes = {s["id"]: self._criar_detalhes(s) for s in SEITAS}
        self.selo_membro = self._criar_selo("Membro")

    # ------------------------------------------------------------------
    # LÓGICA
    # ------------------------------------------------------------------
    def entrar(self, id_seita):
        """Entra (ou troca para) uma seita. Devolve False se o id não existe."""
        if id_seita not in self.seitas:
            return False
        antiga = self.seita_atual
        self.seita_atual = id_seita
        if self.ao_mudar and antiga != id_seita:
            self.ao_mudar(antiga, id_seita)
        return True

    def sair(self):
        """Deixa a seita atual."""
        antiga = self.seita_atual
        self.seita_atual = None
        if self.ao_mudar and antiga is not None:
            self.ao_mudar(antiga, None)

    def bonus_total(self):
        """Bônus da seita atual. Ex.: {"qi_clique": 2}. Vazio se não houver seita."""
        if self.seita_atual is None:
            return {}
        return dict(self.seitas[self.seita_atual]["bonus"])

    def bonus(self, chave):
        """Bônus de um tipo (0 se a seita atual não der esse bônus)."""
        return self.bonus_total().get(chave, 0)

    def para_dict(self):
        """Estado em formato simples, pronto para salvar em JSON."""
        return {"seita_atual": self.seita_atual}

    def carregar_dict(self, dados):
        atual = dados.get("seita_atual")
        self.seita_atual = atual if atual in self.seitas else None

    # ------------------------------------------------------------------
    # EVENTOS
    # ------------------------------------------------------------------
    def tratar_evento(self, evento):
        """Clique esquerdo numa carta seleciona a seita; no botão, entra / troca / sai.
        Devolve True se o clique foi usado."""
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return False

        if self.selecionada and self.rect_botao.collidepoint(evento.pos):
            if self.seita_atual == self.selecionada:
                self.sair()
            else:
                self.entrar(self.selecionada)
            return True

        for id_seita, rect in self.rects_cartas.items():
            if rect.collidepoint(evento.pos):
                self.selecionada = id_seita
                return True
        return False

    # ------------------------------------------------------------------
    # LAYOUT E PRÉ-RENDERIZAÇÃO
    # ------------------------------------------------------------------
    def _calcular_layout(self):
        a = self.area
        self.largura_coluna = a.width // 3
        indice_lado = {l["id"]: i for i, l in enumerate(LADOS)}
        contagem = {l["id"]: 0 for l in LADOS}

        y_cartas = a.y + 135
        self.rects_cartas = {}
        for s in SEITAS:
            coluna = indice_lado[s["lado"]]
            linha = contagem[s["lado"]]
            contagem[s["lado"]] += 1
            x = a.x + coluna * self.largura_coluna + (self.largura_coluna - LARG_CARTA) // 2
            y = y_cartas + linha * (ALT_CARTA + ESPACO_CARTAS)
            self.rects_cartas[s["id"]] = pygame.Rect(x, y, LARG_CARTA, ALT_CARTA)

        linhas = max(contagem.values())
        self.y_fim_cartas = y_cartas + linhas * (ALT_CARTA + ESPACO_CARTAS) - ESPACO_CARTAS
        topo = self.y_fim_cartas + 16
        self.rect_detalhes = pygame.Rect(a.x + 30, topo, a.width - 60, a.bottom - 16 - topo)
        self.rect_botao = pygame.Rect(self.rect_detalhes.right - 20 - 300,
                                      self.rect_detalhes.bottom - 20 - 46, 300, 46)

    def _criar_carta(self, seita):
        lado = self.lados[seita["lado"]]
        sup = pygame.Surface((LARG_CARTA, ALT_CARTA), pygame.SRCALPHA)
        pygame.draw.rect(sup, FUNDO_CARTA, (0, 0, LARG_CARTA, ALT_CARTA), border_radius=10)

        # ideogramas na vertical, ao lado do nome (como em uma faixa tradicional)
        caracteres = list(seita["chines"])
        passo = 33
        y = (ALT_CARTA - len(caracteres) * passo) // 2
        for c in caracteres:
            img = self.f_card_chines.render(c, True, lado["cor"])
            sup.blit(img, img.get_rect(center=(42, y + passo // 2)))
            y += passo
        pygame.draw.line(sup, (112, 104, 94), (82, 18), (82, ALT_CARTA - 18), 1)

        # nome e resumo
        y = 18
        for linha in quebrar_texto(seita["nome"], self.f_card_nome, LARG_CARTA - 96 - 14):
            img = self.f_card_nome.render(linha, True, CLARINHO)
            sup.blit(img, (96, y))
            y += img.get_height()
        y += 6
        for linha in quebrar_texto(seita["resumo"], self.f_card_resumo, LARG_CARTA - 96 - 14):
            img = self.f_card_resumo.render(linha, True, TEXTO_SUAVE)
            sup.blit(img, (96, y))
            y += img.get_height() + 1
        return sup

    def _criar_detalhes(self, seita):
        """Painel de detalhes da seita (tudo, menos o botão, que muda conforme o estado)."""
        lado = self.lados[seita["lado"]]
        r = self.rect_detalhes
        sup = pygame.Surface(r.size, pygame.SRCALPHA)
        pygame.draw.rect(sup, FUNDO_CARTA, (0, 0, r.width, r.height), border_radius=10)
        pygame.draw.rect(sup, lado["cor"], (0, 0, r.width, r.height), 3, border_radius=10)

        # ideogramas (horizontal) e pinyin
        chines = self.f_det_chines.render(seita["chines"], True, lado["cor"])
        sup.blit(chines, chines.get_rect(midleft=(28, 62)))
        pinyin = self.f_pinyin.render(f"{seita['pinyin']}  |  {lado['nome']}", True, TEXTO_SUAVE)
        sup.blit(pinyin, pinyin.get_rect(midleft=(28, 118)))

        # nome e descrição
        nome = self.f_det_nome.render(seita["nome"], True, CLARINHO)
        sup.blit(nome, (300, 16))
        y = 60
        for linha in quebrar_texto(seita["descricao"], self.f_det_texto, 470):
            img = self.f_det_texto.render(linha, True, TEXTO_SUAVE)
            sup.blit(img, (300, y))
            y += 22

        # bônus
        rotulo = self.f_rotulo.render("Bônus de membro", True, DOURADO)
        sup.blit(rotulo, (r.width - 20 - 250, 16))
        y = 40
        for chave, valor in seita["bonus"].items():
            img = self.f_bonus.render(formatar_bonus(chave, valor), True, COR_BONUS)
            sup.blit(img, (r.width - 20 - 250, y))
            y += 22
        return sup

    def _criar_selo(self, texto):
        img = self.f_rotulo.render(texto, True, MARROM)
        sup = pygame.Surface((img.get_width() + 20, 22), pygame.SRCALPHA)
        pygame.draw.rect(sup, DOURADO, sup.get_rect(), border_radius=11)
        sup.blit(img, img.get_rect(center=sup.get_rect().center))
        return sup

    # ------------------------------------------------------------------
    # DESENHO
    # ------------------------------------------------------------------
    def desenhar(self, tela):
        a = self.area
        mouse = pygame.mouse.get_pos()

        # cabeçalhos das três colunas
        for i, lado in enumerate(LADOS):
            cx = a.x + i * self.largura_coluna + self.largura_coluna // 2
            chines = self.f_cab_chines.render(lado["chines"], True, lado["cor_escura"])
            tela.blit(chines, chines.get_rect(midtop=(cx, a.y + 20)))
            nome = self.f_cab_nome.render(lado["nome"], True, MARROM)
            tela.blit(nome, nome.get_rect(midtop=(cx, a.y + 20 + chines.get_height())))
            pygame.draw.line(tela, lado["cor"], (cx - 70, a.y + 122), (cx + 70, a.y + 122), 3)

        # linhas verticais que separam os lados
        for i in (1, 2):
            x = a.x + i * self.largura_coluna
            pygame.draw.line(tela, DOURADO, (x, a.y + 20), (x, self.y_fim_cartas), 2)

        # cartas
        for s in SEITAS:
            id_seita = s["id"]
            rect = self.rects_cartas[id_seita]
            tela.blit(self.cartas[id_seita], rect.topleft)

            selecionada = id_seita == self.selecionada
            em_cima = rect.collidepoint(mouse)
            cor = DOURADO if (selecionada or em_cima) else self.lados[s["lado"]]["cor"]
            espessura = 4 if selecionada else (3 if em_cima else 2)
            pygame.draw.rect(tela, cor, rect, espessura, border_radius=10)

            if id_seita == self.seita_atual:
                tela.blit(self.selo_membro, self.selo_membro.get_rect(center=(rect.right - 12 - self.selo_membro.get_width() // 2, rect.y)))

        # painel de detalhes
        r = self.rect_detalhes
        if self.selecionada is None:
            pygame.draw.rect(tela, FUNDO_CARTA, r, border_radius=10)
            pygame.draw.rect(tela, DOURADO, r, 3, border_radius=10)
            if self.seita_atual:
                linha = f"Sua seita: {self.seitas[self.seita_atual]['nome']}"
                sub = "Clique em uma seita para ver os detalhes"
            else:
                linha = "Você ainda não pertence a nenhuma seita"
                sub = "Clique em uma seita para ver os detalhes"
            t1 = self.f_aviso.render(linha, True, CLARINHO)
            t2 = self.f_det_texto.render(sub, True, TEXTO_SUAVE)
            tela.blit(t1, t1.get_rect(center=(r.centerx, r.centery - 14)))
            tela.blit(t2, t2.get_rect(center=(r.centerx, r.centery + 20)))
        else:
            tela.blit(self.detalhes[self.selecionada], r.topleft)
            self._desenhar_botao(tela, mouse)

    def _desenhar_botao(self, tela, mouse):
        if self.seita_atual == self.selecionada:
            texto = "Deixar a seita"
        elif self.seita_atual is None:
            texto = "Entrar na seita"
        else:
            texto = "Trocar para esta seita"
        em_cima = self.rect_botao.collidepoint(mouse)
        pygame.draw.rect(tela, pygame.Color("#EBDDB2") if em_cima else CLARINHO, self.rect_botao, border_radius=8)
        pygame.draw.rect(tela, DOURADO, self.rect_botao, 3, border_radius=8)
        img = self.f_botao.render(texto, True, MARROM)
        tela.blit(img, img.get_rect(center=self.rect_botao.center))