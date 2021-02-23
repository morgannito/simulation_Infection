import random
import arcade
import math

# --- Constants ---
AGENT_COUNT = 50
AGENT_INFECTED_COUNT = 1
AGENT_SPEED = 5
AGENT_FRAMES_BETWEEN_UPDATE = 120

CIRCLE_RADIUS = 30

AGENT_WHITE = (255, 255, 255)
AGENT_RED = (255, 0, 0)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


# Inherit from SpriteCircle in order to show a solid-colored circle
class Agent(arcade.SpriteCircle):
    def __init__(self, position):
        # Create a circle with a size of 10 and the given color
        super().__init__(CIRCLE_RADIUS, AGENT_WHITE)

        # Set the initial position
        self.center_x = position[0]
        self.center_y = position[1]

        # Count frames (calls to update())
        self.frame_count = 0

        # Set an initial speed
        self.change_speed()

    def update(self):
        # Count a frame
        self.frame_count += 1

        # Every once in a while, change direction
        if self.frame_count % AGENT_FRAMES_BETWEEN_UPDATE == 0:
            self.change_speed()

        # Move, but stay within bounds of the screen
        self.center_x = arcade.clamp(self.center_x + self.speed[0], 0, SCREEN_WIDTH)
        self.center_y = arcade.clamp(self.center_y + self.speed[1], 0, SCREEN_HEIGHT)

    def change_speed(self):
        # Pick a random direction
        angle = random.random() * 2 * math.pi
        # Translate the angle to x and y coordinates
        self.speed = (math.cos(angle) * AGENT_SPEED, math.sin(angle) * AGENT_SPEED)

    def change_color(self, color):
        self.texture = arcade.make_circle_texture(CIRCLE_RADIUS * 2, color)


class Simulation(arcade.Window):
    def __init__(self):
        # Show a window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Simulation")
        # A sprite list contains a list of sprites that can be easily manipulated
        self.agent_list = arcade.SpriteList()
        self.ennemis_list = arcade.SpriteList()
        # Create the agents
        for i in range(AGENT_COUNT):
            # Pick a random position on the screen
            position = (random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT))
            # Create the agent and add it to the list
            agent = Agent(position)
            agent.color = (255, 255, 255)
            self.agent_list.append(agent)
        # Create the agents
        for i in range(AGENT_INFECTED_COUNT):
            # Pick a random position on the screen
            position = (random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT))
            # Create the agent and add it to the list
            agent = Agent(position)
            agent.color = (255, 0, 0)
            self.ennemis_list.append(agent)

    def update(self, delta_time):
        # Update all the agents
        for enemy in self.agent_list:
            any_collisions = arcade.check_for_collision_with_list(enemy, self.ennemis_list)
            if len(any_collisions) > 0:
                self.ennemis_list.append(enemy)
                self.agent_list.remove(enemy)
                enemy.color = (255, 0, 0)
                enemy.update()
        self.agent_list.update()
        self.ennemis_list.update()

    def on_draw(self):
        # Clear the previous screen
        arcade.start_render()

        # Show all the agents
        self.agent_list.draw()
        self.ennemis_list.draw()


def main():
    simulation = Simulation()
    arcade.run()


if __name__ == "__main__":
    main()
