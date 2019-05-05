from flask import (
    flash,
    current_app,
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

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


@views.route('/launch/<app_id>', methods=['POST'])
def launch(app_id):
  current_app.roku.launch_app(app_id=app_id)
  flash(f'Launching {app_id}')
  return redirect(url_for('views.index'))


@views.route('/power/<value>', methods=['POST'])
def power(value):
  """ switch the power of the device """
  if value == 'on':
    current_app.roku.turn_on()
  elif value == 'off':
    current_app.roku.turn_off()
  else:
    raise ValueError(f'value shoud be one of on, off')
  return redirect(url_for('views.index'))


@views.after_request
def log_request(response):
  current_app.logger.info('Incoming request from %s: %s %s -> %s', request.remote_addr,
                          request.method, request.path, response.status)
  return response
