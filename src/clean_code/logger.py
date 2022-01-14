import logging.config
from pathlib import Path
import yaml

_logger = logging.getLogger(__name__)


class LevelFormatter:
    """Logging Formatter to add colors"""

    def __init__(self, fmt=None, datefmt=None, style="%", validate=True):
        if fmt is None:
            # Specify color strings by name
            grey = "\x1b[38;21m"
            green = "\x1b[32;21m"
            yellow = "\x1b[33;21m"
            red = "\x1b[31;21m"
            bold_red = "\x1b[31;1m"
            reset = "\x1b[0m"
            # Define the generic format
            fmt_str = "%(asctime)s - %(name)s (%(filename)s:%(lineno)d) - %(levelname)s - %(message)s"
            # Specify the coloring
            fmt = {
                logging.DEBUG: grey + fmt_str + reset,
                logging.INFO: green + fmt_str + reset,
                logging.WARNING: yellow + fmt_str + reset,
                logging.ERROR: red + fmt_str + reset,
                logging.CRITICAL: bold_red + fmt_str + reset
            }

        self.formatters = {
            level: logging.Formatter(
                fmt=f,
                datefmt=datefmt,
                style=style,
                validate=validate
            )
            for level, f in fmt.items()
        }

    def format(self, record):
        return self.formatters.get(record.levelno).format(record)


def initialize_logging(logging_config_path=None):
    # Use a default logging configuration if a specific configuration is not supplied
    if logging_config_path is None:
        logging_config_path = Path(__file__).parent / "logging_config.yml"

    # Load the configuration
    logging_config = yaml.load(open(logging_config_path), Loader=yaml.FullLoader)

    # Ensure the paths exist, to which logs are to be saved
    debug_path = logging_config["logging"]["handlers"]["debug_file_handler"]["filename"]
    info_path = logging_config["logging"]["handlers"]["info_file_handler"]["filename"]
    warning_path = logging_config["logging"]["handlers"]["warning_file_handler"]["filename"]
    error_path = logging_config["logging"]["handlers"]["error_file_handler"]["filename"]
    critical_path = logging_config["logging"]["handlers"]["critical_file_handler"]["filename"]

    Path(debug_path).parent.mkdir(parents=True, exist_ok=True)
    Path(info_path).parent.mkdir(parents=True, exist_ok=True)
    Path(warning_path).parent.mkdir(parents=True, exist_ok=True)
    Path(error_path).parent.mkdir(parents=True, exist_ok=True)
    Path(critical_path).parent.mkdir(parents=True, exist_ok=True)

    # Load the logging configuration
    logging.config.dictConfig(logging_config["logging"])
    _logger.info("Config loaded")
