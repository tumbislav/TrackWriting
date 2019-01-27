# encoding: utf-8
# author: Marko Čibej
# file: __main__.py
"""
Entry point to the TrackWriting package.
"""

from paths import app
import webbrowser
import random


port = 5000  # + random.randint(0, 999)
url = "http://127.0.0.1:{0}".format(port)

# threading.Timer(1.25, lambda: webbrowser.open(url)).start()

# webbrowser.open(url)
app.run(port=port, debug=False)
