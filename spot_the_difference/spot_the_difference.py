#Spot the difference

import pygame #pip install pygame

#initialize the pygame framework
pygame.init()

#Constants
GAME_FOLDER  = 'D:/Python/project/spot_the_difference/'
BLUE = pygame.Color(0,0, 255)
RED = pygame.Color(255,0,0)
ORANGE = pygame.Color(255, 127, 0)
WHITE = pygame.Color(255,255, 255)
BLACK = pygame.Color(0,0,0)

HUD_HEIGHT = 50
RADIUS = 50

#Game window, caption
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800 + HUD_HEIGHT
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('SPOT THE DIFFERENCE')

#sounds
pygame.mixer.music.load(GAME_FOLDER+ 'instrumental.mp3')
pygame.mixer.music.set_volume(0.3)


beep = pygame.mixer.Sound(GAME_FOLDER + 'beep.wav')
beep.set_volume(0.2)

loss = pygame.mixer.Sound(GAME_FOLDER + 'loss.wav')
loss.set_volume(0.1)

#game data structures, values
#dict : {key, (image_path_string, play_area_tuple, differences_list) }

game_levels = {
1: ('spot_the_difference_1.jpg', (600,0,1200,800), [(860,280),(1030,430),(915,705),(660,765),(1060,265), (1050,760), (1020,615), ((1070,440),(1130,450)), ((690,470),(730,480),(695,505)), ((930,105),(990,130),(1025,165),(990,205)) ] , 'Jungle'),
2: ('spot_the_difference_2.png', (0,400,1200,800), [(1090,710), (1150,610), (500,760), ((880,580),(920,570)), (265,480), (200,480)] , 'Roller Skates'),
3: ('spot_the_difference_3.jpg', (0,400,1200,800), [(100,700), (900,630), (1140,690), (570, 690), (890,500), (275,570), ((365,450), (365,490), (480,480), (580,490))], 'Pool')

}

#game values
number_of_levels = len(game_levels)
current_level = 0
assets_loaded = False
game_over = False
game_status = 2


#game font and text
big_font = pygame.font.Font(GAME_FOLDER + 'SunnyspellsRegular.otf', 40)
small_font = pygame.font.Font(GAME_FOLDER + 'SunnyspellsRegular.otf', 30)

title = big_font.render('Spot The Difference', True, ORANGE)
title_rect = title.get_rect()
title_rect.center = (WINDOW_WIDTH//2, HUD_HEIGHT//2)

level = small_font.render('Level', True, WHITE)
level_rect = level.get_rect()
level_rect.centery = HUD_HEIGHT//2
level_rect.left = 50

time = small_font.render('Time', True, WHITE)
time_rect = time.get_rect()
time_rect.centery = HUD_HEIGHT//2
time_rect.right = WINDOW_WIDTH - 50

theme_title = big_font.render(game_levels[current_level+1][-1], True, WHITE)
theme_title_rect = theme_title.get_rect()
theme_title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

game_ends = big_font.render('GAME ENDS!!!', True, WHITE)
game_ends_rect = game_ends.get_rect()
game_ends_rect.center = (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 - 50)

game_won = small_font.render('You WIN!!!', True, RED)
game_lost = small_font.render('You LOSE!!!', True, RED)
game_won_lost = game_won
game_won_lost_rect = game_won.get_rect()
game_won_lost_rect.center = (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2)

game_restart = small_font.render('Press r to restart, q to quit', True, WHITE)
game_restart_rect = game_restart.get_rect()
game_restart_rect.center = (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 + 50)

#main game loop (defines the life of the game)
running = True
FPS = 30
clock = pygame.time.Clock()
timer = 0
slide_timer = FPS *2

while running:
    if game_status == 1:
        if not assets_loaded:
            level = small_font.render('Level: ' + str(current_level), True, WHITE)
            background_image = pygame.image.load( GAME_FOLDER + game_levels[current_level][0])
            playable_area = game_levels[current_level][1]
            actual_differences = game_levels[current_level][2].copy()

            chances = len(actual_differences)
            play_time = chances * 6
            time = small_font.render('Time: ' + str(play_time), True, WHITE)

            pygame.mixer.music.play(-1)

            discovered_differences = []

            timer = 0

            assets_loaded = True

        timer+=1
        if timer == FPS:
            timer = 0
            play_time-=1
            if play_time > 10:
                time = small_font.render('Time: ' + str(play_time), True, WHITE)
            elif play_time > 0:
                time = small_font.render('Time: ' + str(play_time), True, RED)
                beep.play()
            elif play_time <= 0:
                game_won_lost = game_lost
                game_status = 3

    #read the events
    for ev in  pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_q:
                running = False
            elif ev.key == pygame.K_r and game_status == 3:
                current_level = 0
                game_status = 2
                slide_timer = FPS *2
                assets_loaded = False
                theme_title = big_font.render(game_levels[current_level + 1][-1], True, WHITE)


        elif ev.type == pygame.MOUSEBUTTONDOWN and game_status == 1:
            if ev.button == 1: #LEFT mouse button
                click_x = ev.pos[0]
                click_y = ev.pos[1]- HUD_HEIGHT
                if click_x >= playable_area[0] and click_x <= playable_area[2] and click_y >= playable_area[1] and click_y <= playable_area[3]:#inside the playable area

                    if chances: #game on
                        #check right or wrong (sequential search)
                        check = False

                        for i, point in enumerate(actual_differences): # (0,first_point); (1,second_point); ...; (n-1,last_point)
                            if isinstance(point[0], int): #single point
                                if abs( point[0] - click_x) < RADIUS and abs(point[1] - click_y) < RADIUS:
                                    check = True
                                    #remove that point
                                    temp = actual_differences.pop(i)
                                    discovered_differences.append((temp, check))

                                    break
                            elif isinstance(point[0], tuple):#cluster of points
                                for subpoint in point:
                                    if abs(subpoint[0] - click_x) < RADIUS and abs(subpoint[1] - click_y) < RADIUS:
                                        check = True
                                        # remove that point
                                        temp = actual_differences.pop(i)
                                        discovered_differences.append((temp, check))
                                        break

                        if check == False:
                            discovered_differences.append(((click_x, click_y), False))
                            loss.play()

                        chances-=1

    #fill black in the window to refresh the hud area
    display_surface.fill(BLACK)

    if game_status == 1:
        # apply thee background image to the display surface (window)
        display_surface.blit(background_image, (0, HUD_HEIGHT))

        for point in discovered_differences:
            color = BLUE if point[1] else RED
            if isinstance(point[0][0], int):
                #single point
                pygame.draw.circle(surface=display_surface, color=color, center=(point[0][0], point[0][1]+HUD_HEIGHT), radius=RADIUS, width=2)
            elif isinstance(point[0][0], tuple):
                for subpoint in point[0]:
                    pygame.draw.circle(surface=display_surface, color=color, center=(subpoint[0], subpoint[1]+ HUD_HEIGHT) , radius=RADIUS, width=2)


        #check for chances reduced to 0
        if chances == 0:
            # check for level change:
            if len(actual_differences) == 0:
                pygame.mixer.music.stop()
                game_status = 2
                slide_timer = FPS * 2
                assets_loaded = False
                if current_level < 3:
                    theme_title = big_font.render(game_levels[current_level + 1][-1], True, WHITE)

            else:
                #lost
                game_won_lost = game_lost
                game_status = 3

        #blit the HUD
        display_surface.blit(title, title_rect)
        display_surface.blit(level, level_rect)
        display_surface.blit(time, time_rect)

    if game_status == 2:
        display_surface.blit(title, title_rect)
        if current_level < 3:
            display_surface.blit(theme_title, theme_title_rect)
        else:
            slide_timer = 1

        slide_timer -=1
        if slide_timer== 0:
            current_level+=1
            if current_level > number_of_levels:
                game_won_lost = game_won
                game_status = 3
            else:
                game_status = 1
    if game_status == 3:
        pygame.mixer.music.stop()
        display_surface.blit(title, title_rect)
        display_surface.blit(game_ends, game_ends_rect)
        display_surface.blit(game_won_lost, game_won_lost_rect)
        display_surface.blit(game_restart, game_restart_rect)


    #update the display
    pygame.display.update()
    #moderate the rate of iteration
    #cooperative multitasking is achieved
    #game players get the same gaming experience across different CPU's
    clock.tick(FPS)

#quit (dispose the resources)
pygame.quit()