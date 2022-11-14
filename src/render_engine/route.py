from dataclasses import dataclass


@dataclass
class Route:
    """Route class for the render engine."""

    filepath: str  # The Path relative to the output directory
    markup: str  # The markup to be rendered
    reference: str  # The reference that other routes can use to link to this object's filepath
