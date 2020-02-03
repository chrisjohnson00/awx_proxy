from flask import Flask
from towerlib import Tower
from awx_proxy.models import PlexDownloads
import logging
import sys

app = Flask(__name__)
app.config.from_pyfile('instance/config.py', silent=False)
"""Configure loggers."""
handler = logging.StreamHandler(sys.stdout)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(handler)


@app.route('/')
def hello():
    return "Welcome the AWX Proxy!"


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
    app.logger.info("Job status: {}").format(execution.status)
    return execution.status
