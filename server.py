__author__ = "@samparsky"

from src.api import app
from src.config import Settings

app.run(debug=Settings.get('debug'), port=Settings.get('port'))