from services.rename_service import rename_service
import argparse
from datetime import datetime
import logging
import logging.config
import os
from os import path
from pathlib import Path as libPath

def initialize_logging(ss):
    log_settings = ss.data.get("logging")
    log_config_dir = log_settings.get("log_config_dir")
    log_config_file = log_settings.get("log_config_file")

    app_file_path = libPath(__file__)
    app_root = app_file_path.parent

    #log_file_path = path.join(app_root, log_config_dir, log_config_file)

    #print(log_file_path)

    log_file_path = path.join(path.dirname(path.abspath(__file__)), log_config_dir, log_config_file)

    log_dir = log_settings.get("log_dir")
    file_name = log_settings.get("log_file_name")
    log_path = path.join(log_dir, file_name)

    rfh_settings = log_settings.get("rotating_file_handler")
    max_bytes = rfh_settings.get("max_bytes")
    backup_count = rfh_settings.get("backup_count")
    logging.config.fileConfig(log_file_path, defaults={'logfilename': log_path, 'maxBytes': max_bytes, 'backupCount': backup_count})

def run(command_service):
    command_service.parse_commands()

settings_service = SettingsService()
initialize_logging(settings_service)
logger = logging.getLogger()
logger.warning("Beginning execution...")
cache_service = CacheService(settings_service, logger)
mcrcon_service = McrconService(settings_service, cache_service, logger)
webhook_service = WebhookService(settings_service, logger)
sqlite_service = SQLiteService(settings_service, logger)
command_service = CommandService(settings_service, mcrcon_service, cache_service, webhook_service, sqlite_service, logger)
run(command_service)

logger.warning("Ending execution...")
