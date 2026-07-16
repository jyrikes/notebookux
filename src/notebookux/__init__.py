from .core import UX, NotebookUX, create_theme
from .lessons import available_algorithm_lessons, render_algorithm_lesson
from .parallelism import render_parallelism_demo

__version__ = "0.2.2"

__all__ = [
    "NotebookUX",
    "UX",
    "__version__",
    "available_algorithm_lessons",
    "create_theme",
    "render_algorithm_lesson",
    "render_parallelism_demo",
]
