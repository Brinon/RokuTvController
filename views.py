from flask import current_app, Blueprint, render_template, request

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():

  power_is_on = current_app.roku.power_on
  current_roku_app = current_app.roku.get_active_app()
  installed_apps = current_app.roku.apps
  return render_template(
      'index.html',
      power_is_on=power_is_on,
      current_app=current_roku_app,
      installed_apps=installed_apps,
  )


@views.after_request
def log_request(response):
  current_app.logger.info('Incoming request from %s: %s %s -> %s', request.remote_addr,
                          request.method, request.path, response.status)
  return response
