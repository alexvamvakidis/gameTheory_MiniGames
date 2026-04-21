import pygame
import random

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)
BLUE = (50, 100, 200)
RED = (200, 50, 50)
GREEN = (50, 180, 50)
LIGHT_BLUE = (100, 150, 255)
WOOD_COLOR = (222, 184, 135)  
MATCH_HEAD = (200, 40, 40)



def play_game1(screen):
    
    WIDTH, HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont("arial", 55, bold=True)
    font_sub = pygame.font.SysFont("arial", 40, italic=True)
    font_button = pygame.font.SysFont("arial", 34, bold=True)
    font_label = pygame.font.SysFont("arial", 32)
    font_error = pygame.font.SysFont("arial", 28, italic=True)

    STATE_SETUP = "SETUP"
    STATE_PLAYING = "PLAYING"
    running_state = STATE_SETUP

    pvp = True
    classic = True
    numSticks = "16"
    maxNumRemovedSticks = "4"
    active_box = None
    error_msg = ""

    sticks = 16
    max_remove = 4
    turn = "Green"
    winner = None
    pc_move_msg = ""
    
    computer_thinking_start = 0 

    clock = pygame.time.Clock()
    running = True

    replay_btn = pygame.Rect(150, 20, 130, 40)
    back_btn = pygame.Rect(20, 20, 100, 40)

    while running:
        hover = False
        screen.fill(WHITE)
        m_pos = pygame.mouse.get_pos()

        if running_state == STATE_SETUP:

            screen.blit(font_title.render("Single Column NIM Game", True, BLACK), (WIDTH//2 - 320, 80))
            screen.blit(font_sub.render("Select game mode and rules", True, BLACK), (WIDTH//2 - 270, 140))

            # buttons
            pvc_btn = pygame.Rect(260, 210, 220, 65)
            pvp_btn = pygame.Rect(540, 210, 220, 65)
            pygame.draw.rect(screen, BLUE if not pvp else GRAY, pvc_btn, border_radius=8)
            pygame.draw.rect(screen, BLUE if pvp else GRAY, pvp_btn, border_radius=8)
            screen.blit(font_button.render("vs PC", True, WHITE), font_button.render("vs PC", True, WHITE).get_rect(center=pvc_btn.center))
            screen.blit(font_button.render("vs Player", True, WHITE), font_button.render("vs Player", True, WHITE).get_rect(center=pvp_btn.center))

            classic_btn = pygame.Rect(260, 300, 220, 65)
            misere_btn = pygame.Rect(540, 300, 220, 65)
            pygame.draw.rect(screen, GREEN if classic else GRAY, classic_btn, border_radius=8)
            pygame.draw.rect(screen, GREEN if not classic else GRAY, misere_btn, border_radius=8)
            screen.blit(font_button.render("Classic", True, WHITE), font_button.render("Classic", True, WHITE).get_rect(center=classic_btn.center))
            screen.blit(font_button.render("Misere", True, WHITE), font_button.render("Misere", True, WHITE).get_rect(center=misere_btn.center))

            # inputs
            s_label = font_label.render("Sticks (16-25):", True, BLACK)
            m_label = font_label.render("Max Remove (2-5):", True, BLACK)
            screen.blit(s_label, (260, 420))
            screen.blit(m_label, (260, 480))
            s_box = pygame.Rect(550, 415, 200, 40)
            m_box = pygame.Rect(550, 475, 200, 40)
            pygame.draw.rect(screen, WHITE if active_box != 's' else LIGHT_BLUE, s_box)
            pygame.draw.rect(screen, BLACK, s_box, 2)
            pygame.draw.rect(screen, WHITE if active_box != 'm' else LIGHT_BLUE, m_box)
            pygame.draw.rect(screen, BLACK, m_box, 2)
            screen.blit(font_button.render(numSticks, True, BLACK), (555 , 420))
            screen.blit(font_button.render(maxNumRemovedSticks, True, BLACK), (555, 480))
            
            if error_msg:
                err = font_error.render(error_msg, True, RED)
                screen.blit(err, err.get_rect(center=(WIDTH//2, 540)))

            start_btn = pygame.Rect(350, 600, 300, 70)
            pygame.draw.rect(screen, BLACK, start_btn, border_radius=15)
            start_txt = font_button.render("START GAME", True, WHITE)
            screen.blit(start_txt, start_txt.get_rect(center=start_btn.center))

        elif running_state == STATE_PLAYING:
            draw_sticks(screen, sticks, WIDTH, HEIGHT)

            if winner: 
                info_txt = f"WINNER: {winner}!" 
                txt = font_title.render(info_txt, True, BLACK)
                screen.blit(txt, txt.get_rect(center=(WIDTH//2, 400 )))
            else: 
                info_txt = f"{sticks} stick(s) left | {turn}'s turn!"
                txt = font_sub.render(info_txt, True, BLUE)
                screen.blit(txt, txt.get_rect(center=(WIDTH//2, 150 )))

            if pc_move_msg:
                color = GRAY if "thinking" in pc_move_msg else RED
                msg_surf = font_label.render(pc_move_msg, True, color)
                screen.blit(msg_surf, msg_surf.get_rect(center=(WIDTH//2, 190)))

            # take button
            if not winner and turn != "Computer":
                for i in range(1, max_remove + 1):
                    btn = pygame.Rect(WIDTH//2 - 350 + (i-1)*190, 600, 170, 50)
                    pygame.draw.rect(screen, BLUE if sticks >= i else GRAY, btn, border_radius=5)
                    t_txt = font_label.render(f"Remove {i}", True, WHITE)
                    screen.blit(t_txt, t_txt.get_rect(center=btn.center))

            # replay button
            pygame.draw.rect(screen, GREEN, replay_btn, border_radius=5)
            screen.blit(font_label.render("Replay", True, WHITE), (165, 25))

        # back button
        pygame.draw.rect(screen, RED, back_btn, border_radius=5)
        screen.blit(font_label.render("Back", True, WHITE), (35, 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(m_pos):
                    if running_state == STATE_PLAYING:
                        running_state = STATE_SETUP
                    else:
                        return 
             
                if running_state == STATE_PLAYING and replay_btn.collidepoint(m_pos):
                    turn = "Player" if not pvp else "Green"
                    winner, error_msg = None, ""
                    pc_move_msg = ""
                    sticks = int(numSticks)

                if running_state == STATE_SETUP:
                    if pvc_btn.collidepoint(m_pos): pvp = False
                    if pvp_btn.collidepoint(m_pos): pvp = True
                    if classic_btn.collidepoint(m_pos): classic = True
                    if misere_btn.collidepoint(m_pos): classic = False
                    if s_box.collidepoint(m_pos): active_box = 's'
                    elif m_box.collidepoint(m_pos): active_box = 'm'
                    else: active_box = None
                    
                    if start_btn.collidepoint(m_pos):
                        try:
                            s, m = int(numSticks), int(maxNumRemovedSticks)
                            if 16 <= s <= 25 and 2 <= m <= 5:
                                sticks, max_remove = s, m
                                turn = "Player" if not pvp else "Green"
                                winner, error_msg = None, ""
                                pc_move_msg = ""
                                running_state = STATE_PLAYING
                            else: error_msg = "Invalid Bounds!"
                        except: error_msg = "Enter numbers!"

                elif running_state == STATE_PLAYING and not winner and turn != "Computer":
                    for i in range(1, max_remove + 1):
                        btn = pygame.Rect(WIDTH//2 - 350 + (i-1)*190, 600, 170, 50)
                        if btn.collidepoint(m_pos) and sticks >= i:
                            sticks -= i
                            if sticks == 0:
                                if turn == "Player": winner = "Player" if classic else "Computer"
                                elif turn == "Green": winner = "Green" if classic else "Red"
                                elif turn == "Red": winner = "Red" if classic else "Green"
                                pc_move_msg = ""
                            else:
                                if not pvp:
                                    turn = "Computer"
                                    pc_move_msg = "Computer is thinking..."
                                    computer_thinking_start = pygame.time.get_ticks()
                                else:
                                    turn = "Red" if turn == "Green" else "Green"
                                    pc_move_msg = ""
                
                

            if event.type == pygame.KEYDOWN and running_state == STATE_SETUP:
                if active_box == 's':
                    if event.key == pygame.K_BACKSPACE: numSticks = numSticks[:-1]
                    else: numSticks += event.unicode
                elif active_box == 'm':
                    if event.key == pygame.K_BACKSPACE: maxNumRemovedSticks = maxNumRemovedSticks[:-1]
                    else: maxNumRemovedSticks += event.unicode
                    
        # Computer Logic 
        if running_state == STATE_PLAYING and turn == "Computer" and not winner:
            if pygame.time.get_ticks() - computer_thinking_start > 1200:
                if classic:
                    move = sticks % (max_remove + 1) or random.randint(1, min(max_remove, sticks))
                else:
                    move = (sticks - 1) % (max_remove + 1) or random.randint(1, min(max_remove, sticks))
                
                actual_move = min(move, sticks)
                sticks -= actual_move
                
                pc_move_msg = f"Computer removed {actual_move} stick(s)"
                
                if sticks == 0: 
                    winner = "Computer" if classic else "Player"
                    
                else: 
                    turn = "Player" 
        
        if running_state == STATE_SETUP:
            if pvc_btn.collidepoint(m_pos) or pvp_btn.collidepoint(m_pos) or back_btn.collidepoint(m_pos) or\
                classic_btn.collidepoint(m_pos) or misere_btn.collidepoint(m_pos) or start_btn.collidepoint(m_pos)\
                    or s_box.collidepoint(m_pos) or m_box.collidepoint(m_pos):
                hover = True
            else: hover = False

        if running_state == STATE_PLAYING:
            if replay_btn.collidepoint(m_pos) or back_btn.collidepoint(m_pos)\
                or (not winner and turn != "Computer" and any(pygame.Rect(WIDTH//2 - 350 + (i-1)*190, 600, 170, 50).collidepoint(m_pos) for i in range(1, max_remove + 1))):
                hover = True
            else:
                hover = False

        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
                    

        pygame.display.flip()
        clock.tick(60)

    

def draw_sticks(screen, count, W, H):
    for i in range(count):
        x_pos = W//2.4 - (count*15)//2 + i*28
        y_pos = 280
        
        pygame.draw.rect(screen, WOOD_COLOR, (x_pos, y_pos + 15, 15, 175), border_radius=3)
        pygame.draw.rect(screen, MATCH_HEAD, (x_pos - 2, y_pos, 19, 25), border_radius=8)