import sys

import pygame

from settings import ALTO, ANCHO, FPS, NEGRO, BLANCO, GRIS, AZUL, ROSA, VERDE, AMARILLO


def dibujar_fondo(screen):
    screen.fill((6, 8, 18))

    for y in range(0, ALTO, 18):
        pygame.draw.line(screen, (14, 16, 32), (0, y), (ANCHO, y), 1)

    for i in range(30):
        x = (i * 37 + pygame.time.get_ticks() * 0.02) % ANCHO
        y = (i * 19 + pygame.time.get_ticks() * 0.03) % ALTO
        pygame.draw.circle(screen, (60, 80, 120), (int(x), int(y)), 1)


def dibujar_menu(screen, fuente, fuente_grande, titulo, opciones, seleccion):
    dibujar_fondo(screen)

    titulo_txt = fuente_grande.render(titulo, True, AMARILLO)
    screen.blit(titulo_txt, (40, 42))

    x = ANCHO - 240
    y = ALTO - 130
    for i, texto in enumerate(opciones):
        color = AMARILLO if i == seleccion else BLANCO
        marker = ">" if i == seleccion else " "
        txt = fuente.render(f"{marker} {i + 1}. {texto}", True, color)
        screen.blit(txt, (x, y + i * 28))

    pie = fuente.render("Z: confirmar    ↑↓: navegar", True, GRIS)
    screen.blit(pie, (ANCHO - 300, ALTO - 38))
    pygame.display.flip()


def pantalla_inicio(screen, fuente, fuente_grande):
    seleccion = 0
    opciones = ["JUGAR", "AJUSTES", "SALIR"]

    while True:
        dibujar_menu(screen, fuente, fuente_grande, "ORBE ARCADE", opciones, seleccion)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_z:
                    if seleccion == 0:
                        return "jugar"
                    if seleccion == 1:
                        return "ajustes"
                    pygame.quit()
                    sys.exit()


def pantalla_ajustes(screen, fuente, fuente_grande, config):
    seleccion = 0
    opciones = [
        f"Velocidad: {config['velocidad']}",
        f"Color: {config['color_nombre']}",
        f"Saltar texto: {'Sí' if config['saltar_texto'] else 'No'}",
        "Volver",
    ]

    while True:
        dibujar_fondo(screen)
        titulo = fuente_grande.render("AJUSTES", True, AMARILLO)
        screen.blit(titulo, (40, 42))

        x = ANCHO - 230
        y = ALTO - 135
        for i, texto in enumerate(opciones):
            color = AMARILLO if i == seleccion else BLANCO
            marker = ">" if i == seleccion else " "
            txt = fuente.render(f"{marker} {i + 1}. {texto}", True, color)
            screen.blit(txt, (x, y + i * 28))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_z:
                    if seleccion == 0:
                        config['velocidad'] = 3 if config['velocidad'] == 5 else 5
                        opciones[0] = f"Velocidad: {config['velocidad']}"
                    elif seleccion == 1:
                        if config['color_nombre'] == 'Azul':
                            config['color'] = ROSA
                            config['color_nombre'] = 'Rosa'
                        elif config['color_nombre'] == 'Rosa':
                            config['color'] = VERDE
                            config['color_nombre'] = 'Verde'
                        else:
                            config['color'] = AZUL
                            config['color_nombre'] = 'Azul'
                        opciones[1] = f"Color: {config['color_nombre']}"
                    elif seleccion == 2:
                        config['saltar_texto'] = not config['saltar_texto']
                        opciones[2] = f"Saltar texto: {'Sí' if config['saltar_texto'] else 'No'}"
                    else:
                        return config


def jugar(screen, config):
    reloj = pygame.time.Clock()
    x = ANCHO // 2
    y = ALTO // 2
    radius = 18
    font = pygame.font.SysFont(None, 28)
    font_dialogo = pygame.font.SysFont("DejaVu Sans Mono", 18, bold=True)

    objeto_x = ANCHO // 2
    objeto_y = ALTO // 2 + 80
    objeto_rect = pygame.Rect(objeto_x - 18, objeto_y - 18, 36, 36)

    dialogos = [
        "Hola, soy Niko.",
        "Presiona Z para avanzar poco a poco.",
        "Mantén C para saltar rápido este diálogo.",
        "¡Listo! Ya puedes seguir explorando.",
    ]
    dialogo_index = 0
    dialogo_activo = False
    texto_mostrado = ""
    reveal_timer = 0
    saltando_texto = False

    corriendo = True
    while corriendo:
        reloj.tick(FPS)
        dt = reloj.get_time() / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_x:
                    return "menu"
                if evento.key == pygame.K_z:
                    if (x - objeto_x) ** 2 + (y - objeto_y) ** 2 < 60 ** 2:
                        if not dialogo_activo:
                            dialogo_activo = True
                            dialogo_index = 0
                            texto_mostrado = ""
                            reveal_timer = 0
                        elif len(texto_mostrado) < len(dialogos[dialogo_index]):
                            reveal_timer = 0
                        else:
                            dialogo_index += 1
                            if dialogo_index >= len(dialogos):
                                dialogo_activo = False
                                dialogo_index = 0
                                texto_mostrado = ""
                            else:
                                texto_mostrado = ""
                                reveal_timer = 0
                if evento.key == pygame.K_c and config['saltar_texto']:
                    saltando_texto = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_c:
                saltando_texto = False

        teclas = pygame.key.get_pressed()
        saltando_texto = teclas[pygame.K_c] and config['saltar_texto']
        velocidad = 5 if teclas[pygame.K_RSHIFT] or teclas[pygame.K_LSHIFT] else config['velocidad']

        movimiento_x = 0
        movimiento_y = 0
        if teclas[pygame.K_UP]:
            movimiento_y -= velocidad
        if teclas[pygame.K_DOWN]:
            movimiento_y += velocidad
        if teclas[pygame.K_LEFT]:
            movimiento_x -= velocidad
        if teclas[pygame.K_RIGHT]:
            movimiento_x += velocidad

        player_rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        nueva_x = x + movimiento_x
        nueva_y = y + movimiento_y

        if not objeto_rect.colliderect(pygame.Rect(nueva_x - radius, y - radius, radius * 2, radius * 2)):
            x = max(radius, min(nueva_x, ANCHO - radius))
        if not objeto_rect.colliderect(pygame.Rect(x - radius, nueva_y - radius, radius * 2, radius * 2)):
            y = max(radius, min(nueva_y, ALTO - radius))

        screen.fill(NEGRO)
        pygame.draw.circle(screen, config['color'], (int(x), int(y)), radius)
        pygame.draw.rect(screen, (255, 215, 90), objeto_rect, border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255), objeto_rect, 2, border_radius=6)

        if dialogo_activo and len(texto_mostrado) < len(dialogos[dialogo_index]):
            if saltando_texto:
                texto_mostrado = dialogos[dialogo_index]
            else:
                reveal_timer += dt
                if reveal_timer >= 0.06:
                    reveal_timer = 0
                    texto_mostrado += dialogos[dialogo_index][len(texto_mostrado)]

        txt = font.render(f"X: {int(x)}   Y: {int(y)}", True, BLANCO)
        screen.blit(txt, (10, 10))
        hint = font.render("X: salir   Z: hablar   C: saltar   Shift: correr", True, GRIS)
        screen.blit(hint, (10, ALTO - 30))

        cerca = (x - objeto_x) ** 2 + (y - objeto_y) ** 2 < 70 ** 2
        if cerca:
            aviso = font_dialogo.render("Pulsa Z para interactuar", True, AMARILLO)
            screen.blit(aviso, (10, 45))

        if dialogo_activo:
            panel_x = 20
            panel_y = ALTO - 95
            panel_w = ANCHO - 40
            panel_h = 70
            pygame.draw.rect(screen, (18, 22, 35), (panel_x, panel_y, panel_w, panel_h), border_radius=10)
            pygame.draw.rect(screen, (120, 140, 170), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=10)
            texto = font_dialogo.render(texto_mostrado, True, BLANCO)
            screen.blit(texto, (panel_x + 12, panel_y + 18))
            instruccion = font.render("Z = avanzar   C = mantener para saltar", True, GRIS)
            screen.blit(instruccion, (panel_x + 12, panel_y + 45))

        pygame.display.flip()

    return "menu"
