import constants
import engine
import math
import time

if __name__ == '__main__':
    geometry = engine.compute_geometry()
    balls = engine.create_balls(geometry)
    cue_ball = balls[6]
 
    previous_collisions = []

    running = True

    mouse_x = 1283
    mouse_y = 351
    
    aiming_x = mouse_x / constants.SCALE
    aiming_y = mouse_y / constants.SCALE
    dx = aiming_x - cue_ball["x"]
    dy = aiming_y - cue_ball["y"]
    cue_ball["dx"] = dx / 500.
    cue_ball["dy"] = dy / 500.

    start_time = time.time()

    while running:
        moving_balls = engine.how_many_moving_balls(balls)  #####

        colls = engine.computeCollisions(balls)

        # collision resolution
        engine.processCollisions(balls, previous_collisions, colls)
        previous_collisions = colls
        
        for ball in moving_balls :
            for i in range(16):
                engine.update(ball, 1)

        
        
        running = (moving_balls != [])

    end_time = time.time()
    
    print((int)((end_time-start_time)*1000), "ms")
