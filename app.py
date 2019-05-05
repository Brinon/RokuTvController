import flask
import os
import logging

from flask import Flask
from roku import Roku


def make_app():
  app = Flask(__name__)
  # app.config.from_object('config')
  app.config.update(
      DEBUG=True,
      TESTING=True,
      ROKU_TV_IP='192.168.0.5',
      SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
      LOGLEVEL=logging.info,
  )

  # setup loggers
  gunicorn_logger = logging.getLogger('gunicorn.info')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)

  from views import views
  app.register_blueprint(views)
  roku = Roku(app.config['ROKU_TV_IP'])
  app.roku = roku
  app.glogger = gunicorn_logger
  return app


if __name__ == '__main__':
  app = make_app()
  app.run(host='0.0.0.0', debug=True)
