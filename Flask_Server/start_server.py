import sys
from api_server import CreateApp

if len(sys.argv) == 1:
    app = CreateApp('dev')
elif len(sys.argv) == 2:
    if sys.argv[1] in ['test', 'dev', 'default']:
        app = CreateApp(sys.argv[1])
    else:
        raise ValueError("Wrong configuration name")
else:
    raise ValueError("Too much arguments")

if __name__ == "__main__":
    app.run(debug=True)
