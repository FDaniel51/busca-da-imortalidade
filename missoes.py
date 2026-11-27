import pygame

FONTE_CHINES = "fontes/NotoSansSC-Bold.ttf"
FONTE_TEXTO = "fontes/Cinzel-VariableFont_wght.ttf"

CONTRIB_POR_ROCHA = 20      # quanta contribuição vale 1 rocha espiritual

MARROM = pygame.Color("#4B261C")
DOURADO = pygame.Color("#BC9148")
CLARINHO = pygame.Color("#DECC9A")
FUNDO_CARTA = (70, 64, 58)
FUNDO_BARRA = (46, 41, 36)
TEXTO_SUAVE = (206, 198, 176)
OURO_VIVO = (240, 200, 100)
BOTAO_OFF = (150, 143, 130)

# cor de cada lado: (cor viva, cor escura para ler no painel creme)
LADOS_COR = {
    "ortodoxo":     ((90, 160, 235), (30, 90, 160)),
    "nao_ortodoxo": ((90, 190, 115), (30, 120, 60)),
    "demoniaco":    ((225, 75, 75),  (150, 30, 30)),
}

# ---------------------------------------------------------------------
# DADOS: 4 missões por lado (duração em segundos, recompensa em contribuição)
# ---------------------------------------------------------------------
MISSOES = {
    "ortodoxo": [
        {"id": "orto_patrulha", "nome": "Patrulhar a Montanha", "duracao": 15, "contribuicao": 4,
         "descricao": "Percorra as trilhas da seita e afaste os animais selvagens dos peregrinos."},
        {"id": "orto_vila", "nome": "Proteger a Vila", "duracao": 40, "contribuicao": 12,
         "descricao": "Aldeões pedem ajuda contra saqueadores. Defenda-os até a noite chegar."},
        {"id": "orto_escolta", "nome": "Escoltar Peregrinos", "duracao": 90, "contribuicao": 30,
         "descricao": "Acompanhe um grupo de fiéis até o templo, atravessando um desfiladeiro perigoso."},
        {"id": "orto_fera", "nome": "Selar a Fera Antiga", "duracao": 180, "contribuicao": 75,
         "descricao": "Uma criatura adormecida ameaça despertar. Reforce o selo antes que seja tarde."},
    ],
    "nao_ortodoxo": [
        {"id": "nao_estrada", "nome": "Vigiar a Estrada", "duracao": 15, "contribuicao": 4,
         "descricao": "Fique de olho nas caravanas que passam e avise o grupo sobre os guardas."},
        {"id": "nao_entrega", "nome": "Entregar Mercadoria Discreta", "duracao": 40, "contribuicao": 12,
         "descricao": "Leve um pacote sem perguntas até o ponto combinado, longe de olhares curiosos."},
        {"id": "nao_informacao", "nome": "Roubar Informações", "duracao": 90, "contribuicao": 30,
         "descricao": "Infiltre-se na casa de um rival e copie os documentos antes do amanhecer."},
        {"id": "nao_comboio", "nome": "Emboscar o Comboio", "duracao": 180, "contribuicao": 75,
         "descricao": "Um comboio carregado de tesouros cruzará a floresta. Prepare a emboscada perfeita."},
    ],
    "demoniaco": [
        {"id": "dem_ervas", "nome": "Colher Ervas Sombrias", "duracao": 15, "contribuicao": 4,
         "descricao": "Recolha plantas venenosas que só florescem sob a luz da lua."},
        {"id": "dem_desertor", "nome": "Caçar Desertores", "duracao": 40, "contribuicao": 12,
         "descricao": "Alguém tentou fugir do culto. Encontre-o antes que revele os segredos."},
        {"id": "dem_ritual", "nome": "Conduzir o Ritual", "duracao": 90, "contribuicao": 30,
         "descricao": "Prepare o altar e conduza o ritual que alimenta o poder da seita."},
        {"id": "dem_templo", "nome": "Invadir um Templo Rival", "duracao": 180, "contribuicao": 75,
         "descricao": "Atravesse as defesas de uma seita ortodoxa e roube a relíquia do santuário."},
    ],
}


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


def formatar_tempo(segundos):
    segundos = max(0, int(segundos))
    if segundos >= 60:
        return f"{segundos // 60}:{segundos % 60:02d}"
    return f"{segundos} s"


# ---------------------------------------------------------------------
# CLASSE PRINCIPAL
# ---------------------------------------------------------------------
class AbaMissoes:
    def __init__(self, area, obter_seita, ao_concluir=None):
        """
        area         : Rect do painel onde a aba é desenhada
        obter_seita  : função que devolve a seita atual ({"nome": ..., "lado": ...}) ou None
        ao_concluir  : função opcional ao_concluir(missao, contribuicao) chamada ao terminar uma missão
        """
        self.area = area
        self._obter_seita = obter_seita
        self.ao_concluir = ao_concluir

        self.contribuicao = 0
        self.rochas_espirituais = 0
        self.concluidas = {}               # id da missão -> quantas vezes foi concluída
        self.missao_ativa = None           # id da missão em andamento (ou None)
        self.inicio_missao = 0
        self._seita_anterior = None
        self.aviso = ""
        self.aviso_ate = 0

        # fontes (criadas uma vez)
        self.f_titulo = pygame.font.Font(FONTE_TEXTO, 40)
        self.f_seita = pygame.font.Font(FONTE_TEXTO, 24)
        self.f_nome = pygame.font.Font(FONTE_TEXTO, 26)
        self.f_texto = pygame.font.Font(FONTE_TEXTO, 16)
        self.f_info = pygame.font.Font(FONTE_TEXTO, 18)
        self.f_recompensa = pygame.font.Font(FONTE_TEXTO, 22)
        self.f_botao = pygame.font.Font(FONTE_TEXTO, 20)
        self.f_numero = pygame.font.Font(FONTE_TEXTO, 44)
        self.f_aviso = pygame.font.Font(FONTE_TEXTO, 20)
        self.f_bloqueio = pygame.font.Font(FONTE_TEXTO, 32)
        self.f_bloqueio_sub = pygame.font.Font(FONTE_TEXTO, 22)
        self.f_chines = pygame.font.Font(FONTE_CHINES, 22)
        self.f_marca = pygame.font.Font(FONTE_CHINES, 180)

        self._calcular_layout()
        self.cartas = {m["id"]: self._criar_carta(m) for lista in MISSOES.values() for m in lista}
        self.marca_bloqueio = self.f_marca.render("锁", True, (206, 190, 148))

    # ------------------------------------------------------------------
    # LÓGICA
    # ------------------------------------------------------------------
    def seita(self):
        """Seita atual do jogador (dicionário) ou None."""
        return self._obter_seita()

    def desbloqueada(self):
        return self.seita() is not None

    def missoes_disponiveis(self):
        """Lista de missões do lado da seita atual (vazia se não houver seita)."""
        seita = self.seita()
        if seita is None:
            return []
        return MISSOES.get(seita["lado"], [])[:len(self.rects_cartas)]

    def iniciar(self, id_missao):
        """Começa uma missão. Só uma de cada vez. Devolve True se começou."""
        if self.missao_ativa is not None:
            return False
        if id_missao not in [m["id"] for m in self.missoes_disponiveis()]:
            return False
        self.missao_ativa = id_missao
        self.inicio_missao = pygame.time.get_ticks()
        return True

    def atualizar(self):
        """Chame todo frame, mesmo com outra aba aberta, para a missão terminar no tempo certo."""
        seita = self.seita()
        id_seita = (seita.get("id") or seita["nome"]) if seita else None
        if id_seita != self._seita_anterior:           # trocou ou saiu da seita
            self.missao_ativa = None                    # cancela a missão em andamento
            self._seita_anterior = id_seita

        if self.missao_ativa is None:
            return
        missao = next((m for m in self.missoes_disponiveis() if m["id"] == self.missao_ativa), None)
        if missao is None:
            self.missao_ativa = None
            return
        if pygame.time.get_ticks() - self.inicio_missao >= missao["duracao"] * 1000:
            self.contribuicao += missao["contribuicao"]
            self.concluidas[missao["id"]] = self.concluidas.get(missao["id"], 0) + 1
            self.missao_ativa = None
            self._avisar(f"Missão concluída! +{missao['contribuicao']} de contribuição")
            if self.ao_concluir:
                self.ao_concluir(missao, missao["contribuicao"])

    def trocar(self, rochas):
        """Troca contribuição por 'rochas' rochas espirituais. Devolve True se conseguiu."""
        custo = rochas * CONTRIB_POR_ROCHA
        if rochas <= 0 or self.contribuicao < custo:
            return False
        self.contribuicao -= custo
        self.rochas_espirituais += rochas
        return True

    def trocar_tudo(self):
        """Troca toda a contribuição possível. Devolve quantas rochas ganhou."""
        rochas = self.contribuicao // CONTRIB_POR_ROCHA
        if rochas > 0 and self.trocar(rochas):
            return rochas
        return 0

    def gastar_rochas(self, quantidade):
        """Para uso futuro (lojas etc.). Devolve False, sem gastar, se não houver o bastante."""
        if quantidade <= 0 or self.rochas_espirituais < quantidade:
            return False
        self.rochas_espirituais -= quantidade
        return True

    def para_dict(self):
        """Estado em formato simples, pronto para salvar em JSON (a missão em andamento não é salva)."""
        return {"contribuicao": self.contribuicao,
                "rochas_espirituais": self.rochas_espirituais,
                "concluidas": dict(self.concluidas)}

    def carregar_dict(self, dados):
        self.contribuicao = int(dados.get("contribuicao", 0))
        self.rochas_espirituais = int(dados.get("rochas_espirituais", 0))
        self.concluidas = dict(dados.get("concluidas", {}))
        self.missao_ativa = None

    def _avisar(self, texto):
        self.aviso = texto
        self.aviso_ate = pygame.time.get_ticks() + 3000

    # ------------------------------------------------------------------
    # EVENTOS
    # ------------------------------------------------------------------
    def tratar_evento(self, evento):
        """Clique esquerdo nos botões 'Iniciar' e de troca. Devolve True se o clique foi usado."""
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return False
        if not self.desbloqueada():
            return False

        for i, missao in enumerate(self.missoes_disponiveis()):
            if self.rects_botoes[i].collidepoint(evento.pos):
                self.iniciar(missao["id"])
                return True

        if self.rects_troca["1"].collidepoint(evento.pos):
            self._tentar_troca(1)
            return True
        if self.rects_troca["5"].collidepoint(evento.pos):
            self._tentar_troca(5)
            return True
        if self.rects_troca["tudo"].collidepoint(evento.pos):
            rochas = self.trocar_tudo()
            if rochas:
                self._avisar(f"Você ganhou {rochas} rocha(s) espiritual(is)!")
            return True
        return False

    def _tentar_troca(self, rochas):
        if self.trocar(rochas):
            self._avisar(f"Você ganhou {rochas} rocha(s) espiritual(is)!")

    # ------------------------------------------------------------------
    # LAYOUT E PRÉ-RENDERIZAÇÃO
    # ------------------------------------------------------------------
    def _calcular_layout(self):
        a = self.area
        y0 = a.y + 115
        self.rects_cartas = [pygame.Rect(a.x + 30, y0 + i * 158, 760, 146) for i in range(4)]
        self.rects_botoes = [pygame.Rect(r.right - 20 - 200, r.bottom - 16 - 40, 200, 40) for r in self.rects_cartas]

        x_troca = a.x + 30 + 760 + 20
        self.rect_troca = pygame.Rect(x_troca, y0, a.right - 30 - x_troca, 4 * 158 - 12)
        bx, bw = self.rect_troca.x + 20, self.rect_troca.width - 40
        yb = self.rect_troca.y + 345
        self.rects_troca = {"1": pygame.Rect(bx, yb, bw, 44),
                            "5": pygame.Rect(bx, yb + 56, bw, 44),
                            "tudo": pygame.Rect(bx, yb + 112, bw, 44)}

    def _criar_carta(self, missao):
        sup = pygame.Surface(self.rects_cartas[0].size, pygame.SRCALPHA)
        w, h = sup.get_size()
        pygame.draw.rect(sup, FUNDO_CARTA, (0, 0, w, h), border_radius=10)

        sup.blit(self.f_nome.render(missao["nome"], True, CLARINHO), (24, 14))
        y = 52
        for linha in quebrar_texto(missao["descricao"], self.f_texto, 410)[:3]:
            sup.blit(self.f_texto.render(linha, True, TEXTO_SUAVE), (24, y))
            y += 20

        sup.blit(self.f_info.render(f"Duração: {formatar_tempo(missao['duracao'])}", True, TEXTO_SUAVE), (490, 16))
        sup.blit(self.f_recompensa.render(f"+{missao['contribuicao']} Contribuição", True, OURO_VIVO), (490, 44))
        return sup

    # ------------------------------------------------------------------
    # DESENHO
    # ------------------------------------------------------------------
    def desenhar(self, tela):
        a = self.area
        mouse = pygame.mouse.get_pos()
        seita = self.seita()

        titulo = self.f_titulo.render("Missões", True, MARROM)
        tela.blit(titulo, titulo.get_rect(midtop=(a.centerx, a.y + 22)))

        if seita is None:
            self._desenhar_bloqueio(tela)
            return

        cor, cor_escura = LADOS_COR.get(seita["lado"], ((190, 190, 190), (90, 90, 90)))
        sub = self.f_seita.render(seita["nome"], True, cor_escura)
        tela.blit(sub, sub.get_rect(midtop=(a.centerx, a.y + 72)))

        self._desenhar_missoes(tela, mouse, cor)
        self._desenhar_troca(tela, mouse)

    def _desenhar_bloqueio(self, tela):
        a = self.area
        tela.blit(self.marca_bloqueio, self.marca_bloqueio.get_rect(center=(a.centerx, a.centery - 110)))
        t1 = self.f_bloqueio.render("Missões bloqueadas", True, MARROM)
        tela.blit(t1, t1.get_rect(center=(a.centerx, a.centery + 30)))
        y = a.centery + 78
        for linha in quebrar_texto("As missões serão desbloqueadas quando você escolher uma seita.",
                                   self.f_bloqueio_sub, 700):
            t2 = self.f_bloqueio_sub.render(linha, True, MARROM)
            tela.blit(t2, t2.get_rect(center=(a.centerx, y)))
            y += 30
        t3 = self.f_texto.render("Escolha uma delas na aba Seitas.", True, (110, 80, 60))
        tela.blit(t3, t3.get_rect(center=(a.centerx, y + 10)))

    def _desenhar_missoes(self, tela, mouse, cor):
        agora = pygame.time.get_ticks()
        for i, missao in enumerate(self.missoes_disponiveis()):
            rect = self.rects_cartas[i]
            tela.blit(self.cartas[missao["id"]], rect.topleft)
            pygame.draw.rect(tela, cor, rect, 2, border_radius=10)

            ativa = missao["id"] == self.missao_ativa
            if ativa:
                duracao_ms = missao["duracao"] * 1000
                decorrido = agora - self.inicio_missao
                fracao = min(1.0, decorrido / duracao_ms)
                barra = pygame.Rect(rect.x + 24, rect.bottom - 26, 400, 12)
                pygame.draw.rect(tela, FUNDO_BARRA, barra, border_radius=6)
                if fracao > 0:
                    pygame.draw.rect(tela, cor, (barra.x, barra.y, max(12, int(barra.width * fracao)), barra.height),
                                     border_radius=6)
                pygame.draw.rect(tela, DOURADO, barra, 1, border_radius=6)
                resta = self.f_texto.render(formatar_tempo((duracao_ms - decorrido) / 1000 + 0.99), True, TEXTO_SUAVE)
                tela.blit(resta, resta.get_rect(midleft=(barra.right + 12, barra.centery)))

            # botão
            botao = self.rects_botoes[i]
            if ativa:
                texto, ligado = "Em andamento", False
            elif self.missao_ativa is not None:
                texto, ligado = "Ocupado", False
            else:
                texto, ligado = "Iniciar", True
            self._desenhar_botao(tela, botao, texto, ligado, mouse)

    def _desenhar_troca(self, tela, mouse):
        r = self.rect_troca
        pygame.draw.rect(tela, FUNDO_CARTA, r, border_radius=10)
        pygame.draw.rect(tela, DOURADO, r, 3, border_radius=10)

        t = self.f_nome.render("Troca com a Seita", True, CLARINHO)
        tela.blit(t, t.get_rect(midtop=(r.centerx, r.y + 18)))

        # saldos
        rot = self.f_info.render("Contribuição", True, TEXTO_SUAVE)
        tela.blit(rot, rot.get_rect(midtop=(r.centerx, r.y + 76)))
        num = self.f_numero.render(str(self.contribuicao), True, CLARINHO)
        tela.blit(num, num.get_rect(midtop=(r.centerx, r.y + 100)))

        rot2 = self.f_info.render("Rochas Espirituais", True, TEXTO_SUAVE)
        tela.blit(rot2, rot2.get_rect(midtop=(r.centerx - 22, r.y + 172)))
        chines = self.f_chines.render("灵石", True, OURO_VIVO)
        tela.blit(chines, chines.get_rect(midleft=(rot2.get_rect(midtop=(r.centerx - 22, r.y + 172)).right + 10, r.y + 184)))
        num2 = self.f_numero.render(str(self.rochas_espirituais), True, OURO_VIVO)
        tela.blit(num2, num2.get_rect(midtop=(r.centerx, r.y + 196)))

        y = r.y + 268
        for linha in quebrar_texto(f"{CONTRIB_POR_ROCHA} de contribuição = 1 rocha espiritual", self.f_texto, r.width - 50):
            img = self.f_texto.render(linha, True, TEXTO_SUAVE)
            tela.blit(img, img.get_rect(midtop=(r.centerx, y)))
            y += 22

        # botões de troca
        tudo = self.contribuicao // CONTRIB_POR_ROCHA
        opcoes = (("1", "Trocar 1 rocha", self.contribuicao >= CONTRIB_POR_ROCHA),
                  ("5", "Trocar 5 rochas", self.contribuicao >= 5 * CONTRIB_POR_ROCHA),
                  ("tudo", f"Trocar tudo ({tudo})", tudo > 0))
        for chave, texto, ligado in opcoes:
            self._desenhar_botao(tela, self.rects_troca[chave], texto, ligado, mouse)

        # aviso temporário
        if pygame.time.get_ticks() < self.aviso_ate:
            y = r.bottom - 70
            for linha in quebrar_texto(self.aviso, self.f_aviso, r.width - 40):
                img = self.f_aviso.render(linha, True, OURO_VIVO)
                tela.blit(img, img.get_rect(midtop=(r.centerx, y)))
                y += 26

    def _desenhar_botao(self, tela, rect, texto, ligado, mouse):
        if ligado:
            fundo = pygame.Color("#EBDDB2") if rect.collidepoint(mouse) else CLARINHO
            borda, cor_texto = DOURADO, MARROM
        else:
            fundo, borda, cor_texto = BOTAO_OFF, (120, 113, 100), (96, 90, 80)
        pygame.draw.rect(tela, fundo, rect, border_radius=8)
        pygame.draw.rect(tela, borda, rect, 3, border_radius=8)
        img = self.f_botao.render(texto, True, cor_texto)
        tela.blit(img, img.get_rect(center=rect.center))