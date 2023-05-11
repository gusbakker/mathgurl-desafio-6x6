import pygame
import pygame.freetype

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Font setup
font = pygame.freetype.SysFont(None, 24)

# Grid setup
grid = [[0 for _ in range(6)] for _ in range(6)]
cell_size = 100  # Size of a cell in pixels


def draw_panel():
    panel_rect = pygame.Rect(600, 0, 200, 600)
    pygame.draw.rect(screen, (100, 100, 100), panel_rect)

    quit_button = pygame.Rect(650, 100, 100, 50)
    pygame.draw.rect(screen, (200, 0, 0), quit_button)
    text_surface, _ = font.render("QUIT", (0, 0, 0))
    screen.blit(text_surface, (quit_button.x + 20, quit_button.y + 10))

    solve_button = pygame.Rect(650, 200, 100, 50)
    pygame.draw.rect(screen, (0, 200, 0), solve_button)
    text_surface, _ = font.render("SOLVE", (0, 0, 0))
    screen.blit(text_surface, (solve_button.x + 10, solve_button.y + 10))

    # Add reset button
    reset_button = pygame.Rect(650, 300, 100, 50)
    pygame.draw.rect(screen, (0, 0, 200), reset_button)
    text_surface, _ = font.render("RESET", (0, 0, 0))
    screen.blit(text_surface, (reset_button.x + 10, reset_button.y + 10))


def handle_click(pos):
    # Adjust function to not return cell coordinates when clicking outside of the grid (in the panel)
    if pos[0] < 600 and pos[1] < 600:
        i, j = pos[0] // cell_size, pos[1] // cell_size
        return i, j
    else:
        return None


def check_button_click(pos):
    if 650 < pos[0] < 750 and 100 < pos[1] < 150:
        return 'quit'
    elif 650 < pos[0] < 750 and 200 < pos[1] < 250:
        return 'solve'
    # Check if reset button was clicked
    elif 650 < pos[0] < 750 and 300 < pos[1] < 350:
        return 'reset'
    return None


# Function to reset the grid
def reset_grid():
    global grid
    grid = [[0 for _ in range(6)] for _ in range(6)]


def draw_grid():
    for i in range(6):
        for j in range(6):
            rect = pygame.Rect(i * cell_size, j * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

            if grid[i][j] != 0:
                text_surface, _ = font.render(str(grid[i][j]), (0, 0, 0))
                screen.blit(text_surface, (i * cell_size + cell_size // 2, j * cell_size + cell_size // 2))


def draw_input_box():
    input_rect = pygame.Rect(0, 600 - cell_size, 600, cell_size)
    pygame.draw.rect(screen, (255, 255, 255), input_rect)
    text_surface, _ = font.render("Enter a number (1-8):", (0, 0, 0))
    screen.blit(text_surface, (10, 600 - cell_size + 10))


def draw_warning_box():
    warning_rect = pygame.Rect(0, 600 - cell_size, 600, cell_size)
    pygame.draw.rect(screen, (255, 255, 255), warning_rect)
    text_surface, _ = font.render("Distance should be greater!", (0, 0, 0))
    screen.blit(text_surface, (10, 600 - cell_size + 10))


def calculate_distance(i, j, number):
    for x in range(6):
        for y in range(6):
            if grid[x][y] == number and (x != i or y != j):
                if abs(x - i) + abs(y - j) <= number:
                    return True
    return False


def solve_puzzle():
    for i in range(6):
        for j in range(6):
            if grid[i][j] == 0:  # If the cell is empty
                for number in range(1, 9):
                    if not calculate_distance(i, j, number):
                        grid[i][j] = number
                        if solve_puzzle():
                            return True
                        grid[i][j] = 0  # Reset cell if no valid number can be placed
                return False  # Trigger backtracking from previous cell
    return True  # Return True when all cells are filled


i, j = 0, 0
running = True
waiting_for_input = False
warning = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button = check_button_click(pygame.mouse.get_pos())
                if button == 'quit':
                    running = False
                elif button == 'solve':
                    solve_puzzle()
                elif button == 'reset':
                    reset_grid()
                else:
                    cell = handle_click(pygame.mouse.get_pos())
                    if cell is not None:
                        i, j = cell
                        waiting_for_input = True
                        warning = False
        elif event.type == pygame.KEYDOWN and waiting_for_input:
            if event.unicode.isdigit() and int(event.unicode) in range(1, 9):
                if not calculate_distance(i, j, int(event.unicode)):
                    grid[i][j] = int(event.unicode)
                    waiting_for_input = False
                else:
                    warning = True
                    waiting_for_input = False

    screen.fill((200, 200, 200))
    draw_grid()
    draw_panel()

    if waiting_for_input:
        draw_input_box()
    elif warning:
        draw_warning_box()

    pygame.display.flip()

pygame.quit()
