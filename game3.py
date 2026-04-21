import pygame
import random

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)
BLUE = (50, 100, 200)
RED = (200, 50, 50)
GREEN = (50, 180, 50)

def is_game_over(board):
    return ((board[0] == 1 and board[1] == 1 and board[2] == 1) or 
            (board[3] == 1 and board[4] == 1 and board[5] == 1) or 
            (board[6] == 1 and board[7] == 1 and board[8] == 1) or 
            (board[0] == 1 and board[3] == 1 and board[6] == 1) or 
            (board[1] == 1 and board[4] == 1 and board[7] == 1) or 
            (board[2] == 1 and board[5] == 1 and board[8] == 1) or 
            (board[0] == 1 and board[4] == 1 and board[8] == 1) or 
            (board[2] == 1 and board[4] == 1 and board[6] == 1))

def get_nim_value(board, memo, gameType):
    state = tuple(board)
    if state in memo: return memo[state]

    if is_game_over(board):
        return 0 if gameType == 1 else 1  

    child_nims = set()
    for i in range(9):
        if board[i] == 0:
            board[i] = 1 
            child_nims.add(get_nim_value(board, memo, gameType)) 
            board[i] = 0 
            
    mex = 0
    while mex in child_nims:
        mex += 1

    memo[state] = mex
    return mex

def play_game3(screen):
    WIDTH, HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont("arial", 55, bold=True)
    font_sub = pygame.font.SysFont("arial", 40, bold=True)
    font_button = pygame.font.SysFont("arial", 34, bold=True)
    font_label = pygame.font.SysFont("arial", 32)
    font_large = pygame.font.SysFont("arial", 80, bold=True)

    STATE_SETUP = "SETUP"
    STATE_PLAYING = "PLAYING"
    running_state = STATE_SETUP

    pvp = False
    classic = True

    board = [0] * 9      
    ui_board = [0] * 9   
    turn = "Player"
    winner = None
    pc_move_msg = ""
    computer_thinking_start = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        m_pos = pygame.mouse.get_pos()

        if running_state == STATE_SETUP:
            screen.blit(font_title.render("Tic-Tac-Toe 3x3", True, BLACK), (WIDTH//2 - 220, 80))
            screen.blit(font_sub.render("Select game mode and rules", True, BLACK), (WIDTH//2 - 270, 140))

            pvc_btn = pygame.Rect(250, 220, 220, 60)
            pvp_btn = pygame.Rect(530, 220, 220, 60)
            pygame.draw.rect(screen, BLUE if not pvp else GRAY, pvc_btn, border_radius=8)
            pygame.draw.rect(screen, BLUE if pvp else GRAY, pvp_btn, border_radius=8)
            screen.blit(font_button.render("vs PC", True, WHITE), (315, 235))
            screen.blit(font_button.render("vs Player", True, WHITE), (570, 235))

            classic_btn = pygame.Rect(250, 320, 220, 60)
            misere_btn = pygame.Rect(530, 320, 220, 60)
            pygame.draw.rect(screen, GREEN if classic else GRAY, classic_btn, border_radius=8)
            pygame.draw.rect(screen, GREEN if not classic else GRAY, misere_btn, border_radius=8)
            screen.blit(font_button.render("Classic", True, WHITE), (305, 335))
            screen.blit(font_button.render("Misere", True, WHITE), (590, 335))

            start_btn = pygame.Rect(350, 500, 300, 70)
            pygame.draw.rect(screen, BLACK, start_btn, border_radius=15)
            screen.blit(font_button.render("START GAME", True, WHITE), (390, 520))

        elif running_state == STATE_PLAYING:
            info_txt = f"{turn}'s turn!" if not winner else f"WINNER: {winner}!"
            screen.blit(font_sub.render(info_txt, True, BLUE), (WIDTH//2 - 130, 80))

            if pc_move_msg:
                color = GRAY if "thinking" in pc_move_msg else RED
                screen.blit(font_label.render(pc_move_msg, True, color), (WIDTH//2 - 150, 130))

            # draw grid
            start_x = WIDTH // 2 - 150
            start_y = 220
            cell_size = 100

            for i in range(1, 3):
                pygame.draw.line(screen, BLACK, (start_x + i * cell_size, start_y), (start_x + i * cell_size, start_y + 300), 5)
                pygame.draw.line(screen, BLACK, (start_x, start_y + i * cell_size), (start_x + 300, start_y + i * cell_size), 5)

            # draw marks
            for i in range(9):
                if ui_board[i] != 0:
                    row, col = divmod(i, 3)
                    cx = start_x + col * cell_size + cell_size // 2
                    cy = start_y + row * cell_size + cell_size // 2
                    if ui_board[i] == 1:
                        screen.blit(font_large.render("G", True, GREEN), (cx - 25, cy - 45))
                    else:
                        screen.blit(font_large.render("R", True, RED), (cx - 30, cy - 45))
            
            # replay button
            replay_btn = pygame.Rect(150, 20, 130, 40)
            pygame.draw.rect(screen, GREEN, replay_btn, border_radius=5)
            screen.blit(font_label.render("Replay", True, WHITE), (165, 25))


        back_btn = pygame.Rect(20, 20, 100, 40)
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
                    board = [0] * 9
                    ui_board = [0] * 9
                    turn = "Player" if not pvp else "Green"
                    winner, pc_move_msg = None, ""

                if running_state == STATE_SETUP:
                    if pygame.Rect(250, 200, 220, 60).collidepoint(m_pos): pvp = False
                    if pygame.Rect(530, 200, 220, 60).collidepoint(m_pos): pvp = True
                    if pygame.Rect(250, 300, 220, 60).collidepoint(m_pos): classic = True
                    if pygame.Rect(530, 300, 220, 60).collidepoint(m_pos): classic = False
                    
                    if pygame.Rect(350, 500, 300, 70).collidepoint(m_pos):
                        board = [0] * 9
                        ui_board = [0] * 9
                        turn = "Player" if not pvp else "Green"
                        winner, pc_move_msg = None, ""
                        running_state = STATE_PLAYING

                elif running_state == STATE_PLAYING and not winner and turn != "Computer":
                    start_x = WIDTH // 2 - 150
                    start_y = 220
                    cell_size = 100
                    
                    if start_x <= m_pos[0] <= start_x + 300 and start_y <= m_pos[1] <= start_y + 300:
                        col = (m_pos[0] - start_x) // cell_size
                        row = (m_pos[1] - start_y) // cell_size
                        idx = row * 3 + col
                        
                        if board[idx] == 0:
                            board[idx] = 1
                            ui_board[idx] = 1 if turn == "Player" or turn == "Green" else 2
                            
                            if is_game_over(board):
                                if turn == "Player": winner = "Player" if classic else "Computer"
                                elif turn == "Green": winner = "Green" if classic else "Red"
                                elif turn == "Red": winner = "Red" if classic else "Green"
                            else:
                                if not pvp:
                                    turn = "Computer"
                                    pc_move_msg = "Computer is thinking..."
                                    computer_thinking_start = pygame.time.get_ticks()
                                else:
                                    turn = "Red" if turn == "Green" else "Green"
                                    pc_move_msg = ""
                                

        if running_state == STATE_PLAYING and turn == "Computer" and not winner:
            if pygame.time.get_ticks() - computer_thinking_start > 800:
                memo = {}
                
                best_move = -1
                empty_cells = [i for i in range(9) if board[i] == 0]
                
                for cell in empty_cells:
                    board[cell] = 1
                    nim_value = get_nim_value(board, memo, classic)
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
                    winner = "Computer" if classic else "Player"
                else:
                    turn = "Player"

        pygame.display.flip()
        clock.tick(60)