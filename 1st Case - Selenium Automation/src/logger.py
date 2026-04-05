import os
import logging

from .constants import OUTPUT_FOLDER


os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logger = logging.getLogger("selenium_test")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(f"{OUTPUT_FOLDER}/output.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)
