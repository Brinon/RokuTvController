import flask
import os
import logging

from flask import Flask
from roku import Roku


def make_app():
  app = Flask(__name__)
  app.config.from_object('config')

  # setup loggers
  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)

  from views import views
  app.register_blueprint(views)
  roku = Roku(app.config['ROKU_TV_IP'])
  app.roku = roku

  return app
