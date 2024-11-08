"""
Configure visualization elements and instantiate a server
"""

from .model import CleanModel, CleanAgent  
import mesa

def circle_portrayal_example(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
        "Color": "Pink",
    }
    return portrayal

# Canvas grid for visualizing the agents in a 10x10 grid with each cell 500x500 pixels
canvas_element = mesa.visualization.CanvasGrid(
    circle_portrayal_example, 10, 10, 500, 500
)

# grafico para ver cuantas celdas sucias quedan
chart_element = mesa.visualization.ChartModule(
    [{"Label": "Dirty Cells", "Color": "Pink"}]
)

# PARAMETROS
model_kwargs = {"num_agents": 10, "width": 10, "height": 10, "dirty_percentage": 1}

# Set Up
server = mesa.visualization.ModularServer(
    CleanModel,
    [canvas_element, chart_element],
    "Cleaning Agents Simulation",
    model_kwargs,
)

# Set up port = 8521
server.port = 8521  
