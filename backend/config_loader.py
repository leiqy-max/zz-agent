import yaml
import os

class Config:
    def __init__(self):
        self.db = {}
        self.llm = {}
        self.server = {}
        self.load_config()

    def load_config(self):
        config_path = "config.yaml"
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)
                self.db = config_data.get("database", {})
                self.llm = config_data.get("llm", {})
                self.server = config_data.get("server", {})
        else:
            print("Warning: config.yaml not found, using defaults/env vars")

config = Config()
