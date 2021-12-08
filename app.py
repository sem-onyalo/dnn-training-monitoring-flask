from app import init_app
from common.config import Config

app = init_app()

if __name__ == "__main__":
    config = Config()
    app.run(debug=config.debug, host=config.host, port=config.port)
