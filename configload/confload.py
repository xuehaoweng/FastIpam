# -*- coding: utf-8 -*-
import os
import json
import yaml
import logging
import logging.config
from pathlib import Path

log = logging.getLogger(__name__)

CONFIG_FILENAME = "config/config.json"
DEFAULTS_FILENAME = "config/defaults.json"
NAMESPACE = "public"
try:
    yaml_loader = yaml.CSafeLoader
except AttributeError:
    yaml_loader = yaml.SafeLoader


def load_config_files(
        defaults_filename: str = DEFAULTS_FILENAME, config_filename: str = CONFIG_FILENAME
) -> dict:
    data = {}

    for fname in (defaults_filename, config_filename):
        try:
            with open(fname) as infil:
                data.update(json.load(infil))
        except FileNotFoundError:
            log.warning(f"Couldn't find {fname}")

    if not data:
        raise RuntimeError(
            f"Could not find either {defaults_filename} or {config_filename}"
        )

    return data


class Config:
    _instance = None

    def __init__(self):
        data = load_config_files()

        self.data = data

    # 单例模式
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    # 项目日志配置
    def setup_logging(self, max_debug=False):
        with open(self.log_config_filename) as infil:
            log_config_dict = yaml.load(infil, Loader=yaml_loader)

        if max_debug:
            for handler in log_config_dict["handlers"].values():
                handler["level"] = "DEBUG"

            for logger in log_config_dict["loggers"].values():
                logger["level"] = "DEBUG"

            log_config_dict["root"]["level"] = "DEBUG"

        logging.config.dictConfig(log_config_dict)
        log.info(f"confload: Logging setup @ {__name__}")

    # 获取项目根目录
    @property
    def get_root_path(self):
        file_path = Path(__file__).resolve()  # 获取当前文件的绝对路径
        root_path = file_path.parent  # 获取当前文件所在目录的路径
        while root_path.name != self.project_name:  # 根据实际情况修改根目录的名称
            root_path = root_path.parent  # 获取上级目录的路径
        return root_path


config = Config()
