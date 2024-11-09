#----------------------------------------------------------
# M1 Actividad
#
# 8-Nov-2024
# Autores:
#           Sebastian Espinoza Farías A01750311
#           Jesús Guzmán Ortega A01799257
# This file defines the agent model as well as the two agents used ofr the simulation
# It includes the CleanAgent and the DirtyAgent and their behavior inside the model
#----------------------------------------------------------
import mesa
import random

class CleanAgent(mesa.Agent):
    """
    An agent that moves randomly and cleans dirty cells.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.movements = 0  # Individual movement counter

    def step(self):
        """
        If the agent is on a dirty cell, it cleans it.
        Then it moves to a random neighboring cell.
        """
        # Clean the cell if there is a DirtyAgent present
        cellContents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellContents:
            if isinstance(agent, DirtyAgent):
                agent.clean()  # Clean the dirty agent

        # Move to a random neighbor cell that is not occupied by another CleanAgent
        possibleSteps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        validSteps = [pos for pos in possibleSteps if all(not isinstance(a, CleanAgent) for a in self.model.grid.get_cell_list_contents([pos]))]
        
        if validSteps:  # Only move if there's a valid step
            newPosition = self.random.choice(validSteps)
            self.model.grid.move_agent(self, newPosition)
            self.movements += 1  # Increment movement counter


class DirtyAgent(mesa.Agent):
    """
    An agent representing dirt in a cell. Starts as green and turns white when cleaned.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.isDirty = True  # Start as dirty

    def clean(self):
        """
        Clean the agent, turning it from dirty (green) to clean (white).
        """
        self.isDirty = False


class CleanModel(mesa.Model):
    """
    Model that holds agents and manages a grid with dirty agents.
    """
    def __init__(self, numAgents, width, height, dirtyPercentage, maxSteps):
        super().__init__()
        self.numAgents = numAgents
        self.maxSteps = maxSteps
        self.currentStep = 0
        self.totalMovements = 0  # Total movements from ALL agents
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width=width, height=height, torus=False)
        self.cleanTime = None  # Time (steps to clean)
        self.finalCleanPercentage = 0  # Clean cells at the end

        # Create dirty agents based on the dirtyPercentage
        totalCells = width * height
        numDirtyCells = int(totalCells * dirtyPercentage)
        allCells = [(x, y) for x in range(width) for y in range(height)]
        dirtyCells = self.random.sample(allCells, numDirtyCells)
        
        for pos in dirtyCells:
            dirtyAgent = DirtyAgent(self.next_id(), self)
            self.schedule.add(dirtyAgent)
            self.grid.place_agent(dirtyAgent, pos)

        # Place all cleaning agents in (1, 1)
        for i in range(self.numAgents):
            cleanAgent = CleanAgent(self.next_id(), self)
            self.schedule.add(cleanAgent)
            self.grid.place_agent(cleanAgent, (1, 1))  # Start all agents in (1,1)

        # Data collector for dirty cells count and total movements
        self.datacollector = mesa.datacollection.DataCollector(
            {
                "Dirty Cells": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, DirtyAgent) and agent.isDirty),
                "Total Movements": lambda m: sum(agent.movements for agent in m.schedule.agents if isinstance(agent, CleanAgent))
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        A model step. Collects data and advances the schedule.
        """
        self.currentStep += 1
        self.datacollector.collect(self)
        self.schedule.step()

        # Check if all cells are clean
        dirtyCellsRemaining = any(isinstance(agent, DirtyAgent) and agent.isDirty for agent in self.schedule.agents)
        
        if not dirtyCellsRemaining and self.cleanTime is None:
            self.cleanTime = self.currentStep  # Current step at the end to measure time

        # Stop if no dirty agents remain or max steps reached
        if not dirtyCellsRemaining or self.currentStep >= self.maxSteps:
            self.running = False
            # Clean cell percentage operations
            totalDirtyCells = sum(1 for agent in self.schedule.agents if isinstance(agent, DirtyAgent))
            cleanedCells = sum(1 for agent in self.schedule.agents if isinstance(agent, DirtyAgent) and not agent.isDirty)
            self.finalCleanPercentage = (cleanedCells / totalDirtyCells) * 100 if totalDirtyCells > 0 else 100

            # All movements
            self.totalMovements = sum(agent.movements for agent in self.schedule.agents if isinstance(agent, CleanAgent))
