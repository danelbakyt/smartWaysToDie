import pygame
import sys

# Initialize Pygame
pygame.init()

# Window setup
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Smart Ways To Die")

player_img = pygame.image.load("images/happy.png")
player_img = pygame.transform.scale(player_img, (40, 40))
player = pygame.Rect(100, 100, 40, 40)  # keep this for collision/movement
grass_img = pygame.image.load("images/grass.jpeg")

roomWidth = 300
roomHeight = 200
doorSize = 50
wallWidth = 10

assetWidth = 70
assetHeight = 120
# Score system
score = 0
font = pygame.font.Font("pixelfont.ttf", 24)
bigfont = pygame.font.Font("pixelfont.ttf", 66)

def reset_game():
    global player, score, running, startTime

    player = pygame.Rect(100, 100, 40, 40)
    score = 0
    running = True
    startTime = pygame.time.get_ticks()


#start screen
def startScreen():
    while True:
        screen.fill((20, 20, 20))
        title = bigfont.render("SMART WAYS TO DIE", True, (255, 255, 255))
        d1 = font.render("Find the smartest and fastest way to die.", True, (200, 200, 200))
        d2 = font.render("Your player dies at 100 points.", True, (200, 200, 200))
        begin = font.render("Press SPACE to begin!", True, (255, 255, 255))

        screen.blit(title, title.get_rect(center = (WINDOW_WIDTH // 2, 150)))
        screen.blit(d1, d1.get_rect(center = (WINDOW_WIDTH // 2, 200)))
        screen.blit(d2, d2.get_rect(center = (WINDOW_WIDTH // 2, 230)))
        screen.blit(begin, begin.get_rect(center = (WINDOW_WIDTH // 2, 320)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        pygame.display.flip()
        clock.tick(60)

#game over screen; seconds is from timer
def gameOverScreen(seconds):
    while True:
        screen.fill((20, 20, 20))

        over = bigfont.render("YOU DIED! CONGRATS!", True, (255, 255, 255))
        msg = font.render(f"You took {seconds} seconds to die!", True, (200, 200, 200))

        screen.blit(over, over.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))
        screen.blit(msg, msg.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)

def add_points(amount):
    """Increase the score."""
    global score
    score += amount

def setRoom():
    # Load & scale images
    floor = pygame.transform.scale(
        pygame.image.load("images/floor.jpg"),
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )


    coffee_table_img = pygame.transform.scale(
        pygame.image.load("images/coffee-table.png"),
        (assetWidth, assetHeight)
    )

    desk_img = pygame.transform.scale(
        pygame.image.load("images/desk.png"),
        (assetWidth, assetHeight)
    )

    bonfire_img = pygame.transform.scale(
        pygame.image.load("images/bonfire.png"),
        (50, 50)
    )

    kitchen_img = pygame.image.load("images/kitchen.png")
    kitchen_img = pygame.transform.scale(kitchen_img, (assetWidth + 50, assetHeight + 50))
    kitchen_img = pygame.transform.rotate(kitchen_img, 90)


    # walls x-cordinate, y-cordinate, width, height
    wall_data = [
        #outer walls
        [0,0,wallWidth,WINDOW_HEIGHT],
        [0,0,WINDOW_WIDTH,wallWidth],
        [0,WINDOW_HEIGHT - wallWidth,WINDOW_WIDTH+wallWidth,wallWidth],
        [WINDOW_WIDTH - wallWidth,0,wallWidth,WINDOW_HEIGHT+wallWidth],

        #bedroom walls
        [roomWidth, 0, wallWidth, roomHeight - doorSize],
        [0, roomHeight, roomWidth//2, wallWidth],
        [roomWidth//2 + doorSize, roomHeight, 3*roomWidth//4, wallWidth],
        #garden
        [2*roomWidth,0,wallWidth,roomHeight],
        [5*roomWidth//4+2*doorSize, roomHeight, roomWidth//2, wallWidth],
        #washroom
        [5*roomWidth//4+3*doorSize,roomHeight, roomWidth//2, wallWidth],
        [WINDOW_WIDTH-roomWidth//4,roomHeight, roomWidth//4, wallWidth],
        #kitchen
        [WINDOW_WIDTH - roomWidth, 2*roomHeight, roomWidth, wallWidth],
        [WINDOW_WIDTH - roomWidth, 2*roomHeight+doorSize+15, wallWidth, roomHeight],
    ]

    walls = []
    for x, y, w, h in wall_data:
        walls.append(pygame.Rect(x, y, w, h))


    wall_color = (120, 120, 120)

    return (floor, desk_img, coffee_table_img,kitchen_img,bonfire_img,
            walls, wall_color)

# Load room setup
(floor, desk_img, coffee_table_img,kitchen_img,bonfire_img,
 walls, wall_color) = setRoom()


def can_move(player_rect, dx, dy, walls):
    new_rect = player_rect.move(dx, dy)

    for wall in walls:
        if new_rect.colliderect(wall):
            return False  # Movement blocked

    return True  # Safe to move



# Simple player rectangle
player = pygame.Rect(100, 100, 40, 40)
player_speed = 2

#we need this to make sure we know the positions of the assets to check collisions or mouse clicks
coffee_table_rect = coffee_table_img.get_rect(topleft=(WINDOW_WIDTH//4, WINDOW_HEIGHT//2))
desk_rect = desk_img.get_rect(topleft=(roomWidth - assetWidth, 0))
kitchen_rect = kitchen_img.get_rect(topleft=(WINDOW_WIDTH - assetHeight - 50, WINDOW_HEIGHT - assetWidth - 50 - wallWidth))
bonfire_rect = bonfire_img.get_rect(topleft=(WINDOW_WIDTH//2, wallWidth))

collidables = walls
interactive_objects = [(coffee_table_rect, "Coffee intoxication?"),
                       (desk_rect, "Midterm prep?"),
                       (kitchen_rect, "Freeze to death?"),
                       (bonfire_rect, "Burn yourself?")]


clock = pygame.time.Clock()

#pop up loop
def popup(message, option1="Yes", option2="No"):
    popWidth, popHeight = 400, 200
    popup_rect = pygame.Rect(
        (WINDOW_WIDTH - popWidth) // 2,
        (WINDOW_HEIGHT - popHeight) // 2,
        popWidth,
        popHeight
    )

    #button rects
    btnWidth, btnHeight = 100, 50
    btn1_rect = pygame.Rect(
        popup_rect.x + 50,
        popup_rect.y + popHeight - btnHeight - 20,
        btnWidth,
        btnHeight
    )
    btn2_rect = pygame.Rect(
        popup_rect.x + popWidth - btnWidth - 50,
        popup_rect.y + popHeight - btnHeight - 20,
        btnWidth,
        btnHeight
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn1_rect.collidepoint(event.pos):
                    return True
                elif btn2_rect.collidepoint(event.pos):
                    return False



        # Draw popup
        pygame.draw.rect(screen, (200, 200, 200), popup_rect)
        pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)

        # Draw buttons
        pygame.draw.rect(screen, (100, 200, 100), btn1_rect)
        pygame.draw.rect(screen, (200, 100, 100), btn2_rect)

        # Button text
        btn_font = pygame.font.Font("pixelfont.ttf", 32)
        btn1_text = btn_font.render(option1, True, (0, 0, 0))
        btn2_text = btn_font.render(option2, True, (0, 0, 0))
        screen.blit(btn1_text, btn1_text.get_rect(center=btn1_rect.center))
        screen.blit(btn2_text, btn2_text.get_rect(center=btn2_rect.center))

        # Message text
        msg_font = pygame.font.Font("pixelfont.ttf", 34)
        msg_text = msg_font.render(message, True, (0, 0, 0))
        screen.blit(msg_text, msg_text.get_rect(center=(popup_rect.centerx, popup_rect.y + 60)))

        pygame.display.flip()
        clock.tick(30)



# Main loop
running = True
popup_active = False #to check for first collision
#game loop
startScreen()
startTime = pygame.time.get_ticks() #to start timer after player presses space bar
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()

    old_x, old_y = player.x, player.y

    # Player movement
    if keys[pygame.K_LEFT]:
        if can_move(player, -player_speed, 0, collidables):
            player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        if can_move(player, player_speed, 0, collidables):
            player.x += player_speed

    if keys[pygame.K_UP]:
        if can_move(player, 0, -player_speed, collidables):
            player.y -= player_speed

    if keys[pygame.K_DOWN]:
        if can_move(player, 0, player_speed, collidables):
            player.y += player_speed


    if keys[pygame.K_r]:
        reset_game()

    for int_obj, msg in interactive_objects:
        if player.colliderect(int_obj) and not popup_active:
            popup_active = True
            choice = popup(msg, "Yes", "No")
            if choice:
                add_points(5)
            player.x, player.y = old_x, old_y
            popup_active = False

    # Draw floor
    screen.blit(floor, (0, 0))

    # screen.blit(grass_area, (rect_x, rect_y))

    # Draw objects
    screen.blit(coffee_table_img, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2 ))
    screen.blit(desk_img, (roomWidth-assetWidth, 0))
    screen.blit(kitchen_img, (WINDOW_WIDTH - assetHeight-50, WINDOW_HEIGHT-assetWidth-50-wallWidth))
    screen.blit(bonfire_img, (WINDOW_WIDTH//2, wallWidth))

    # Draw player
    screen.blit(player_img, player.topleft)

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, wall_color, wall)


    # Draw score (top right)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 20, 20))
    screen.blit(score_text, score_rect)

    # Draw timer under the score
    elapsedTime = (pygame.time.get_ticks() - startTime) // 1000
    timerText = font.render(f"Time: {elapsedTime}", True, (255, 255, 255))
    timerRect = timerText.get_rect(topright = (WINDOW_WIDTH - 20, 40))
    screen.blit(timerText, timerRect)

    if score >= 100:
        gameOverScreen(elapsedTime)

    pygame.display.flip()
    clock.tick(60)   # limits to 60 FPS. This is to make sure it runs in same speed in all computers.

pygame.quit()
sys.exit()
