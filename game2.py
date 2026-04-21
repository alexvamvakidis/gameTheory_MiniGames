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

def draw_sticks(screen, count, center_x, start_y):
    for i in range(count):
        x_pos = center_x - (count * 20) // 2 + i * 20
        pygame.draw.rect(screen, WOOD_COLOR, (x_pos, start_y + 15, 12, 140), border_radius=3)
        pygame.draw.rect(screen, MATCH_HEAD, (x_pos - 2, start_y, 16, 20), border_radius=6)

def play_game2(screen):
    WIDTH, HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont("arial", 55, bold=True)
    font_sub = pygame.font.SysFont("arial", 40, italic=True)
    font_button = pygame.font.SysFont("arial", 34, bold=True)
    font_label = pygame.font.SysFont("arial", 32)
    font_error = pygame.font.SysFont("arial", 28, italic=True)

    STATE_SETUP = "SETUP"
    STATE_PLAYING = "PLAYING"
    running_state = STATE_SETUP

    pvp = False
    numSticks1, numSticks2, numSticks3, maxNumRemovedSticks = "10", "10", "10", "4"
    active_box = None
    error_msg = ""

    sticks = [10, 10, 10]
    max_remove = 4
    turn = "Player"
    winner = None
    pc_move_msg = ""
    computer_thinking_start = 0
    selected_col = 0 
    col_centers = [250, 500, 750]

    clock = pygame.time.Clock()
    running = True

    replay_btn = pygame.Rect(150, 20, 130, 40)
    back_btn = pygame.Rect(20, 20, 100, 40)

    while running:

        hover = False
        screen.fill(WHITE)
        m_pos = pygame.mouse.get_pos()

        if running_state == STATE_SETUP:
            screen.blit(font_title.render("Triple Column NIM Game", True, BLACK), (WIDTH//2 - 320, 80))
            screen.blit(font_sub.render("Select game mode and rules", True, BLACK), (WIDTH//2 - 270, 140))

            pvc_btn = pygame.Rect(250, 210, 220, 60)
            pvp_btn = pygame.Rect(530, 210, 220, 60)
            pygame.draw.rect(screen, BLUE if not pvp else GRAY, pvc_btn, border_radius=8)
            pygame.draw.rect(screen, BLUE if pvp else GRAY, pvp_btn, border_radius=8)
            screen.blit(font_button.render("vs PC", True, WHITE), (315, 225))
            screen.blit(font_button.render("vs Player", True, WHITE), (570, 225))

            labels = ["Column 1 (8-11):", "Column 2 (8-11):", "Column 3 (8-11):", "Max Remove (2-5):"]
            boxes = [
                pygame.Rect(580, 310, 100, 40), pygame.Rect(580, 370, 100, 40),
                pygame.Rect(580, 430, 100, 40), pygame.Rect(580, 490, 100, 40)
            ]
            inputs = [numSticks1, numSticks2, numSticks3, maxNumRemovedSticks]
            keys = ['c1', 'c2', 'c3', 'm']

            for i, label in enumerate(labels):
                screen.blit(font_label.render(label, True, BLACK), (300, 315 + i * 60))
                pygame.draw.rect(screen, LIGHT_BLUE if active_box == keys[i] else WHITE, boxes[i])
                pygame.draw.rect(screen, BLACK, boxes[i], 2)
                screen.blit(font_label.render(inputs[i], True, BLACK), (boxes[i].x + 10, boxes[i].y + 5))

            if error_msg:
                screen.blit(font_error.render(error_msg, True, RED), (WIDTH//2 - 90, 540))

            start_btn = pygame.Rect(350, 580, 300, 70)
            pygame.draw.rect(screen, BLACK, start_btn, border_radius=15)
            screen.blit(font_button.render("START GAME", True, WHITE), (390, 600))

        elif running_state == STATE_PLAYING:
            if winner: 
                info_txt = f"WINNER: {winner}!" 
                txt = font_title.render(info_txt, True, BLACK)
                screen.blit(txt, txt.get_rect(center=(WIDTH//2, 400 )))
            else: 
                info_txt = f"{turn}'s turn!"
                txt = font_sub.render(info_txt, True, BLUE)
                screen.blit(txt, txt.get_rect(center=(WIDTH//2, 90 )))
            
            if pc_move_msg:
                color = GRAY if "thinking" in pc_move_msg else RED
                width = (WIDTH//2 - 110, 130) if "thinking" in pc_move_msg else (WIDTH//2 - 270, 130)
                screen.blit(font_label.render(pc_move_msg, True, color), width)

            col_centers = [250, 500, 750]
            if not winner:
                for i in range(3):
                    draw_sticks(screen, sticks[i], col_centers[i], 220)
                                                                                
                    col_btn = pygame.Rect(col_centers[i] - 100, 400, 190, 50)
                    btn_color = GREEN if selected_col == i else GRAY
                    pygame.draw.rect(screen, btn_color, col_btn, border_radius=5)
                    screen.blit(font_label.render(f"Col {i+1} ({sticks[i]})", True, BLACK), (col_centers[i] - 65, 410))

            if not winner and turn != "Computer":
                for i in range(1, max_remove + 1):
                    btn = pygame.Rect(WIDTH//2 - 370 + (i-1)*190, 550, 170, 50)
                    valid_move = sticks[selected_col] >= i
                    pygame.draw.rect(screen, BLUE if valid_move else GRAY, btn, border_radius=5)
                    screen.blit(font_label.render(f"Remove {i}", True, WHITE), (btn.x + 15, btn.y + 10))
            
            # replay button
            pygame.draw.rect(screen, GREEN, replay_btn, border_radius=5)
            screen.blit(font_label.render("Replay", True, WHITE), (165, 25))

        #back button
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
                    winner, error_msg, pc_move_msg = None, "", ""
                    sticks = [int(numSticks1), int(numSticks2), int(numSticks3)]

                if running_state == STATE_SETUP:
                    pvc_btn = pygame.Rect(250, 210, 220, 60)
                    pvp_btn = pygame.Rect(530, 210, 220, 60)
                    if pvc_btn.collidepoint(m_pos): pvp = False
                    if pvp_btn.collidepoint(m_pos): pvp = True
                    
                    boxes = [pygame.Rect(580, 310+i*60, 100, 40) for i in range(4)]
                    keys = ['c1', 'c2', 'c3', 'm']
                    clicked_box = False
                    for i, box in enumerate(boxes):
                        if box.collidepoint(m_pos):
                            active_box = keys[i]
                            clicked_box = True
                    if not clicked_box and not pvc_btn.collidepoint(m_pos) and not pvp_btn.collidepoint(m_pos):
                        active_box = None
                    
                    start_btn = pygame.Rect(350, 580, 300, 70)
                    if start_btn.collidepoint(m_pos):
                        try:
                            c1, c2, c3, m = int(numSticks1), int(numSticks2), int(numSticks3), int(maxNumRemovedSticks)
                            if all(8 <= x <= 11 for x in [c1, c2, c3]) and 2 <= m <= 5:
                                sticks = [c1, c2, c3]
                                max_remove = m
                                turn = "Player" if not pvp else "Green"
                                winner, error_msg, pc_move_msg = None, "", ""
                                running_state = STATE_PLAYING
                            else: error_msg = "Invalid bounds!"
                        except: error_msg = "Enter numbers!"

                elif running_state == STATE_PLAYING and not winner and turn != "Computer":
                    
                    for i in range(3):
                        if pygame.Rect(col_centers[i] - 100, 400, 190, 50).collidepoint(m_pos):
                            selected_col = i

                    for i in range(1, max_remove + 1):
                        btn = pygame.Rect(WIDTH//2 - 370 + (i-1)*190, 550, 170, 50)
                        if btn.collidepoint(m_pos) and sticks[selected_col] >= i:
                            sticks[selected_col] -= i
                            if sum(sticks) == 0:
                                if turn == "Player": winner = "Player" 
                                elif turn == "Green": winner = "Green" 
                                elif turn == "Red": winner = "Red"
                                pc_move_msg = ""
                            else:
                                if not pvp:
                                    turn = "Computer"
                                    pc_move_msg = "Computer is thinking..."
                                    computer_thinking_start = pygame.time.get_ticks()
                                else:
                                    turn = "Red" if turn == "Green" else "Green"
                                    pc_move_msg = ""
               

            if event.type == pygame.KEYDOWN and running_state == STATE_SETUP and active_box:
                if event.key == pygame.K_BACKSPACE:
                    if active_box == 'c1': numSticks1 = numSticks1[:-1]
                    elif active_box == 'c2': numSticks2 = numSticks2[:-1]
                    elif active_box == 'c3': numSticks3 = numSticks3[:-1]
                    elif active_box == 'm': maxNumRemovedSticks = maxNumRemovedSticks[:-1]
                else:
                    if active_box == 'c1': numSticks1 += event.unicode
                    elif active_box == 'c2': numSticks2 += event.unicode
                    elif active_box == 'c3': numSticks3 += event.unicode
                    elif active_box == 'm': maxNumRemovedSticks += event.unicode

        if running_state == STATE_PLAYING and turn == "Computer" and not winner:
            if pygame.time.get_ticks() - computer_thinking_start > 1200:
                mex1 = sticks[0] % (max_remove + 1)
                mex2 = sticks[1] % (max_remove + 1)
                mex3 = sticks[2] % (max_remove + 1)
                nim_sum = mex1 ^ mex2 ^ mex3
                
                col_removed = -1
                removed_amount = 0

                if nim_sum != 0:          
                    if mex1 ^ nim_sum < mex1:
                        removed_amount = mex1 - (mex1 ^ nim_sum)
                        sticks[0] -= removed_amount
                        col_removed = 1
                    elif mex2 ^ nim_sum < mex2:
                        removed_amount = mex2 - (mex2 ^ nim_sum)
                        sticks[1] -= removed_amount
                        col_removed = 2
                    else:
                        removed_amount = mex3 - (mex3 ^ nim_sum)
                        sticks[2] -= removed_amount
                        col_removed = 3
                else:
                    valid_cols = [i for i in range(3) if sticks[i] > 0]
                    col_idx = random.choice(valid_cols)
                    removed_amount = random.randint(1, min(max_remove, sticks[col_idx]))
                    sticks[col_idx] -= removed_amount
                    col_removed = col_idx + 1

                pc_move_msg = f"Computer removed {removed_amount} stick(s) from Column {col_removed}"
                
                if sum(sticks) == 0: 
                    winner = "Computer"
                else: 
                    turn = "Player"
        if running_state == STATE_SETUP:
            if pvc_btn.collidepoint(m_pos) or pvp_btn.collidepoint(m_pos) or back_btn.collidepoint(m_pos) or\
                start_btn.collidepoint(m_pos) or any(box.collidepoint(m_pos) for box in [pygame.Rect(580, 310+i*60, 100, 40) for i in range(4)]):   
                hover = True   
            else:  
                hover = False     
        if running_state == STATE_PLAYING:
            if replay_btn.collidepoint(m_pos) or back_btn.collidepoint(m_pos)\
                or (not winner and turn != "Computer" and any(pygame.Rect(col_centers[i] - 100, 400, 190, 50).collidepoint(m_pos) for i in range(3)))\
                or (not winner and turn != "Computer" and any(pygame.Rect(WIDTH//2 - 370 + (i-1)*190, 550, 170, 50).collidepoint(m_pos) for i in range(1, max_remove + 1))):
                hover = True
            else:
                hover = False
            
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        clock.tick(60)