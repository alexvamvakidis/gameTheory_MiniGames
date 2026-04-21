import pygame
import sys

import game1
import game2
import game3
import game4


pygame.init()

# Ρυθμίσεις οθόνης
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Made with Pygame")



# Χρώματα
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)
BLUE = (50, 100, 200)
TEXT_COLOR = (255, 255, 255)

font_title = pygame.font.SysFont("arial", 50, bold=True)
font_sub = pygame.font.SysFont("arial", 40,  italic=True)
font_button = pygame.font.SysFont("arial", 35, bold=True)

button_w, button_h = 400, 250
gap = 60 

start_x = (WIDTH - (2 * button_w + gap)) // 2
start_y = 180

buttons = [
    {"rect": pygame.Rect(start_x, start_y, button_w, button_h), "text": "NIM (Single collumn)", "id": 1},
    {"rect": pygame.Rect(start_x + button_w + gap, start_y, button_w, button_h), "text": "NIM (Triple collumn)", "id": 2},
    {"rect": pygame.Rect(start_x, start_y + button_h + gap, button_w, button_h), "text": "Tic-tac-toe 3x3", "id": 3},
    {"rect": pygame.Rect(start_x + button_w + gap, start_y + button_h + gap, button_w, button_h), "text": "Tic-tac-toe 4x4", "id": 4}
]

def draw_menu():
    screen.fill(WHITE)
    
    title = font_title.render("Game Theory - Mini Games", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, 40))
    subtitle_surface = font_sub.render("Select one of the games below:", True, BLACK)
    subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title, title_rect)
    screen.blit(subtitle_surface, subtitle_rect)

    for btn in buttons:
        shadow_rect = btn["rect"].copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (150, 150, 150), shadow_rect, border_radius=12)
        
        pygame.draw.rect(screen, BLUE, btn["rect"], border_radius=12)
        
        text_surface = font_button.render(btn["text"], True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=btn["rect"].center)
        screen.blit(text_surface, text_rect)

def main():
    running = True
    while running:
        hover = False
        draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        if btn["id"] == 1:
                            game1.play_game1(screen)
                        elif btn["id"] == 2:
                            game2.play_game2(screen)
                        elif btn["id"] == 3:
                            game3.play_game3(screen)
                        elif btn["id"] == 4:
                            game4.play_game4(screen)
                    
        if buttons[0]["rect"].collidepoint(pygame.mouse.get_pos()) or \
           buttons[1]["rect"].collidepoint(pygame.mouse.get_pos()) or \
           buttons[2]["rect"].collidepoint(pygame.mouse.get_pos()) or \
           buttons[3]["rect"].collidepoint(pygame.mouse.get_pos()):
            hover = True
        else:
            hover = False

        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()