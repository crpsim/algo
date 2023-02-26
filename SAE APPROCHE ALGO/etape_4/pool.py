from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import random

import constants
import engine
import math

def draw(scene: pygame.Surface, geometry, balls):
    scene.fill(constants.BACKGROUND_COLOR)
    
    pygame.draw.rect(
        scene,
        constants.COLOR_SNOOKER_BACKGROUND,
        (0, 0, constants.LAYOUT_PLAY_AREA_WIDTH * constants.SCALE, constants.LAYOUT_PLAY_AREA_HEIGHT * constants.SCALE),
        0
    )

    pygame.draw.line(
        scene,
        (0, 0, 0),
        (constants.LAYOUT_BAULK_LINE * constants.SCALE, 0),
        (constants.LAYOUT_BAULK_LINE * constants.SCALE, constants.LAYOUT_PLAY_AREA_HEIGHT * constants.SCALE),
        1
    )

    pygame.draw.arc(
        scene,
        (0, 0, 0),
        (
            constants.LAYOUT_BAULK_LINE * constants.SCALE - constants.LAYOUT_SEMI_CIRCLE_RADIUS * constants.SCALE,
            (geometry["center_y"] - constants.LAYOUT_SEMI_CIRCLE_RADIUS) * constants.SCALE,
            2 * constants.LAYOUT_SEMI_CIRCLE_RADIUS * constants.SCALE,
            2 * constants.LAYOUT_SEMI_CIRCLE_RADIUS * constants.SCALE
        ),
        .5 * math.pi,
        1.5 * math.pi,
        1
    )

    for ball in balls:
        pygame.draw.circle(
            scene,
            ball["color"],
            (ball["x"] * constants.SCALE, ball["y"] * constants.SCALE),
            geometry["ball_radius"] * constants.SCALE
        )
   

if __name__ == '__main__':
    random.seed(None)
    geometry = engine.compute_geometry()
    balls = engine.create_balls(geometry)
    cue_ball = balls[6]
    current_state = constants.STATE_BALLS_MOVING

    pygame.init()
    clock = pygame.time.Clock()
    running = True
    scene = pygame.display.set_mode((constants.SCENE_WIDTH, constants.SCENE_HEIGHT), pygame.GL_DOUBLEBUFFER)

    previous_collisions = []

    small_font = pygame.font.Font(None, 24)
    big_font = pygame.font.Font(None, 48)

    paused = False    
    pause_text = big_font.render('PAUSED (press SPACE to continue)', True, (255, 255, 255), (100, 50, 50))
    pause_rect = pause_text.get_rect()
    pause_rect.center = (constants.SCENE_WIDTH // 2, constants.SCENE_HEIGHT // 3)

    mouse_x = 0
    mouse_y = 0

    while running:
                
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                paused = not paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                aiming_x = mouse_x / constants.SCALE
                aiming_y = mouse_y / constants.SCALE
                dx = aiming_x - cue_ball["x"]
                dy = aiming_y - cue_ball["y"]
                cue_ball["dx"] = dx / 500.
                cue_ball["dy"] = dy / 500.

        if paused:
            draw(scene, geometry, balls)
            scene.blit(pause_text, pause_rect)
             
        else :
            moving_balls = engine.how_many_moving_balls(balls) # We initalize the list here
            
            if current_state == constants.STATE_BALLS_MOVING:

                # collision detection
                colls = engine.computeCollisions(balls)

                # collision resolution
                engine.processCollisions(balls, previous_collisions, colls)
                previous_collisions = colls
                
                for ball in moving_balls:
                    for i in range(16):
                        engine.update(ball, 1)

            # draw
            draw(scene, geometry, balls)

            #

            if moving_balls == []: #We have changed the condition here to check the list instead of an integer
                current_state = constants.STATE_PAUSE
            else:
                current_state = constants.STATE_BALLS_MOVING

            if current_state == constants.STATE_PAUSE:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                aiming_x = mouse_x / constants.SCALE
                aiming_y = mouse_y / constants.SCALE

                pygame.draw.aaline(
                    scene,
                    (0, 0, 0),
                    (constants.SCALE * cue_ball["x"] , constants.SCALE * cue_ball["y"]),
                    (constants.SCALE * aiming_x, constants.SCALE * aiming_y),
                    1
                )

        clock.tick(constants.FPS)
        pygame.display.update()

    pygame.quit() 
