from flask import Flask
from towerlib import Tower
from awx_proxy.models import PlexDownloads
import logging
import sys
import consul
import os

app = Flask(__name__)
c = consul.Consul()
consul_path = "awx_proxy/"
keys = c.kv.get(consul_path, keys=True)
config_keys = keys[1]
for key in config_keys:
    if key != consul_path:
        config_key = key.replace(consul_path, '')
        if os.environ.get(config_key):
            app.config[config_key] = os.environ.get(config_key)
        else:
            index, data = c.kv.get(key)
            app.config[config_key] = data['Value'].decode("utf-8")
handler = logging.StreamHandler(sys.stdout)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
required_configs = ['TOWER_HOST', 'TOWER_USER', 'TOWER_PASSWORD']

@app.route('/')
def hello():
    return "Welcome the AWX Proxy!"


@app.route('/health')
def health_check():
    for config in required_configs:
        value = app.config.get(config)
        if value is None:
            raise Exception("{} missing from config".format(config))
    # can i connect to tower?
    Tower(app.config.get('TOWER_HOST'), app.config.get('TOWER_USER'), app.config.get('TOWER_PASSWORD'))
    return "Success"


@app.route('/config')
def config():
    response_text = ""
    for config in required_configs:
        value = app.config.get(config)
        if any(secret in config for secret in ['KEY', 'TOKEN', 'PASSWORD']):
            response_text += "{}: [REDACTED]<br/>".format(config)
        else:
            response_text += "{}: {}<br/>".format(config, value)
    return response_text


@app.route('/upgrade_plex', methods=['GET', 'POST'])
def upgrade_plex():
    app.logger.info("Upgrade Plex Called, running against tower host: {}".format(app.config.get('TOWER_HOST')))
    tower = Tower(app.config.get('TOWER_HOST'), app.config.get('TOWER_USER'), app.config.get('TOWER_PASSWORD'))
    plex_update_job_template = tower.get_job_template_by_name("Plex Update")
    plex_download = PlexDownloads()
    plex_download.get_latest_version_from_plex()
    plex_version = plex_download.get_latest_version()
    extra_vars = "plex_server_version: {}".format(plex_version)
    app.logger.info("Sending update job request to update to version {}".format(plex_version))
    execution = plex_update_job_template.launch(extra_vars=extra_vars)
    app.logger.info("Job status: {}".format(execution.status))
    return execution.status
