import sys
import os
print('/home/itec/PythonProj/websen')
activate_this = '/home/itec/PythonProj/websen/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

sys.path.insert(0, '/home/itec/PythonProj/websen')
def application(environ, start_response):
    from websen import app 
    return app(environ, start_response)