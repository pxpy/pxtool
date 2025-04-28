__version__ = '0.1.2'

from .json_deal import remove_json_wrapper
from .set_log import setup_logger
__all__ = ['remove_json_wrapper', 'setup_logger']