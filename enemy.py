import pygame
import math
import os
from settings import PATH
from settings import PATH_RIGHT

# initialize the game and load the image.
pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))

# set the number of n on keyboard gets pressed.
number_of_n_pressed = 0


class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(
            ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path_index = 0
        self.move_count = 0

        self.counter = 0

        # goes left first due to EnemyGroup.generate() will cause the number_of_n_pressed becomes 1
        if number_of_n_pressed % 2 == 1:
            self.path = PATH
        else:
            # goes right in else block
            # flip the image when it's going the other way, so it looks somewhat natural.
            self.image = pygame.transform.flip(
                self.image, True, False)
            self.path = PATH_RIGHT

        self.x, self.y = self.path[0]
        # set the starting point of enemy

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width //
                              2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):

        pygame.draw.rect(win, (255, 0, 0), [
                         self.x, self.y - 35, 3.5 * (self.health), 4])
        # draw health bar in red
        pygame.draw.rect(win, (0, 255, 0), [
                         self.x - 3.5 * self.health, self.y - 35, 3.5 * (self.max_health - self.health), 4])
        # draw the missing health in green through substraction

    def move(self):

        # adjusting stride will impact how fast enemy goes
        stride = 1

        p_A = self.path[self.path_index]
        p_B = self.path[self.path_index + 1]
        ax, ay = p_A  # x, y position of point A
        bx, by = p_B
        distance_A_B = math.sqrt((ax - bx)**2 + (ay - by)**2)
        # total footsteps that needed from A to B
        max_count = int(distance_A_B / stride)

        if self.counter < max_count:
            # if the footsteps has not reached to total footsteps, than the the position of enemy keeps changing
            unit_vector_x = (bx - ax) / distance_A_B
            unit_vector_y = (by - ay) / distance_A_B
            delta_x = unit_vector_x * stride
            delta_y = unit_vector_y * stride

            # update the position of enemy and the counter
            self.x += delta_x
            self.y += delta_y
            self.counter += 1
        else:
            self.counter = 0
            self.path_index += 1


class EnemyGroup:
    def __init__(self):
        self.campaign_count = 0
        self.campaign_max_count = 120   # (unit: frame)
        self.reserved_members = []

        self.expedition = []

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        if self.is_empty() == False and self.campaign_count == self.campaign_max_count:
            # if the enemies are in bank and the frame reaches 120
            self.expedition.append(
                self.reserved_members.pop())
            # get() one enemy at a time
            self.campaign_count = 0
            # reset the frame count
        elif self.is_empty() == True:
            self.campaign_count = 0
            # if the enemies are all out, reset the frame count as well.
        else:
            self.campaign_count += 1
            # let the frame count pile up if the enemies are in bank and frames are not 120 yet

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        global number_of_n_pressed
        number_of_n_pressed += 1
        for i in range(num):
            self.reserved_members.append(Enemy())
        # generate Enemy for $num times

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)
