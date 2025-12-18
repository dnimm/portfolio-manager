# main.py

from portfolioapp import create_app
from portfolioapp.config import Config

# create the flask app using the factory function
app = create_app(Config)

if __name__ == "__main__":
    app.run()
