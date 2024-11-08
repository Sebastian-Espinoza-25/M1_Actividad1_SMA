"""
Configure visualization elements and instantiate a server
"""

from .model import CleanModel, CleanAgent, DirtyAgent
import mesa

def portrayal_method(agent):
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
        color = "green" if agent.is_dirty else "white"
        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": color,
            "w": 1,
            "h": 1,
        }

# Canvas grid for visualizing agents in a 10x10 grid
canvas_element = mesa.visualization.CanvasGrid(
    portrayal_method, 10, 10, 500, 500
)

# Chart to show remaining dirty cells over time
chart_element = mesa.visualization.ChartModule(
    [{"Label": "Dirty Cells", "Color": "Pink"}]
)

# Model parameters
model_kwargs = {"num_agents": 10, "width": 10, "height": 10, "dirty_percentage": .5}

# Set up the server
server = mesa.visualization.ModularServer(
    CleanModel,
    [canvas_element, chart_element],
    "Cleaning Agents Simulation",
    model_kwargs,
)

# Set up port = 8521
server.port = 8521
