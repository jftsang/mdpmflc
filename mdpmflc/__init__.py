from flask import Flask
from .config import *
from .logger import mflog

app = Flask(__name__)
