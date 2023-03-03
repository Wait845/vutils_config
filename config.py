import yaml
import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ConfigEventHandler(FileSystemEventHandler):
    def __init__(self, config_obj):
        self.config_obj = config_obj

    def on_modified(self, event):
        if event.src_path == self.config_obj.config_file_path:
            self.config_obj.refresh()


class Config:
    _instance = None
    _first_init = True

    def __init__(self, config_file_path):
        if not Config._first_init:
            return
        Config._first_init = False
        self.config_file_path = os.path.abspath(config_file_path)
        self.config = {}
        self.refresh()
        self.observer = Observer()
        self.observer.schedule(
            ConfigEventHandler(self),
            os.path.dirname(self.config_file_path),
            recursive=False
        )
        self.observer.start()

    def get(self, name, key, default=None):
        if name not in self.config:
            self.set(name, key, default)
            return default
        if key not in self.config[name]:
            self.set(name, key, default)
            return default
        return self.config[name][key]

    def set(self, name, key, value):
        if name not in self.config:
            self.config[name] = {}
        self.config[name][key] = value
        with open("config.yaml", "w") as f:
            yaml.dump(self.config, f, allow_unicode=True)

    def refresh(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        else:
            self.config = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __del__(self):
        self.observer.stop()
        self.observer.join()
