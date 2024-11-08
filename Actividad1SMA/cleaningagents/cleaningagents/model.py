import mesa
import random

class CleanAgent(mesa.Agent):
    """
    An agent that moves randomly and cleans dirty cells.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        """
        If the agent is on a dirty cell, it cleans it.
        Then it moves to a random neighboring cell.
        """
        # Clean the cell if there is a DirtyAgent present
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if isinstance(agent, DirtyAgent):
                agent.clean()  # Clean the dirty agent

        # Move to a random neighboring cell that is not occupied by another CleanAgent
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        valid_steps = [pos for pos in possible_steps if all(not isinstance(a, CleanAgent) for a in self.model.grid.get_cell_list_contents([pos]))]
        
        if valid_steps:  # Only move if there's a valid step
            new_position = self.random.choice(valid_steps)
            self.model.grid.move_agent(self, new_position)


class DirtyAgent(mesa.Agent):
    """
    An agent representing dirt in a cell. Starts as green and turns white when cleaned.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_dirty = True  # Start as dirty

    def clean(self):
        """
        Clean the agent, turning it from dirty (green) to clean (white).
        """
        self.is_dirty = False


class CleanModel(mesa.Model):
    """
    Model that holds agents and manages a grid with dirty agents.
    """
    def __init__(self, num_agents, width, height, dirty_percentage, max_steps):
        super().__init__()
        self.num_agents = num_agents
        self.max_steps = max_steps  # step limit
        self.current_step = 0  # step counter to end simulation if reached
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width=width, height=height, torus=False)

        # Create dirty agents based on the dirty_percentage
        total_cells = width * height
        num_dirty_cells = int(total_cells * dirty_percentage)
        all_cells = [(x, y) for x in range(width) for y in range(height)]
        dirty_cells = self.random.sample(all_cells, num_dirty_cells)
        
        for pos in dirty_cells:
            dirty_agent = DirtyAgent(self.next_id(), self)
            self.schedule.add(dirty_agent)
            self.grid.place_agent(dirty_agent, pos)

        # Place all cleaning agents in (1, 1)
        for i in range(self.num_agents):
            clean_agent = CleanAgent(self.next_id(), self)
            self.schedule.add(clean_agent)
            self.grid.place_agent(clean_agent, (1, 1))  # Start all agents in (1,1)

        # Data collector for dirty cells count
        self.datacollector = mesa.datacollection.DataCollector(
            {"Dirty Cells": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, DirtyAgent) and agent.is_dirty)}
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        A model step. Collects data and advances the schedule.
        """
        self.current_step += 1
        self.datacollector.collect(self)
        self.schedule.step()

        # Stop if no dirty agents remain or max steps reached
        if not any(isinstance(agent, DirtyAgent) and agent.is_dirty for agent in self.schedule.agents) or self.current_step >= self.max_steps:
            self.running = False