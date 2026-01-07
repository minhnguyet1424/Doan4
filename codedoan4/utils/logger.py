import logging
import os

def get_logger(test_file_name):
    os.makedirs("logs", exist_ok=True)

    log_file = f"logs/{test_file_name}.log"
    logger = logging.getLogger(test_file_name)
    logger.setLevel(logging.INFO)

    # QUAN TRỌNG: chỉ reset log 1 lần
    if not logger.handlers:
        #  XÓA FILE LOG CŨ (nếu tồn tại)
        if os.path.exists(log_file):
            os.remove(log_file)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        ch = logging.StreamHandler()

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
