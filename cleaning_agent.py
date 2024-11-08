import mesa
from dirty_cell_agent import DirtyCellAgent

class CleaningAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.moves = 0
    
    def step(self):
        self.clean()
        self.move()
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        
        new_position = self.random.choice(possible_steps)
        
        next_cell_contents = self.model.grid.get_cell_list_contents([new_position])
        if not any(isinstance(agent, CleaningAgent) for agent in next_cell_contents):
            self.model.grid.move_agent(self, new_position)
            self.moves += 1
        else:
            pass
    
    def clean(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, DirtyCellAgent):
                self.model.schedule.remove(agent)
                self.model.grid.remove_agent(agent)
                self.model.dirty_cells -= 1
                self.model.clean_cells += 1
                break