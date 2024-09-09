import pygame
import sys
import asyncio
import time
import random

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Kminna")

# Colores vivos y amigables para niños
BLANCO = (255, 255, 255)
AZUL = (0, 102, 204)  # Azul más brillante
VERDE = (102, 204, 0)  # Verde más vivo
AMARILLO = (255, 255, 51)  # Amarillo más brillante
ROJO = (255, 51, 51)  # Rojo brillante
GRIS = (50, 50, 50)
NEGRO = (0, 0, 0)
NARANJA = (255, 165, 0)
GRIS_CLARO = (192, 192, 192)  # Gris claro para el fondo de información
AZUL_CLARO = (0, 153, 255)  # Azul más vivo para los botones
VERDE_CLARO = (153, 255, 102)  # Verde más brillante para el botón de inicio

# Tamaño de las celdas del tablero
TAMANO_CELDA = 60
FILAS, COLUMNAS = ALTO_PANTALLA // TAMANO_CELDA, (ANCHO_PANTALLA - 600) // TAMANO_CELDA

# Velocidad de animación
velocidad_robot = 5

# Dirección inicial del robot
direccion_robot = 'DERECHA'

# Comandos disponibles con botones más grandes
bloques_comandos = [
    {"nombre": "MOVER", "rect": pygame.Rect(640, 50, 160, 50)},
    {"nombre": "GIRAR_IZQUIERDA", "rect": pygame.Rect(640, 120, 160, 50)},
    {"nombre": "GIRAR_DERECHA", "rect": pygame.Rect(640, 190, 160, 50)},
    {"nombre": "SALTAR", "rect": pygame.Rect(640, 260, 160, 50)},
    {"nombre": "ENCENDER_LUZ", "rect": pygame.Rect(640, 330, 160, 50)}
]

# Botón de "Iniciar" para ejecutar la secuencia con más tamaño
boton_iniciar = {"nombre": "INICIAR", "rect": pygame.Rect(640, 420, 160, 50)}

# Lista para almacenar la secuencia de comandos seleccionada
secuencia_comandos = []

# Variables para contar comandos y tiempo
conteo_comandos = 0
tiempo_inicio = time.time()

# Definir los niveles del juego
niveles = [
    {
        "inicio_robot": (0, 0),
        "luz": (5 * TAMANO_CELDA, 5 * TAMANO_CELDA),
        "obstaculos": [(random.randint(0, COLUMNAS - 1) * TAMANO_CELDA, random.randint(0, FILAS - 1) * TAMANO_CELDA) for _ in range(10)]
    },
    {
        "inicio_robot": (0, 0),
        "luz": (7 * TAMANO_CELDA, 7 * TAMANO_CELDA),
        "obstaculos": [(random.randint(0, COLUMNAS - 1) * TAMANO_CELDA, random.randint(0, FILAS - 1) * TAMANO_CELDA) for _ in range(15)]
    },
    {
        "inicio_robot": (0, 0),
        "luz": (6 * TAMANO_CELDA, 6 * TAMANO_CELDA),
        "obstaculos": [(random.randint(0, COLUMNAS - 1) * TAMANO_CELDA, random.randint(0, FILAS - 1) * TAMANO_CELDA) for _ in range(20)]
    },
]

nivel_actual = 0
luz_encendida = False
nivel_completado = False

# Posición inicial del robot
robot_x, robot_y = niveles[nivel_actual]["inicio_robot"]

# Función para reiniciar el conteo de comandos
def reiniciar_conteo_comandos():
    global conteo_comandos
    conteo_comandos = 0

# Función para cargar el nivel
def cargar_nivel(indice_nivel):
    global robot_x, robot_y, luz_x, luz_y, luz_encendida, nivel_completado, obstaculos, tiempo_inicio
    nivel = niveles[indice_nivel]

    # Posicionar el robot en el inicio del nivel
    robot_x, robot_y = nivel["inicio_robot"]

    # Generar los obstáculos evitando que aparezcan en la posición del robot o la luz
    obstaculos = []
    while len(obstaculos) < len(nivel["obstaculos"]):
        obstaculo_x = random.randint(0, COLUMNAS - 1) * TAMANO_CELDA
        obstaculo_y = random.randint(0, FILAS - 1) * TAMANO_CELDA

        # Asegurarse de que los obstáculos no se coloquen en la posición del robot o la luz
        if (obstaculo_x, obstaculo_y) != (robot_x, robot_y) and (obstaculo_x, obstaculo_y) != (nivel["luz"]):
            obstaculos.append((obstaculo_x, obstaculo_y))

    # Posicionar la luz evitando que coincida con obstáculos o el robot
    while True:
        luz_x, luz_y = nivel["luz"]
        if (luz_x, luz_y) not in obstaculos and (luz_x, luz_y) != (robot_x, robot_y):
            break  # Si la luz no está en un obstáculo ni en el robot, continuar

    luz_encendida = False
    nivel_completado = False
    reiniciar_conteo_comandos()
    tiempo_inicio = time.time()

# Dibujar el tablero
def dibujar_tablero():
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            rect = pygame.Rect(columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            pygame.draw.rect(pantalla, BLANCO, rect, 1)

# Dibujar los bloques de comandos con más espacio
def dibujar_bloques_comandos():
    fuente = pygame.font.SysFont(None, 26)
    for bloque_comando in bloques_comandos:
        pygame.draw.rect(pantalla, AZUL_CLARO, bloque_comando["rect"])
        pygame.draw.rect(pantalla, NEGRO, bloque_comando["rect"], 3)  # Borde negro más grueso
        texto = fuente.render(bloque_comando["nombre"], True, NEGRO)
        rect_texto = texto.get_rect(center=bloque_comando["rect"].center)
        pantalla.blit(texto, rect_texto)

# Dibujar el botón de "Iniciar" con más espacio
def dibujar_boton_iniciar():
    fuente = pygame.font.SysFont(None, 26)
    pygame.draw.rect(pantalla, VERDE_CLARO, boton_iniciar["rect"])
    pygame.draw.rect(pantalla, NEGRO, boton_iniciar["rect"], 3)  # Borde negro más grueso
    texto = fuente.render(boton_iniciar["nombre"], True, NEGRO)
    rect_texto = texto.get_rect(center=boton_iniciar["rect"].center)
    pantalla.blit(texto, rect_texto)

# Dibujar la columna de secuencia
def dibujar_secuencia():
    fuente = pygame.font.SysFont(None, 24)
    y_pos = 50
    for comando in secuencia_comandos:
        texto_comando = fuente.render(comando, True, VERDE)
        pantalla.blit(texto_comando, (820, y_pos))
        y_pos += 30

# Dibujar la columna de información
def dibujar_columna_informacion():
    # Fondo de la sección de información
    pygame.draw.rect(pantalla, GRIS_CLARO, (1000, 0, 200, ALTO_PANTALLA))

    fuente = pygame.font.SysFont(None, 24)
    texto_comandos = fuente.render(f"Comandos usados: {conteo_comandos}", True, NEGRO)
    pantalla.blit(texto_comandos, (1020, 50))

    tiempo_transcurrido = time.time() - tiempo_inicio
    texto_tiempo = fuente.render(f"Tiempo: {int(tiempo_transcurrido)}s", True, NEGRO)
    pantalla.blit(texto_tiempo, (1020, 100))

# Dibujar el robot con un indicador frontal
def dibujar_robot_con_indicador():
    global robot_x, robot_y, direccion_robot
    pygame.draw.rect(pantalla, AZUL, (robot_x, robot_y, TAMANO_CELDA, TAMANO_CELDA))

    if direccion_robot == 'ARRIBA':
        rect_indicador = pygame.Rect(robot_x + 20, robot_y - 10, 20, 10)
    elif direccion_robot == 'ABAJO':
        rect_indicador = pygame.Rect(robot_x + 20, robot_y + TAMANO_CELDA, 20, 10)
    elif direccion_robot == 'IZQUIERDA':
        rect_indicador = pygame.Rect(robot_x - 10, robot_y + 20, 10, 20)
    elif direccion_robot == 'DERECHA':
        rect_indicador = pygame.Rect(robot_x + TAMANO_CELDA, robot_y + 20, 10, 20)

    pygame.draw.rect(pantalla, NARANJA, rect_indicador)

# Función para girar el robot a la izquierda o a la derecha
def girar_robot(direccion):
    global direccion_robot
    
    direcciones = ['ARRIBA', 'DERECHA', 'ABAJO', 'IZQUIERDA']
    indice_actual = direcciones.index(direccion_robot)
    
    if direccion == 'IZQUIERDA':
        direccion_robot = direcciones[(indice_actual - 1) % 4]
    elif direccion == 'DERECHA':
        direccion_robot = direcciones[(indice_actual + 1) % 4]

# Función para ejecutar la secuencia de comandos
async def ejecutar_comandos():
    global conteo_comandos
    for comando in secuencia_comandos:
        if comando == 'MOVER':
            await mover_robot()
        elif comando == 'GIRAR_IZQUIERDA':
            girar_robot('IZQUIERDA')
        elif comando == 'GIRAR_DERECHA':
            girar_robot('DERECHA')
        elif comando == 'SALTAR':
            await saltar_robot()
        elif comando == 'ENCENDER_LUZ':
            encender_luz()
        conteo_comandos += 1

# Dibujar el juego completo
def dibujar_juego():
    pantalla.fill(NEGRO)
    dibujar_tablero()

    # Fondo de la columna de botones
    pygame.draw.rect(pantalla, GRIS, (600, 0, 200, ALTO_PANTALLA))

    dibujar_bloques_comandos()
    dibujar_boton_iniciar()
    dibujar_robot_con_indicador()

    pygame.draw.rect(pantalla, AMARILLO if luz_encendida else BLANCO, (luz_x, luz_y, TAMANO_CELDA, TAMANO_CELDA))

    for obstaculo in obstaculos:
        pygame.draw.rect(pantalla, ROJO, (obstaculo[0], obstaculo[1], TAMANO_CELDA, TAMANO_CELDA))

    # Dibujar la columna de secuencia
    dibujar_secuencia()

    # Dibujar la columna de información con fondo
    dibujar_columna_informacion()

    if nivel_completado:
        fuente = pygame.font.SysFont(None, 24)
        texto = fuente.render("¡Nivel completado! Presiona N para el siguiente nivel", True, VERDE)
        pantalla.blit(texto, (50, ALTO_PANTALLA - 50))

# Función para mover el robot
async def mover_robot():
    global robot_x, robot_y, direccion_robot

    destino_x, destino_y = robot_x, robot_y
    if direccion_robot == 'ARRIBA':
        destino_y = max(robot_y - TAMANO_CELDA, 0)
    elif direccion_robot == 'ABAJO':
        destino_y = min(robot_y + TAMANO_CELDA, ALTO_PANTALLA - TAMANO_CELDA)
    elif direccion_robot == 'IZQUIERDA':
        destino_x = max(robot_x - TAMANO_CELDA, 0)
    elif direccion_robot == 'DERECHA':
        destino_x = min(robot_x + TAMANO_CELDA, (ANCHO_PANTALLA - 600) - TAMANO_CELDA)

    if (destino_x, destino_y) in obstaculos:
        print("¡Obstáculo detectado! Usa SALTAR.")
    else:
        await animar_movimiento(destino_x, destino_y)

# Función para saltar el robot
async def saltar_robot():
    global robot_x, robot_y, direccion_robot

    destino_x, destino_y = robot_x, robot_y
    if direccion_robot == 'ARRIBA':
        destino_y = max(robot_y - 2 * TAMANO_CELDA, 0)
    elif direccion_robot == 'ABAJO':
        destino_y = min(robot_y + 2 * TAMANO_CELDA, ALTO_PANTALLA - TAMANO_CELDA)
    elif direccion_robot == 'IZQUIERDA':
        destino_x = max(robot_x - 2 * TAMANO_CELDA, 0)
    elif direccion_robot == 'DERECHA':
        destino_x = min(robot_x + 2 * TAMANO_CELDA, (ANCHO_PANTALLA - 600) - TAMANO_CELDA)

    if (destino_x, destino_y) in obstaculos:
        print("¡Obstáculo detectado! No puedes saltar sobre él.")
    else:
        await animar_movimiento(destino_x, destino_y)

# Función para animar el movimiento del robot
async def animar_movimiento(destino_x, destino_y):
    global robot_x, robot_y
    while robot_x != destino_x or robot_y != destino_y:
        if robot_x < destino_x:
            robot_x += velocidad_robot
        elif robot_x > destino_x:
            robot_x -= velocidad_robot
        if robot_y < destino_y:
            robot_y += velocidad_robot
        elif robot_y > destino_y:
            robot_y -= velocidad_robot
        dibujar_juego()
        pygame.display.flip()
        await asyncio.sleep(0.03)

# Función para encender la luz
def encender_luz():
    global luz_encendida, nivel_completado
    if robot_x == luz_x and robot_y == luz_y:
        luz_encendida = True
        nivel_completado = True
        print("¡Luz encendida! ¡Nivel completado!")
    else:
        print("¡El robot no está en la casilla de luz!")

# Bucle principal del juego
async def main():
    global secuencia_comandos, nivel_actual
    reloj = pygame.time.Clock()

    comando_arrastrado = None

    cargar_nivel(nivel_actual)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for bloque_comando in bloques_comandos:
                    if bloque_comando["rect"].collidepoint(evento.pos):
                        comando_arrastrado = bloque_comando["nombre"]
                        break
                if boton_iniciar["rect"].collidepoint(evento.pos):
                    await ejecutar_comandos()
                    secuencia_comandos = []

            if evento.type == pygame.MOUSEBUTTONUP:
                if comando_arrastrado:
                    if 800 <= evento.pos[0] <= 1000:
                        secuencia_comandos.append(comando_arrastrado)
                    comando_arrastrado = None

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_n and nivel_completado:
                    nivel_actual += 1
                    if nivel_actual < len(niveles):
                        cargar_nivel(nivel_actual)
                    else:
                        print("¡No hay más niveles!")
                    secuencia_comandos = []
                    reiniciar_conteo_comandos()
                    tiempo_inicio = time.time()

        dibujar_juego()

        if comando_arrastrado:
            pos = pygame.mouse.get_pos()
            fuente = pygame.font.SysFont(None, 22)
            texto = fuente.render(comando_arrastrado, True, BLANCO)
            pantalla.blit(texto, pos)

        pygame.display.flip()
        reloj.tick(30)
        await asyncio.sleep(0)

# Ejecutar el juego de manera asincrónica
asyncio.run(main())
