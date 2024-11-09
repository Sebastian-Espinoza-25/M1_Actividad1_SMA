#----------------------------------------------------------
# M1 Actividad
#
# 8-Nov-2024
# Autores:
#           Sebastian Espinoza Farías A01750311
#           Jesús Guzmán Ortega A01799257
# This file is the definition of the server to display the simulation for the 
# cleaning agents. It helps display the model.py file which contains the model and the agents behavior
#----------------------------------------------------------

"""
Configure visualization elements and instantiate a server
"""

from .model import CleanModel, CleanAgent, DirtyAgent
import mesa
from mesa.visualization.modules import TextElement


class ModelData(TextElement):
    """
    Display custom data from the model.
    """
    def render(self, model):
        # Show results at the end of the simulation
        if not model.running:  # The results only show when the simulation reaches end by cleaning or max steps
            cleanTime = model.cleanTime if model.cleanTime is not None else model.currentStep
            cleanPercentage = model.finalCleanPercentage
            totalMovements = model.totalMovements
            return f"Tiempo necesario para limpiar o fin de ejecución: {cleanTime} pasos<br>" \
                   f"Porcentaje de celdas limpias: {cleanPercentage:.2f}%<br>" \
                   f"Total de movimientos de agentes: {totalMovements}"
        else:
            return "Simulación en ejecución..."


def portrayalMethod(agent):
    """
    Define the visual representation for cleaning and dirty agents.
    """
    if agent is None:
        return
    
    # Representation for CleanAgent (pink circle)
    if isinstance(agent, CleanAgent):
        return {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 1,
            "r": 0.5,
            "Color": "Pink",
        }
    
    # Representation for DirtyAgent (green if dirty, white if clean)
    if isinstance(agent, DirtyAgent):
        color = "green" if agent.isDirty else "white"
        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": color,
            "w": 1,
            "h": 1,
        }


def createCanvasElement(width, height):
    """
    Automatic cell adjustment based on key args.
    """
    displayWidth = 500
    displayHeight = 500
    cellWidth = displayWidth // width
    cellHeight = displayHeight // height
    return mesa.visualization.CanvasGrid(portrayalMethod, width, height, cellWidth * width, cellHeight * height)


# Text for the data collected
customTextElement = ModelData()

# Key Arguments for the start of the simulation
modelKwargs = {"numAgents": 10, "width": 10, "height": 10, "dirtyPercentage": 0.8, "maxSteps": 100}

# Canvas element with dynamic adjustment
canvasElement = createCanvasElement(modelKwargs["width"], modelKwargs["height"])

# Remaining cells graph
chartElement = mesa.visualization.ChartModule(
    [{"Label": "Dirty Cells", "Color": "Pink"}]
)

# Setup server
server = mesa.visualization.ModularServer(
    CleanModel,
    [canvasElement, chartElement, customTextElement],
    "Cleaning Agents Simulation",
    modelKwargs,
)

server.port = 8521
