import sys
import pygame
import random
import math
import numpy

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("BOUNCING BALLS")
FPS = 60
fpsClock = pygame.time.Clock()
BLACK = (0, 0, 0)
ORANGE = (255, 110, 0)
RED = (255, 0, 0)
CIRCLE_CENTER = numpy.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2], dtype=numpy.float64)  # List
CIRCLE_RADIUS = 150
BALL_RADIUS = 5
ball_pos = numpy.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 120], dtype=numpy.float64)
GRAVITY = 0.2
ball_velocity = numpy.array([0, 0], dtype=numpy.float64)  # vận tốc theo Ox và Oy
arc_degrees = 60
start_angle = math.radians(-arc_degrees / 2)
end_angle = math.radians(arc_degrees / 2)
spinning_speed = 0.01


class Ball:
    def __init__(self, position, velocity):
        self.p = numpy.array(position, dtype=numpy.float64)
        self.v = numpy.array(velocity, dtype=numpy.float64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.is_in = True


def draw_arc(window, center, radius, start_angle, end_angle):
    p1 = center + (radius + 1000) * numpy.array([math.cos(start_angle), math.sin(start_angle)])
    p2 = center + (radius + 1000) * numpy.array([math.cos(end_angle), math.sin(end_angle)])
    pygame.draw.polygon(window, BLACK, [center, p1, p2], 0)


def is_ball_in_arc(ball_pos, CIRCLE_CENTER, start_angle, end_angle):
    dx = ball_pos[0] - CIRCLE_CENTER[0]
    dy = ball_pos[1] - CIRCLE_CENTER[1]
    ball_angle = math.atan2(dy, dx)
    start_angle = start_angle % (2 * math.pi)
    end_angle = end_angle % (2 * math.pi)
    if start_angle > end_angle:
        end_angle += 2 * math.pi
    if start_angle <= ball_angle <= end_angle or start_angle <= ball_angle + 2 * math.pi <= end_angle:
        return True
    return False


ball = Ball(ball_pos, ball_velocity)
balls = [Ball(ball_pos, ball_velocity)]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    start_angle += spinning_speed
    end_angle += spinning_speed
    for ball in balls:
        if ball.p[0] < 0 or ball.p[0] > WINDOW_WIDTH or ball.p[1] < 0 or ball.p[1] > WINDOW_HEIGHT:
            balls.remove(ball)
            balls.append(Ball(position=ball_pos, velocity=[random.uniform(-4, 4), random.uniform(-1, 1)]))
            balls.append(Ball(position=ball_pos, velocity=[random.uniform(-4, 4), random.uniform(-1, 1)]))

        ball.v[1] += GRAVITY
        ball.p += ball.v
        dist = numpy.linalg.norm(ball.p - CIRCLE_CENTER)
        if dist + BALL_RADIUS > CIRCLE_RADIUS:
            if is_ball_in_arc(ball.p, CIRCLE_CENTER, start_angle, end_angle):
                ball.is_in = False
            if ball.is_in:
                d = ball.p - CIRCLE_CENTER
                d_unit = d / numpy.linalg.norm(d)
                ball.p = CIRCLE_CENTER + (CIRCLE_RADIUS - BALL_RADIUS) * d_unit
                t = numpy.array([-d[1], d[0]], dtype=numpy.float64)
                proj_v_t = (numpy.dot(ball.v, t) / numpy.dot(t, t)) * t  # projection: hình chiếu
                ball.v = 2 * proj_v_t - ball.v
                ball.v += t * spinning_speed  # v=rw

    window.fill(BLACK)
    pygame.draw.circle(window, ORANGE, CIRCLE_CENTER, CIRCLE_RADIUS, 3)
    draw_arc(window, CIRCLE_CENTER, CIRCLE_RADIUS, start_angle, end_angle)
    for ball in balls:
        pygame.draw.circle(window, ball.color, ball.p, BALL_RADIUS)

    pygame.display.flip()
    fpsClock.tick(FPS)
