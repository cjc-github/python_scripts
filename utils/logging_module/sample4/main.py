from sample4_logger import setup_logging, info, warn, error

# 在 main.py 中设置 logger
logger = setup_logging(__file__)

def main():
    info("This is an info message from main.py.")
    warn("This is a warning message from main.py.")
    error("This is an error message from main.py.")

if __name__ == "__main__":
    main()