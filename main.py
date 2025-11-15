import pygame, sys, random, time

#ball movement and collisions
def ball_animation():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # ball collision
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    #resseting startup timer
    global startup_frames, startup_timer, frames_elapsed, game_started
    startup_frames = 3 * FPS  # 3 second delay (assuming FPS = 60)
    startup_timer = 3 * FPS  # 3 seconds (adjust FPS as needed)
    frames_elapsed = 0
    game_started = False

    #resetting ball and opponent
    global ball_speed_x, ball_speed_y, opponent
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))
    opponent.x, opponent.y = screen_width - 20, screen_height / 2 - 70
    


#init
pygame.init()
clock = pygame.time.Clock()

#init screen
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

#init shapes
#menu
title_text = pygame.font.Font(None, 100).render("PONG", True, (255, 255, 255))
play_text = pygame.font.Font(None, 50).render("Press 'enter' to Play", True, (100, 100, 100))

#game
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)

#colors
bg_color = (24, 24, 24)
light_grey = (200, 200, 200)
WHITE = (255, 255, 255)

#font
font = pygame.font.Font(None, 90)

#game data
FPS = 60
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7

#menu data
game = 0

ball_restart()
#game loop
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game == 0:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game = 1
                    startup_timer = 3 * FPS
        screen.fill(bg_color)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4 - title_text.get_height() // 2))
        screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, screen_height // 1.25 - play_text.get_height() // 2))

    elif game == 1:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player_speed += 7
                if event.key == pygame.K_w:
                    player_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player_speed -= 7
                if event.key == pygame.K_w:
                    player_speed += 7
        player_animation()
        if frames_elapsed < startup_frames:
            frames_elapsed += 1
        else:
            ball_animation()
            opponent_animation()


        #visuals
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

        # Countdown display
        if startup_timer > 0:
            startup_timer -= 1
            countdown_number = (startup_timer // FPS) + 1
            countdown_text = font.render(str(countdown_number), True, WHITE)
            screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height / 2.5))
        else:
            game_started = True

    #update window
    pygame.display.flip()
    clock.tick(FPS)