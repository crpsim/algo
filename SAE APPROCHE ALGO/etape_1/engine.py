import constants
import math

def compute_geometry():
    geometry = dict()

    geometry["ball_radius"] = constants.BALL_RADIUS
    geometry["width"] = constants.LAYOUT_PLAY_AREA_WIDTH
    geometry["height"] = constants.LAYOUT_PLAY_AREA_HEIGHT
    geometry["bottom_right_x"] = constants.LAYOUT_PLAY_AREA_WIDTH
    geometry["bottom_right_y"] = constants.LAYOUT_PLAY_AREA_HEIGHT
    geometry["center_x"] = constants.LAYOUT_PLAY_AREA_WIDTH / 2
    geometry["center_y"] = constants.LAYOUT_PLAY_AREA_HEIGHT / 2
    geometry["d_zone_top_y"] = geometry["center_y"] - constants.LAYOUT_SEMI_CIRCLE_RADIUS
    geometry["d_zone_bottom_y"] = geometry["center_y"] + constants.LAYOUT_SEMI_CIRCLE_RADIUS
    geometry["d_zone_max_x"] = constants.LAYOUT_BAULK_LINE - constants.LAYOUT_SEMI_CIRCLE_RADIUS
    geometry["pink_spot_x"] =  constants.LAYOUT_PLAY_AREA_WIDTH - constants.LAYOUT_PINK_SPOT
    geometry["black_spot_x"] = constants.LAYOUT_PLAY_AREA_WIDTH - constants.LAYOUT_BLACK_SPOT

    return geometry

def update(ball, deltaTime):        
    ball["x"] += deltaTime * ball["dx"]
    ball["y"] += deltaTime * ball["dy"]

    dx = ball["dx"]
    dy = ball["dy"]
    l = math.sqrt(dx ** 2 + dy ** 2)
    if l > constants.EPSILON_SPEED:
        dx = dx / l * constants.FRICTION
        dy = dy / l * constants.FRICTION
    
        ball["dx"] -= dx * deltaTime
        ball["dy"] -= dy * deltaTime
    else:
        ball["dx"] = 0
        ball["dy"] = 0
    

    # bouncing
    if ball["x"] < constants.BALL_RADIUS:
        ball["x"] =  constants.BALL_RADIUS
        ball["dx"] = -ball["dx"] * constants.DAMP_COEF
        ball["dy"] *= constants.DAMP_COEF
    elif ball["x"] > constants.LAYOUT_PLAY_AREA_WIDTH - constants.BALL_RADIUS:
        ball["x"] = constants.LAYOUT_PLAY_AREA_WIDTH - constants.BALL_RADIUS
        ball["dx"] = -ball["dx"] * constants.DAMP_COEF
        ball["dy"] *= constants.DAMP_COEF

    if ball["y"] < constants.BALL_RADIUS:
        ball["y"] = constants.BALL_RADIUS
        ball["dy"] = -ball["dy"] * constants.DAMP_COEF
        ball["dx"] *= constants.DAMP_COEF
    elif ball["y"] > constants.LAYOUT_PLAY_AREA_HEIGHT - constants.BALL_RADIUS:
        ball["y"] = constants.LAYOUT_PLAY_AREA_HEIGHT - constants.BALL_RADIUS
        ball["dy"] = -ball["dy"] * constants.DAMP_COEF
        ball["dx"] *= constants.DAMP_COEF

def bounce(a, b):
    tangent = (b["y"] - a["y"], -(b["x"] - a["x"]))

    norm = math.sqrt(tangent[0] ** 2 + tangent[1] ** 2)
    if norm == 0:
        return
    tangent = (tangent[0] / norm, tangent[1] / norm)

    relative_velocity = (a["dx"] - b["dx"], a["dy"] - b["dy"])

    length = relative_velocity[0] * tangent[0] + relative_velocity[1] * tangent[1]
    
    velocity_component_on_tangent = (length * tangent[0], length * tangent[1])
    velocity_component_perpendicular_to_tangent = (relative_velocity[0] - velocity_component_on_tangent[0], relative_velocity[1] - velocity_component_on_tangent[1])
    a["dx"] -= velocity_component_perpendicular_to_tangent[0]
    a["dy"] -= velocity_component_perpendicular_to_tangent[1]
    b["dx"] += velocity_component_perpendicular_to_tangent[0]
    b["dy"] += velocity_component_perpendicular_to_tangent[1]

    return

def processCollisions(balls, previous_collisions, colls):
    for collision in colls:
        # ignore collisions that were already occuring in the previous frame
        if collision in previous_collisions:
            continue
        
        a, b = collision
        p = balls[a]
        q = balls[b]

        bounce(p, q)

def create_balls(geometry):

    balls = []
    balls.append({
        "x": geometry["center_x"],
        "y": geometry["center_y"],
        "dx": 0,
        "dy": 0,
        "color": constants.COLOR_SNOOKER_BLUE
    })

    balls.append({
        "x": constants.LAYOUT_BAULK_LINE,
        "y": geometry["d_zone_top_y"],
        "dx": 0,
        "dy": 0,
        "color": constants.COLOR_SNOOKER_YELLOW
    })

    balls.append({
        "x": constants.LAYOUT_BAULK_LINE,
        "y": geometry["d_zone_bottom_y"],
        "dx": 0,
        "dy": 0,
        "color": constants.COLOR_SNOOKER_GREEN
    })

    balls.append({
        "x": constants.LAYOUT_BAULK_LINE,
        "y": geometry["center_y"],
        "dx": 0,
        "dy": 0,
        "color": constants.COLOR_SNOOKER_BROWN
    })

    balls.append({
        "x": geometry["pink_spot_x"],
        "y": geometry["center_y"],
        "dx": 0,
        "dy": 0,
        "color": constants.COLOR_SNOOKER_PINK
    })

    balls.append({
        "x": geometry["black_spot_x"],
        "y": geometry["center_y"],
        "dx": 0,
        "dy": 0,
        "color": constants.COLOR_SNOOKER_BLACK
    })

    balls.append({
        "x": geometry["d_zone_max_x"] + 3,
        "y": geometry["center_y"] + 3,
        "dx": 0,
        "dy": 0,
        "color": constants.COLOR_SNOOKER_CUE
    })

    first_red_ball_x = geometry["pink_spot_x"] + 2 * constants.BALL_RADIUS
    first_red_ball_y = geometry["center_y"]
    radius = constants.BALL_RADIUS
    sqrt32 = math.sqrt(3) * radius + constants.LAYOUT_GAP_BETWEEN_ADJACENT_BALLS
    radius += .5

    balls.append({
        "x": first_red_ball_x,
        "y": first_red_ball_y,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + sqrt32,
        "y": first_red_ball_y - radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + sqrt32,
        "y": first_red_ball_y + radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 2 * sqrt32,
        "y": first_red_ball_y - 2* radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 2 * sqrt32,
        "y": first_red_ball_y,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 2 * sqrt32,
        "y": first_red_ball_y + 2* radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 3 * sqrt32,
        "y": first_red_ball_y - 3 * radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 3 * sqrt32,
        "y": first_red_ball_y - radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 3 * sqrt32,
        "y": first_red_ball_y + radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 3 * sqrt32,
        "y": first_red_ball_y + 3 * radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 4 * sqrt32,
        "y": first_red_ball_y + 4 * radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 4 * sqrt32,
        "y": first_red_ball_y + 2 * radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 4 * sqrt32,
        "y": first_red_ball_y,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 4 * sqrt32,
        "y": first_red_ball_y - 2 * radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

    balls.append({
        "x": first_red_ball_x + 4 * sqrt32,
        "y": first_red_ball_y - 4 * radius,
        "dx": 0,
        "dy": .0,
        "color": constants.COLOR_SNOOKER_RED
    })

        
    return balls

def circleCollision(c1, c2):
    '''
    Determines if two circles intersect or not
    '''
    angle = 0
    while(angle<3.1415926*2):
        # we pick a point on the first circle
        ptx = c1[0]+(math.cos(angle)*constants.BALL_RADIUS)
        pty = c1[1]+(math.sin(angle)*constants.BALL_RADIUS)
        # we compute the length between this point and the center of c2
        dx = ptx - c2[0]
        dy = pty - c2[1]
        d = math.sqrt(dx ** 2 + dy ** 2)
        # if this length is less than the radius of c2, then this point is inside the circle
        if d < constants.BALL_RADIUS:
            return True
        # we then move to another point close to the previous one, until we loop around c1
        angle = angle + 0.01

    # no collision detected: c1 and c2 do not intersect
    return False


def computeCollisions(balls):
    '''
    Computes the collisions between a collection of balls and a single ball
    among them, identified by their list index
    '''

    collisions = []
    for i in range(len(balls)):
        p = balls[i]
        for j in range (i+1, len(balls)):
            if i!=j :
                # To avoid considering collisions with themselves
                q = balls[j]
                # To test mooving balls only 
                if ((p["dx"] != 0) or (p["dy"] != 0) or (q["dx"] != 0) or (q["dy"] != 0)):
                    # Test collision between the balls p and q
                    if circleCollision((p["x"],p["y"]),(q["x"],q["y"])):
                        collisions.append((i, j))
                    
    return collisions

def how_many_moving_balls(balls):
    moving_balls = 0
    for ball in balls:
        if ball["dx"] != 0 or ball["dy"] != 0:
            moving_balls += 1
    
    return moving_balls
