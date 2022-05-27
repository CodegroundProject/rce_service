import logging
import logging.config

from pyms.flask.app import Microservice
from project.models.init_db import db


class RCEMicroservice(Microservice):
    def init_libs(self) -> None:

        db.init_app(self.application)
        with self.application.test_request_context():
            db.create_all()

    def init_logger(self) -> None:
        if not self.application.config["DEBUG"]:
            super().init_logger()
        else:
            level = "DEBUG"
            LOGGING = {
                'version': 1,
                'disable_existing_loggers': False,
                'handlers': {
                    'console': {
                        'level': level,
                        'class': 'logging.StreamHandler',
                    },
                },
                'loggers': {
                    '': {
                        'handlers': ['console'],
                        'level': level,
                        'propagate': True,
                    },
                    'anyconfig': {
                        'handlers': ['console'],
                        'level': "WARNING",
                        'propagate': True,
                    },
                    'pyms': {
                        'handlers': ['console'],
                        'level': "WARNING",
                        'propagate': True,
                    },
                    'root': {
                        'handlers': ['console'],
                        'level': level,
                        'propagate': True,
                    },
                }
            }

            logging.config.dictConfig(LOGGING)


def create_app() -> None:
    """Initialize the Flask app, register blueprints and intialize all libraries like Swagger, database, the trace system...
    return the app and the database objects.
    :return:
    """
    ms = RCEMicroservice(path=__file__)

    return ms.create_app()
