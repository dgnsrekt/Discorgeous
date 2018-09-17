import logging
import logging.config
import structlog
import sys

from paths import INFO_LOG_PATHS, ERROR_LOG_PATHS


def configure_logs(*, log_level):

    pre_chain = [
        # Add the log level and a timestamp to the event_dict if the log entry
        # is not from structlog.
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
    ]

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(colors=False),
                    "foreign_pre_chain": pre_chain,
                },
                "colored": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(colors=True),
                    "foreign_pre_chain": pre_chain,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": f"{log_level}",
                    "formatter": "colored",
                },
                "error_logfile": {
                    "level": "ERROR",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "when": "midnight",
                    "backupCount": 1,
                    "filename": ERROR_LOG_PATHS,
                    "formatter": "plain",
                },
                "info_logfile": {
                    "level": "INFO",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "when": "midnight",
                    "backupCount": 1,
                    "filename": INFO_LOG_PATHS,
                    "formatter": "plain",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["console", "error_logfile", "info_logfile"],
                    "level": "DEBUG",
                    "propagate": True,
                }
            },
        }
    )
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            # structlog.stdlib.render_to_log_kwargs,
            # structlog.processors.KeyValueRenderer,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
