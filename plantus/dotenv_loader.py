from os.path import join, dirname
from dotenv import load_dotenv


def load_dotenv_file():
    """
    Load the .env file for the settings
    """
    dotenv_path = join(dirname(dirname(__file__)), '.env')
    load_dotenv(dotenv_path)
