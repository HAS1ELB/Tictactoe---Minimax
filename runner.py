import pygame
import sys
import time
import tictactoe as ttt

# Initialisation de Pygame
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

# Couleurs
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

# Polices
try:
    mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
    largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
    moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)
except FileNotFoundError:
    print("Police OpenSans-Regular.ttf introuvable.")
    sys.exit()

# Variables globales
user = None
board = ttt.initial_state()
ai_turn = False
clock = pygame.time.Clock()

# Fonctions utilitaires
def draw_text(screen, text, font, color, center):
    rendered_text = font.render(text, True, color)
    rect = rendered_text.get_rect(center=center)
    screen.blit(rendered_text, rect)

def draw_title(screen, text):
    draw_text(screen, text, largeFont, white, (width / 2, 50))

def draw_button(screen, text, rect, color=white, text_color=black):
    pygame.draw.rect(screen, color, rect)
    draw_text(screen, text, mediumFont, text_color, rect.center)

def draw_board(screen, board):
    tile_size = 80
    tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
    tiles = []

    for i in range(3):
        row = []
        for j in range(3):
            rect = pygame.Rect(
                tile_origin[0] + j * tile_size,
                tile_origin[1] + i * tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen, white, rect, 3)
            if board[i][j] != ttt.EMPTY:
                draw_text(screen, board[i][j], moveFont, white, rect.center)
            row.append(rect)
        tiles.append(row)
    return tiles

# Fonction principale
def main():
    global user, board, ai_turn
    running = True

    while running:
        screen.fill(black)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if user is None:
            # Écran de sélection du joueur
            draw_title(screen, "Play Tic-Tac-Toe")
            
            playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
            playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
            
            draw_button(screen, "Play as X", playXButton)
            draw_button(screen, "Play as O", playOButton)

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if playXButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = ttt.X
                elif playOButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = ttt.O
        else:
            # Jeu principal
            tiles = draw_board(screen, board)
            game_over = ttt.terminal(board)
            player = ttt.player(board)
            
            if game_over:
                winner = ttt.winner(board)
                title = f"Game Over: {winner} wins." if winner else "Game Over: Tie."
            elif user == player:
                title = f"Play as {user}"
            else:
                title = "Computer thinking..."
            draw_title(screen, title)

            # Mouvement de l'IA
            if user != player and not game_over:
                if ai_turn:
                    time.sleep(0.5)
                    move = ttt.minimax(board)
                    board = ttt.result(board, move)
                    ai_turn = False
                else:
                    ai_turn = True

            # Mouvement de l'utilisateur
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1 and user == player and not game_over:
                mouse = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                            board = ttt.result(board, (i, j))

            # Bouton "Play Again"
            if game_over:
                againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
                draw_button(screen, "Play Again", againButton)
                
                if click == 1:
                    mouse = pygame.mouse.get_pos()
                    if againButton.collidepoint(mouse):
                        time.sleep(0.2)
                        user = None
                        board = ttt.initial_state()
                        ai_turn = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
