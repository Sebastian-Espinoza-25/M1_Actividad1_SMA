"""
Configure visualization elements and instantiate a server
"""

from .model import CleanModel, CleanAgent, DirtyAgent
import mesa
from mesa.visualization.modules import TextElement


class modelData(TextElement):
    """
    Display custom data from the model.
    """
    def render(self, model):
        # show results at the end of the simulation
        if not model.running:  # The results only show when the simulation reaches end by cleaning or max steps
            clean_time = model.clean_time if model.clean_time is not None else model.current_step
            clean_percentage = model.final_clean_percentage
            total_movements = model.total_movements
            return f"Tiempo necesario para limpiar ó fin de ejecución: {clean_time} pasos<br>" \
                   f"Porcentaje de celdas limpias: {clean_percentage:.2f}%<br>" \
                   f"Total de movimientos de agentes: {total_movements}"
        else:
            return "Simulación en ejecución..."

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

# Automatic cell adjustment based on key args
def create_canvas_element(width, height):
    # Size of the display on the browser
    display_width = 500
    display_height = 500
    # cell calculation
    cell_width = display_width // width
    cell_height = display_height // height
    return mesa.visualization.CanvasGrid(portrayal_method, width, height, cell_width * width, cell_height * height)

# Text for the data collected
custom_text_element = modelData()

# Key Arguments for the start of the simulation
model_kwargs = {"num_agents": 40, "width": 40, "height": 40, "dirty_percentage": .8, "max_steps": 100}

# Canvas element with dynamic adjustment
canvas_element = create_canvas_element(model_kwargs["width"], model_kwargs["height"])

# Remaining cells graph
chart_element = mesa.visualization.ChartModule(
    [{"Label": "Dirty Cells", "Color": "Pink"}]
)

# setup server
server = mesa.visualization.ModularServer(
    CleanModel,
    [canvas_element, chart_element, custom_text_element],
    "Cleaning Agents Simulation",
    model_kwargs,
)

server.port = 8521
