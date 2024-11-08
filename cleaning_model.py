import mesa
from cleaning_agent import CleaningAgent
from dirty_cell_agent import DirtyCellAgent
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
import random
import numpy as np

class CleaningModel(mesa.Model):
    def __init__(self, num_agents, width, height, dirty_percentage, max_steps):
        super().__init__()
        self.num_agents = num_agents
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.dirty_cells = int(width * height * dirty_percentage)
        self.clean_cells = width * height - self.dirty_cells
        self.max_steps = max_steps
        self.total_moves = 0
        self.steps_to_clean = None

        for i in range(self.num_agents):
            agent = CleaningAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))

        all_positions = [(x, y) for x in range(width) for y in range(height)]
        dirty_positions = random.sample(all_positions, self.dirty_cells)
        for idx, pos in enumerate(dirty_positions):
            dirty_agent = DirtyCellAgent(f"dirty_{idx}", self)
            self.schedule.add(dirty_agent)
            self.grid.place_agent(dirty_agent, pos)

    def step(self):
        self.schedule.step()

        self.total_moves = sum(agent.moves for agent in self.schedule.agents if isinstance(agent, CleaningAgent))

        if self.dirty_cells == 0 and self.steps_to_clean is None:
            self.steps_to_clean = self.schedule.steps

    def run_model(self):
        plt.figure(figsize=(6, 6))
        for i in range(self.max_steps):
            self.step()
            self.visualize_grid(i)
            if self.dirty_cells == 0:
                break

        clean_percentage = ((self.grid.width * self.grid.height - self.dirty_cells) / (self.grid.width * self.grid.height)) * 100
        print(f"Time required to clean all cells (or max time): {self.steps_to_clean or self.max_steps}")
        print(f"Percentage of clean cells after the simulation: {clean_percentage}%")
        print(f"Total number of moves made by all agents: {self.total_moves}")
        plt.show()

    def visualize_grid(self, step_num):
        grid_state = np.zeros((self.grid.width, self.grid.height), dtype=int)

        cmap = mcolors.ListedColormap(['white', 'gray', 'red'])
        bounds = [0, 1, 2, 3]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        for (content, position) in self.grid.coord_iter():
            x, y = position
            if any(isinstance(agent, DirtyCellAgent) for agent in content):
                grid_state[x, y] = 1
            elif any(isinstance(agent, CleaningAgent) for agent in content):
                grid_state[x, y] = 2

        plt.imshow(grid_state, cmap=cmap, norm=norm, origin="upper", extent=(0, self.grid.width, 0, self.grid.height))
        plt.title(f"Step {step_num}")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.draw()
        plt.pause(0.9)
        plt.clf()
