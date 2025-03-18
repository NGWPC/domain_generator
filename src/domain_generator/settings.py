import configparser
import os
from pathlib import Path


class Settings:
    def __init__(self):
        config_file = Path.cwd() / "settings.ini"
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.headers = {
            'Accept': self.config["HEADERS"]["accept"],
            'User-Agent': self.config["HEADERS"]["user_agent"]
        }
        
        self.STAGES = set(self.config['STAGES']['stages'].split(','))

        self.gpkg_path = self.config['DEFAULT']["GPKG"]
        
        self.BASE_URL = self.config['DEFAULT']['BASE_URL']
        self.rate_limit = self.config.getint('DEFAULT', 'rate_limit')
        self.reach_limit = self.config.getint('DEFAULT', 'reach_limit')
        
        self.rabbitmq_username = self.config['RABBITMQ']['username']
        self.rabbitmq_password = self.config['RABBITMQ']['password']
        self.rabbitmq_host = self.config['RABBITMQ']['host']
        self.rabbitmq_port = self.config.getint('RABBITMQ', 'port')
        
        self.flooded_data_queue = self.config['QUEUES']['flooded_data']
        self.error_queue = self.config['QUEUES']['error']
        
        self.log_path = self.config['PATHS']['log_path']
        self.user = self.config['DEFAULT']['user']
        
        if os.getenv("RABBITMQ_HOST"):
            self.rabbitmq_host = os.getenv("RABBITMQ_HOST")
        if os.getenv("RABBITMQ_USERNAME"):
            self.rabbitmq_username = os.getenv("RABBITMQ_HOST")
        if os.getenv("RABBITMQ_PASSWORD"):
            self.rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")
        
        self.pika_url = f"amqp://{self.rabbitmq_username}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"
        
        if os.getenv("PIKA_URL"):
            self.pika_url = os.getenv("PIKA_URL")
