import logging
import xml.etree.ElementTree as ET

from dataclasses import dataclass
import requests

logger = logging.getLogger(__name__)


class RequestsException(Exception):
  pass


class AppNotInstalledException(Exception):
  pass


@dataclass
class RokuApp:
  name: str
  app_id: str
  app_type: str
  version: str


class Roku:
  """ Object representing a Roku tv """

  def make_request(self, method, endpoint, ok_codes=None, **kwargs):
    url = self.url + endpoint
    ok_codes = ok_codes or [200]
    r = requests.request(method, url, **kwargs)
    if r.status_code not in ok_codes:
      raise RequestsException(f'request {method} {url} failed with status code: {r.status_code}, '
                              f'text: {r.text}')
    return r

  def __init__(self, url):
    self.url = f'http://{url}:8060'
    self.make_request('get', '/')
    self.apps = self.list_apps()

  def press_key(self, key):
    self.make_request('post', f'/keydown/{key}')

  def turn_on(self):
    if self.power_on:
      return
    self.press_key('power')

  def turn_of(self):
    if not self.power_on:
      return
    self.press_key('power')

  @property
  def power_on(self):
    r = self.make_request('get', '/query/device-info')
    tree = ET.fromstring(r.text)
    power_mode = tree.find('power-mode').text
    return power_mode == 'PowerOn'

  def list_apps(self):
    """ list the installed apps on the device """
    r = self.make_request('get', '/query/apps')
    # parse the xml app list
    # <apps>
    #   <app id="...", ...>AppName</app>
    #   ....
    #   <app></app>
    # </apps>
    tree = ET.fromstring(r.text)
    return [
        RokuApp(
            name=app_element.text.replace(u'\xa0', ' '),
            app_id=app_element.attrib.get('id'),
            app_type=app_element.attrib.get('type'),
            version=app_element.attrib.get('version'),
        ) for app_element in tree
    ]

  def get_active_app(self):
    r = self.make_request('get', '/query/active-app')
    tree = ET.fromstring(r.text)
    app_element = tree[0]
    return RokuApp(
        name=app_element.text.replace(u'\xa0', ' '),
        app_id=app_element.attrib.get('id'),
        app_type=app_element.attrib.get('type'),
        version=app_element.attrib.get('version'),
    )

  def launch_app(self, app_name):
    app = [a for a in self.apps if a.name == app_name]
    if not app:
      raise AppNotInstalledException(f'App {app_name} is not installed in the tv')
    app = app[0]
    self.make_request('post', f'/launch/{app.app_id}')
