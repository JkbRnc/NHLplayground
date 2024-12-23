import logging
from os import remove
from os.path import exists
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


def setup_logger(
    name: str,
    filename: str,
    level: int = logging.INFO,
    erase: bool = True,
    verbose: bool = False,
) -> logging.Logger:
    """Function for setting up logger.

    Args:
        name (str): logger name
        filename (str): output file name
        level (int, optional): level of logging displayed. Defaults to logging.INFO.
        erase (bool, optional): flag to erase past logging file. Defaults to True.
        verbose (bool, optional): flag to display logging messages to CMD line. Defaults to False.

    Returns:
        logging.Logger: Logger instance.
    """
    # Erase logging file if it exists
    if erase and exists(filename):
        remove(filename)
    # Configure logfile
    logger = logging.getLogger(name)
    formatter = logging.Formatter("%(message)s")
    fileHandler = logging.FileHandler(filename, mode="w")
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    logger.setLevel(level)
    logger.addHandler(fileHandler)
    if verbose:
        # CMD line prints
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

    return logger


def remove_defaults(
    data: dict[str, Any], cols: list[str] = ["firstName", "lastName"]
) -> dict:
    """Preprocessing function to extract names from raw data.

    Args:
        data (dict): Raw player data.

    Returns:
        dict: Raw player data with fixed names.
    """
    for col in cols:
        data[col] = data[col]["default"]
    return data
