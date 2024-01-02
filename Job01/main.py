import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Définition des constantes
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
FPS = 10

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Direction initiale du serpent
direction = (1, 0)

# Fonction principale
def main():
    global direction
    score = 0

    # Initialisation de l'écran
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Initialisation du serpent
    snake = [(100, 100), (90, 100), (80, 100)]

    # Initialisation de la pomme
    apple = generate_apple(snake)

    clock = pygame.time.Clock()

    # Boucle principale
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # Mise à jour de la position du serpent
        snake, apple, score = update(snake, apple, score)

        # Affichage
        screen.fill(WHITE)
        draw_snake(screen, snake)
        draw_apple(screen, apple)
        draw_score(screen, score)
        pygame.display.flip()

        clock.tick(FPS)

# Fonction pour mettre à jour la position du serpent
def update(snake, apple, score):
    global direction

    # Déplacement du serpent
    x, y = snake[0]
    dx, dy = direction
    new_head = ((x + dx * GRID_SIZE) % WIDTH, (y + dy * GRID_SIZE) % HEIGHT)
    snake.insert(0, new_head)

    # Vérification des collisions avec la pomme
    if snake[0] == apple:
        score += 1
        apple = generate_apple(snake)
    else:
        # Si le serpent n'a pas mangé la pomme, enlever la queue
        snake.pop()

    # Vérification des collisions avec le serpent lui-même
    if collision_with_self(snake):
        game_over(score)
        snake.clear()
        snake.append((100, 100))
        score = 0
        direction = (1, 0)

    return snake, apple, score

# Fonction pour générer une position aléatoire pour la pomme
def generate_apple(snake):
    while True:
        apple = (random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                 random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
        if apple not in snake:
            return apple

# Fonction pour détecter une collision avec le serpent lui-même
def collision_with_self(snake):
    return snake[0] in snake[1:]

# Fonction pour dessiner le serpent
def draw_snake(screen, snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

# Fonction pour dessiner la pomme
def draw_apple(screen, apple):
    pygame.draw.rect(screen, RED, (apple[0], apple[1], GRID_SIZE, GRID_SIZE))

# Fonction pour afficher le score
def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

# Fonction pour afficher l'écran de fin de jeu
def game_over(score):
    font = pygame.font.Font(None, 72)
    text = font.render(f"Game Over - Score: {score}", True, (255, 0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)  # Pause de 2 secondes pour afficher l'écran de fin
    pygame.event.clear()  # Efface tous les événements en attente

if __name__ == "__main__":
    main()
