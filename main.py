import os

import pygame

from settings import ALTO, ANCHO, FPS
from src.juego import jugar, pantalla_ajustes, pantalla_inicio


def reproducir_musica(ruta: str) -> None:
    pygame.mixer.music.stop()
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)


def main() -> None:
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("OneShot: Pygame Port")

    ruta_menu = os.path.join("OneShot: Pygame Port", "assets", "music", "My Burden Is Light.mp3")
    ruta_juego = os.path.join("OneShot: Pygame Port", "assets", "music", "Someplace I Know.mp3")
    reproducir_musica(ruta_menu)

    fuente = pygame.font.SysFont("DejaVu Sans Mono", 22, bold=True)
    fuente_grande = pygame.font.SysFont("DejaVu Sans Mono", 36, bold=True)

    config = {
        "velocidad": 3,
        "color": (0, 200, 255),
        "color_nombre": "Azul",
        "saltar_texto": True,
    }

    while True:
        accion = pantalla_inicio(screen, fuente, fuente_grande)
        if accion == "jugar":
            reproducir_musica(ruta_juego)
            estado = jugar(screen, config)
            if estado == "menu":
                reproducir_musica(ruta_menu)
                continue
        elif accion == "ajustes":
            config = pantalla_ajustes(screen, fuente, fuente_grande, config)
            continue


if __name__ == "__main__":
    main()
