import pygame
import random

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)
BLUE = (50, 100, 200)
RED = (200, 50, 50)
GREEN = (50, 180, 50)

def is_game_over(board):
    wins = [(0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15),
            (0,4,8,12), (1,5,9,13), (2,6,10,14), (3,7,11,15),
            (0,5,10,15), (3,6,9,12)]
    for a, b, c, d in wins:
        if board[a] == board[b] == board[c] == board[d] == 1:
            return True, [a, b, c, d]
    return False

def get_nim_value(board, memo):
    state = tuple(board)
    if state in memo:
        return memo[state]
        
    if is_game_over(board):
        return 0

    child_nims = set()
    for i in range(16):
        if board[i] == 0:
            board[i] = 1 
            child_nims.add(get_nim_value(board, memo)) 
            board[i] = 0 
            
    mex = 0
    while mex in child_nims:
        mex += 1
        
    memo[state] = mex
    return mex

def play_game4(screen):
    WIDTH, HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont("arial", 55, bold=True)
    font_button = pygame.font.SysFont("arial", 34, bold=True)
    font_label = pygame.font.SysFont("arial", 32)
    font_sub = pygame.font.SysFont("arial", 40, italic=True)
    font_large = pygame.font.SysFont("arial", 60, bold=True) 

    STATE_SETUP = "SETUP"
    STATE_PLAYING = "PLAYING"
    running_state = STATE_SETUP

    pvp = False

    board = [0] * 16      
    ui_board = [0] * 16   
    turn = "Player"
    winner = None
    pc_move_msg = ""
    computer_thinking_start = 0

    replay_btn = pygame.Rect(150, 20, 130, 40)
    back_btn = pygame.Rect(20, 20, 100, 40)

    #grid settings
    grid_size = 400
    start_x = WIDTH // 2 - grid_size // 2
    start_y = 180
    cell_size = grid_size // 4

    clock = pygame.time.Clock()
    running = True

    while running:
        hover = False
        screen.fill(WHITE)
        m_pos = pygame.mouse.get_pos()

        if running_state == STATE_SETUP:
            screen.blit(font_title.render("Tic-Tac-Toe 4x4", True, BLACK), (WIDTH//2 - 220, 80))
            screen.blit(font_sub.render("Select game mode and rules", True, BLACK), (WIDTH//2 - 270, 140))

            pvc_btn = pygame.Rect(250, 250, 220, 60)
            pvp_btn = pygame.Rect(530, 250, 220, 60)
            pygame.draw.rect(screen, BLUE if not pvp else GRAY, pvc_btn, border_radius=8)
            pygame.draw.rect(screen, BLUE if pvp else GRAY, pvp_btn, border_radius=8)
            screen.blit(font_button.render("vs PC", True, WHITE), (315, 265))
            screen.blit(font_button.render("vs Player", True, WHITE), (570, 265))

            start_btn = pygame.Rect(350, 450, 300, 70)
            pygame.draw.rect(screen, BLACK, start_btn, border_radius=15)
            screen.blit(font_button.render("START GAME", True, WHITE), (390, 470))

        elif running_state == STATE_PLAYING:
            if winner: 
                info_txt = f"WINNER: {winner}!" 
                txt = font_sub.render(info_txt, True, BLACK)
                screen.blit(txt, txt.get_rect(center=(WIDTH//2, 90 )))
            else: 
                info_txt = f"{turn}'s turn!"
                txt = font_sub.render(info_txt, True, BLUE)
                screen.blit(txt, txt.get_rect(center=(WIDTH//2, 90 )))


            if pc_move_msg:
                color = GRAY if "thinking" in pc_move_msg else RED
                screen.blit(font_label.render(pc_move_msg, True, color), (WIDTH//2 - 150, 110))

            # grid 4x4
            
            for i in range(1, 4):
                pygame.draw.line(screen, BLACK, (start_x + i * cell_size, start_y), (start_x + i * cell_size, start_y + grid_size), 5)
                pygame.draw.line(screen, BLACK, (start_x, start_y + i * cell_size), (start_x + grid_size, start_y + i * cell_size), 5)

        # marks
            for i in range(16):
                if ui_board[i] != 0:
                    row, col = divmod(i, 4)
                    cx = start_x + col * cell_size + cell_size // 2
                    cy = start_y + row * cell_size + cell_size // 2
                    if ui_board[i] == 1:
                        screen.blit(font_large.render("G", True, GREEN), (cx - 20, cy - 30))
                    else:
                        screen.blit(font_large.render("R", True, RED), (cx - 20, cy - 30))
                
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
                    board = [0] * 16
                    ui_board = [0] * 16
                    turn = "Player" if not pvp else "Green"
                    winner, pc_move_msg = None, ""

                if running_state == STATE_SETUP:
                    if pygame.Rect(250, 250, 220, 60).collidepoint(m_pos): pvp = False
                    if pygame.Rect(530, 250, 220, 60).collidepoint(m_pos): pvp = True
                    
                    if pygame.Rect(350, 450, 300, 70).collidepoint(m_pos):
                        board = [0] * 16
                        ui_board = [0] * 16
                        turn = "Player" if not pvp else "Green"
                        winner, pc_move_msg = None, ""
                        running_state = STATE_PLAYING

                elif running_state == STATE_PLAYING and not winner and turn != "Computer":
                    grid_size = 400
                    start_x = WIDTH // 2 - grid_size // 2
                    start_y = 180
                    cell_size = grid_size // 4
                    
                    if start_x <= m_pos[0] <= start_x + grid_size and start_y <= m_pos[1] <= start_y + grid_size:
                        col = (m_pos[0] - start_x) // cell_size
                        row = (m_pos[1] - start_y) // cell_size
                        idx = row * 4 + col
                        
                        if board[idx] == 0:
                            board[idx] = 1
                            ui_board[idx] = 1 if turn == "Player" or turn == "Green" else 2
                            
                            if is_game_over(board):
                                if turn == "Player": winner = "Player"
                                elif turn == "Green": winner = "Green"
                                elif turn == "Red": winner = "Red"
                            else:
                                if not pvp:
                                    turn = "Computer"
                                    pc_move_msg = "Computer is thinking..."
                                    computer_thinking_start = pygame.time.get_ticks()
                                else:
                                    turn = "Red" if turn == "Green" else "Green"
                                    pc_move_msg = ""

        # Computer Logic
        if running_state == STATE_PLAYING and turn == "Computer" and not winner:
            if pygame.time.get_ticks() - computer_thinking_start > 800:
                memo = {}
                best_move = -1
                empty_cells = [i for i in range(16) if board[i] == 0]
                
                for cell in empty_cells:
                    board[cell] = 1
                    nim_value = get_nim_value(board, memo)
                    board[cell] = 0 
                    
                    if nim_value == 0:
                        best_move = cell
                        break 
                        
                if best_move == -1 and empty_cells:
                    best_move = random.choice(empty_cells)
                    
                board[best_move] = 1
                ui_board[best_move] = 2 
                pc_move_msg = ""
                
                if is_game_over(board):
                    winner = "Computer"
                elif 0 not in board:
                    winner = "Draw"
                else:
                    turn = "Player"
        if running_state == STATE_PLAYING and winner:
            win_cells = is_game_over(board)[1]
            x1 = start_x + (win_cells[0] % 4) * cell_size + cell_size // 2
            y1 = start_y + (win_cells[0] // 4) * cell_size + cell_size // 2
            x2 = start_x + (win_cells[3] % 4) * cell_size + cell_size // 2
            y2 = start_y + (win_cells[3] // 4) * cell_size + cell_size // 2

            ext = 40 
            diff = win_cells[1] - win_cells[0] 
            if diff == 1:   
                x1 -= ext   
                x2 += ext   
                
            elif diff == 4: 
                y1 -= ext   
                y2 += ext   
                
            elif diff == 5: 
                x1 -= ext; y1 -= ext
                x2 += ext; y2 += ext
                
            elif diff == 3: 
                x1 += ext; y1 -= ext
                x2 -= ext; y2 += ext
                            
            pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 10) 
        if running_state == STATE_SETUP:
            if pvc_btn.collidepoint(m_pos) or pvp_btn.collidepoint(m_pos) or start_btn.collidepoint(m_pos) or back_btn.collidepoint(m_pos):
                hover = True
            else:
                hover = False
        elif running_state == STATE_PLAYING:
            if replay_btn.collidepoint(m_pos) or back_btn.collidepoint(m_pos) or (not winner and turn != "Computer" and start_x <= m_pos[0] <= start_x + grid_size and start_y <= m_pos[1] <= start_y + grid_size):
                hover = True
            else:
                hover = False
        
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        clock.tick(60)