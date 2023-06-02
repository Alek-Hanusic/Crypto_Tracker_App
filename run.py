import os
import atexit
import subprocess as sp
import os

from PySide2 import QtCore, QtWebEngineWidgets, QtWidgets

def kill_server(p):
    if os.name == 'nt':
        # p.kill is not adequate
        sp.call(['taskkill', '/F', '/T', '/PID', str(p.pid)])
    elif os.name == 'posix':
        p.kill()
    else:
        pass

if __name__ == '__main__':
    cmd = f'streamlit run app.py --server.headless=True'

    p = sp.Popen(cmd.split(), stdout=sp.DEVNULL)
    atexit.register(kill_server, p)

    hostname = 'localhost'
    port = 8501

    app = QtWidgets.QApplication()
    view = QtWebEngineWidgets.QWebEngineView()
    # Set the initial width and height
    window_width = 1600
    window_height = 900

    # Set the new size
    view.resize(window_width, window_height)

    view.load(QtCore.QUrl(f'http://{hostname}:{port}'))
    view.show()
    app.exec_()
