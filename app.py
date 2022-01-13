import argparse

from app import init_app
from common.config import Config

def get_runtime_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", type=bool, default=True, help="Is debug mode")
    parser.add_argument("-i", "--host_ip", type=str, default="0.0.0.0", help="The host IP")
    parser.add_argument("-p", "--host_port", type=str, default="8080", help="The host port")
    parser.add_argument("-s", "--storage", type=str, default="test", help="The storage type")
    parser.add_argument("-r", "--storage_name", type=str, default="gan-training-storage", help="The storage container/bucket name")
    parser.add_argument("-a", "--auto_refresh_seconds", type=int, default=60, help="Number of seconds to auto-refresh the webpage")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_runtime_args()
    config = Config(args)
    app = init_app(config)
    app.run(debug=config.debug, host=config.host, port=config.port)
