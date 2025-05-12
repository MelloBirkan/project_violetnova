from .normal import draw_normal_expression
from .excited import draw_excited_expression
from .curious import draw_curious_expression
from .surprised import draw_surprised_expression
from .warning import draw_warning_expression
from .happy import draw_happy_expression
from .alert import draw_alert_expression

# Dictionary mapping expression names to their drawing functions
EXPRESSION_FUNCTIONS = {
    "normal": draw_normal_expression,
    "excited": draw_excited_expression,
    "curious": draw_curious_expression,
    "surprised": draw_surprised_expression,
    "warning": draw_warning_expression,
    "happy": draw_happy_expression,
    "alert": draw_alert_expression
}