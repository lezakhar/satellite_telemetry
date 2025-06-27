import logging
import sys
from typing import Optional


class ProjectLogger:
    """A customizable logger for consistent logging across the entire project.

    Supports info, warning, and error logging with configurable formatting.

    Usage example:
    from logger import logger

    if __name__ == "__main__":
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")

        try:
            1 / 0
        except ZeroDivisionError:
            logger.exception("An exception occurred")
    """

    def __init__(
        self,
        name: str = "project",
        log_file: Optional[str] = None,
        level: int = logging.INFO,
    ):
        """Initialize the logger.

        :param name: Name of the logger (usually __name__ of the calling module)
        :type name: str
        :param log_file: Path to log file. If None, logs only to console
        :type log_file: Optional[str]
        :param level: Minimum logging level (default: logging.INFO)
        :type level: int
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent adding handlers multiple times
        if not self.logger.handlers:
            self._setup_handlers(log_file, level)

    def _setup_handlers(self, log_file: Optional[str], level: int):
        """Configure handlers for console and optionally file output.

        :param log_file: Path to log file, or None for no file logging
        :type log_file: Optional[str]
        :param level: Minimum logging level
        :type level: int
        """
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler if log file is specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str, **kwargs):
        """Log an info message.

        :param message: The message to log
        :type message: str
        :param kwargs: Additional arguments for the logging method
        """
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log a warning message.

        :param message: The warning message to log
        :type message: str
        :param kwargs: Additional arguments for the logging method
        """
        self.logger.warning(message, **kwargs)

    def error(self, message: str, exc_info: bool = False, **kwargs):
        """Log an error message.

        :param message: Error message to log
        :type message: str
        :param exc_info: Whether to include exception info, defaults to False
        :type exc_info: bool
        :param kwargs: Additional arguments for the logging method
        """
        self.logger.error(message, exc_info=exc_info, **kwargs)

    def exception(self, message: str, **kwargs):
        """Log an exception message with exception info.

        :param message: The exception message to log
        :type message: str
        :param kwargs: Additional arguments for the logging method
        """
        self.logger.exception(message, **kwargs)


logger = ProjectLogger(name="satellite_telemetry")
