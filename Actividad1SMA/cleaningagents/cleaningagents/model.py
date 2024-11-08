import mesa
import random

class CleanAgent(mesa.Agent):
    """
    An agent that moves randomly and cleans dirty cells.
    """

    def __init__(self, unique_id, model):
        """
        Initialize the agent.
        """
        super().__init__(unique_id, model)

    def step(self):
        """
        At each step, if the agent is on a dirty cell, it cleans it.
        Then it moves to a random neighboring cell.
        """
        # Obtener posición actual del agente
        x, y = self.pos

        # Limpiar la celda si está sucia
        if self.model.is_cell_dirty((x, y)):
            self.model.clean_cell((x, y))

        # Elegir una celda adyacente aleatoria y moverse
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)



class CleanModel(mesa.Model):
    """
    Model that holds agents and manages a grid with dirty cells.
    """

    def __init__(self, num_agents, width, height, dirty_percentage):
        super().__init__()
        self.num_agents = num_agents
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width=width, height=height, torus=False)

        # Inicializar celdas sucias con el porcentaje especificado
        self.dirty_cells = set()
        total_cells = width * height
        num_dirty_cells = int(total_cells * dirty_percentage)
        all_cells = [(x, y) for x in range(width) for y in range(height)]
        dirty_cells = random.sample(all_cells, num_dirty_cells)
        self.dirty_cells.update(dirty_cells)

        # Crear agentes
        for i in range(self.num_agents):
            agent = CleanAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))  # Coloca los agentes en [1,1] al inicio

        # Colector de datos
        self.datacollector = mesa.datacollection.DataCollector(
            {"Dirty Cells": lambda m: len(m.dirty_cells)}  # Número de celdas sucias restantes
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.datacollector.collect(self)
        self.schedule.step()

        # Terminar la simulación si no quedan celdas sucias
        if not self.dirty_cells:
            self.running = False

    def is_cell_dirty(self, pos):
        """
        Check if a cell is dirty.
        """
        return pos in self.dirty_cells

    def clean_cell(self, pos):
        """
        Clean a cell by removing it from the dirty cells set.
        """
        self.dirty_cells.discard(pos)
