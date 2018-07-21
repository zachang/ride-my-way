import os
from app import create_app

config_name = os.getenv('DEV_ENVIRON')
app = create_app(config_name)

@app.route("/")
def home():
    return "Welcome to ride my way api"


if __name__ == "__main__":
    app.run()
