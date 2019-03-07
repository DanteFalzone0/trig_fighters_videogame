"""
Copyright (C) 2019 Dante Falzone

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import pygame
import os
import sys
import random
import re
import math
from pygame.locals import *

fpsClock = pygame.time.Clock()

SURF = pygame.display.set_mode((1000, 600))  # Set the surface


def shift(x, y, angle, var):
    rotated_x = (x * math.cos(angle)) - (y * math.sin(angle))  # Perform the necessary transformations
    rotated_y = (y * math.cos(angle)) + (x * math.sin(angle))  # within the coordinate plane.
    if var == "x":
        return rotated_x
    else:
        return rotated_y
    """
    A note of explanation (part 0)

    Here I have used trigonometry to determine how to rotate the points. To rotate a point on a
    2d coordinate plane about the origin with a given initial location of (x, y), the transformed
    coordinates (x', y') for an angle theta can be found using these equations (as expressed in
    normal notation):

    x' = x(cos(theta)) - y(sin(theta))
    y' = y(cos(theta)) + x(sin(theta))

    This can be understood in terms of the transformed point's coordinates as the opposite
    and adjacent sides of a right triangle whose hypotenuse remains constant while its side
    lengths vary proportionally.
    """



def draw_ship(x, y, angle):
    """
    A note of explanation (part 1) (see above for part 0):

    The functions for finding the coordinates of rotated points are described above. However,
    those equations are only for rotating about the origin. Rotating about another arbitrary
    point is slightly more complicated.

    The general equations to find the transformed point (x', y') resulting from rotating the
    point (x, y) about (a, b) by theta degrees are as follows:

    x' = a + (((x - a)cos(theta)) - ((y - b)sin(theta)))
    y' = b + (((y - b)cos(theta)) + ((x - a)sin(theta)))

    What this is doing is essentially replacing the point (a, b) with the origin, doing the
    rotations as described above, and then translating the resultant points back to the
    appropriate location. If you are trying to rotate a shape about an arbitrary point, you
    do this by first calculating exactly what coordinates all the points would have if the shape
    were moved so that the point of rotation becomes the origin. That's what this function does.
    """
    apex_x = (shift(0, -10, angle, "x")) + x
    apex_y = (shift(0, -10, angle, "y")) + y

    middle_x = (shift(0, 5, angle, "x")) + x
    middle_y = (shift(0, 5, angle, "y")) + y

    bottom_left_x = (shift(-10, 10, angle, "x")) + x
    bottom_left_y = (shift(-10, 10, angle, "y")) + y

    bottom_right_x = (shift(10, 10, angle, "x")) + x
    bottom_right_y = (shift(10, 10, angle, "y")) + y

    pygame.draw.line(SURF, (0, 255, 80), (bottom_left_x, bottom_left_y), (apex_x, apex_y),  1)
    pygame.draw.line(SURF, (0, 255, 80), (bottom_right_x, bottom_right_y), (apex_x, apex_y), 1)
    pygame.draw.line(SURF, (0, 255, 80), (bottom_left_x, bottom_left_y), (middle_x, middle_y),  1)
    pygame.draw.line(SURF, (0, 255, 80), (bottom_right_x, bottom_right_y), (middle_x, middle_y), 1)


def draw_enemy(x, y, angle):
    apex_x = (shift(0, -10, angle, "x")) + x
    apex_y = (shift(0, -10, angle, "y")) + y

    middle_left_x = (shift(-3, 0, angle, "x")) + x
    middle_left_y = (shift(-3, 0, angle, "y")) + y

    middle_right_x = (shift(3, 0, angle, "x")) + x
    middle_right_y = (shift(3, 0, angle, "y")) + y

    bottom_left_x = (shift(-5, 10, angle, "x")) + x
    bottom_left_y = (shift(-5, 10, angle, "y")) + y

    bottom_right_x = (shift(5, 10, angle, "x")) + x
    bottom_right_y = (shift(5, 10, angle, "y")) + y

    bottom_middle_x = (shift(0, 8, angle, "x")) + x
    bottom_middle_y = (shift(0, 8, angle, "y")) + y

    pygame.draw.line(SURF, (255, 10, 0), (middle_left_x, middle_left_y),   (apex_x, apex_y),  1)
    pygame.draw.line(SURF, (255, 10, 0), (middle_right_x, middle_right_y), (apex_x, apex_y), 1)
    pygame.draw.line(SURF, (255, 10, 0), (middle_right_x, middle_right_y), (bottom_middle_x, bottom_middle_y), 1)
    pygame.draw.line(SURF, (255, 10, 0), (middle_left_x, middle_left_y),   (bottom_middle_x, bottom_middle_y), 1)
    pygame.draw.line(SURF, (255, 10, 0), (middle_right_x, middle_right_y), (bottom_right_x, bottom_right_y), 1)
    pygame.draw.line(SURF, (255, 10, 0), (middle_left_x, middle_left_y),   (bottom_right_x, bottom_right_y), 1)
    pygame.draw.line(SURF, (255, 10, 0), (middle_right_x, middle_right_y), (bottom_left_x, bottom_left_y), 1)
    pygame.draw.line(SURF, (255, 10, 0), (middle_left_x, middle_left_y),   (bottom_left_x, bottom_left_y), 1)


pygame.font.init()
myfont = pygame.font.SysFont("$HACKERMAN", 24)  # Initialize the font (dependency: $HACKERMAN font; available as FOSS on FontStruct)

angle = 0
x_momentum = 0
y_momentum = 0
x_pos = 500
y_pos = 300

bullet_x_vals = []
bullet_y_vals = []
bullet_angles = []

enemy_t = 0
enemy_x_pos = -20
enemy_y_pos = -20

enemybxv = []
enemybyv = []
enemybtv = []

cycle = 0

add = 1.8

score = 0

mode = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            print("Green fired " + str(len(bullet_angles)) + " shots")
            print("Red fired "   + str(len(enemybtv))      + " shots")
            pygame.quit()
            sys.exit()

    pygame.display.set_caption("Space by Dante Falzone")

    SURF.fill((0, 0, 0)) # Clear the screen

    keys = pygame.key.get_pressed()  # Callback for ingame keypresses

    if mode == 2:
        label = myfont.render("Human wins!", 3, (0, 255, 80))
        SURF.blit(label, (450, 280))
    if mode == 3:
        label = myfont.render("Computer wins!", 3, (255, 10, 0))
        SURF.blit(label, (440, 280))
    if mode == 1:
        draw_ship(x_pos, y_pos, angle)

        draw_enemy(enemy_x_pos, enemy_y_pos, enemy_t)

        # <COMPLICATED MATHS>
        if x_pos >= enemy_x_pos:
            add = 1.8
        else:
            add = 4.8
        m = (y_pos - enemy_y_pos) / (x_pos - enemy_x_pos)
        theta = math.atan(m)
        """
        The above trigonometric equations regarding the rotation of the ship could be expressed in normal notation as follows:

                   -1
        theta = tan  (y  - y )/(x  - x )
                       2    1    2    1

        where theta is the angle of the enemy to the player, and where the player is at the
        point (x , y ) and the enemy is at the point (x , y ).
                1   1                                  2   2
        """
        # </COMPLICATED MATHS>
        enemy_t = theta + add

        if keys[K_LEFT]:
            angle -= 0.1
        if keys[K_RIGHT]:
            angle += 0.1

        if keys[K_UP]:
            if -5 <= x_momentum <= 5:
                x_momentum -= shift(0.1, 0.1, angle + 44.77, "x")
            elif x_momentum < 0:
                x_momentum = -5
            elif x_momentum > 0:
                x_momentum = 5

            if -5 <= y_momentum <= 5:
                y_momentum -= shift(0.1, 0.1, angle + 44.77, "y")
            elif y_momentum < 0:
                y_momentum = -5
            elif y_momentum > 0:
                y_momentum = 5


        if keys[K_SPACE]:
            if cycle / 10 == cycle // 10:
                bullet_y_vals.append(y_pos)
                bullet_x_vals.append(x_pos)
                bullet_angles.append(angle)


        x_pos += x_momentum
        y_pos += y_momentum

        enemy_x_pos = ((99 * enemy_x_pos) + x_pos) / 100
        enemy_y_pos = ((99 * enemy_y_pos) + y_pos) / 100

        if cycle / 20 == cycle // 20:
            enemybyv.append(enemy_y_pos)
            enemybxv.append(enemy_x_pos)
            enemybtv.append(enemy_t)

        if x_pos >= 1011:
            x_pos = -10
        if x_pos <= -11:
            x_pos = 1010
        if y_pos >= 611:
            y_pos = -10
        if y_pos <= -11:
           y_pos = 610

        if bullet_angles:
            for n in range (0, len(bullet_angles) - 1):
                pygame.draw.line(SURF, (0, 255, 80), (bullet_x_vals[n], bullet_y_vals[n]), (bullet_x_vals[n] + 1, bullet_y_vals[n] + 1),  4)
                bullet_x_vals[n] -= shift(10, 10, bullet_angles[n] + 44.77, "x")
                bullet_y_vals[n] -= shift(10, 10, bullet_angles[n] + 44.77, "y")
                if enemy_x_pos - 16 < bullet_x_vals[n] < enemy_x_pos + 16:
                    if enemy_y_pos - 16 < bullet_y_vals[n] < enemy_y_pos + 16:
                        score += 1

        if enemybtv:
            for n in range (0, len(enemybtv) - 1):
                pygame.draw.line(SURF, (255, 10, 0), (enemybxv[n], enemybyv[n]), (enemybxv[n] + 1, enemybyv[n] + 1), 4)
                enemybxv[n] -= shift(10, 10, enemybtv[n] + 44.77, "x")
                enemybyv[n] -= shift(10, 10, enemybtv[n] + 44.77, "y")
                if x_pos - 16 < enemybxv[n] < x_pos + 16 and y_pos - 16 < enemybyv[n] < y_pos + 16:
                    score -= 1

        label0 = myfont.render("Score: " + str(score), 3, (0, 255, 80))
        SURF.blit(label0, (30, 570))

        if score >= 100:
            mode += 1

        if score <= -15:
            mode += 2

        if cycle <= 60:
            cycle += 1
        else:
            cycle = 0

    elif mode == 0:
        label1 = myfont.render("Instructions", 3, (0, 255, 80))
        label2 = myfont.render("Steering: left and right arrow keys", 3, (0, 255, 80))
        label3 = myfont.render("Thruster: up arrow key", 3, (0, 255, 80))
        label4 = myfont.render("Plasma Cannon: spacebar", 3, (0, 255, 80))
        label5 = myfont.render("You are trying to shoot the red ship and avoid getting shot.", 3, (0, 255, 80))
        label6 = myfont.render("Each time you hit them, your score (bottom left corner) increases by one." , 3, (0, 255, 80))
        label7 = myfont.render("Each time you're hit, your score goes down by one.", 3, (0, 255, 80))
        label71 = myfont.render("If your score goes above 100, you win.", 3, (255, 10, 0))
        label72 = myfont.render("If your score goes below -15, you lose.", 3, (255, 10, 0))
        label8 = myfont.render("PRESS X TO START", 3, (255, 10, 0))

        SURF.blit(label1, (400, 30))
        SURF.blit(label2, (30, 70))
        SURF.blit(label3, (30, 100))
        SURF.blit(label4, (30, 130))
        SURF.blit(label5, (30, 160))
        SURF.blit(label6, (30, 190))
        SURF.blit(label7, (30, 220))
        SURF.blit(label71,(30, 260))
        SURF.blit(label72,(30, 290))
        SURF.blit(label8, (30, 330))

        if keys[K_x]:
            mode += 1


    pygame.display.update()
    fpsClock.tick(60)
