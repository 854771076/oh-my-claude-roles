import sys

from loguru import logger


def setup_logger(verbose: bool = False):
    """Setup logger with appropriate verbosity"""
    logger.remove()
    level = "DEBUG" if verbose else "INFO"

    # Console output
    logger.add(
        sys.stderr,
        level=level,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{message}</cyan>"
        ),
    )

    # File output with rotation
    logger.add(
        "logs/oh-roles.log",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8",
    )


__all__ = ["logger", "setup_logger"]
