
from .warning import draw_warning_expression

from .alert import draw_alert_expression

# Dictionary mapping expression names to their drawing functions
EXPRESSION_FUNCTIONS = {
    "warning": draw_warning_expression,
    "alert": draw_alert_expression
}