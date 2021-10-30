import os
import logging
import logging.config


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "common_fluentd": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(process)d"
            "| %(thread)d | %(pathname)s:%(lineno)s | %(message)s",
            "style": "%",
        },
    },
    "heandlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "common_fluentd",
        },
    },

    "loggers": {
        "": {
            "handlers": ["console"],
            "level": os.getenv("LOG_LEVEL", "INFO")
        },
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(os.getenv("APP_NAME", "FLASK"))
