from flask import Flask
from towerlib import Tower
from awx_proxy.models import PlexDownloads

app = Flask(__name__)
app.config.from_pyfile('instance/config.py', silent=False)


@app.route('/')
def hello():
    return "Welcome the AWX Proxy!"


@app.route('/upgrade_plex', methods=['GET', 'POST'])
def upgrade_plex():
    tower = Tower(app.config.get('TOWER_HOST'), app.config.get('TOWER_USER'), app.config.get('TOWER_PASSWORD'))
    plex_update_job_template = tower.get_job_template_by_name("Plex Update")
    plex_download = PlexDownloads()
    plex_download.get_latest_version_from_plex()
    plex_version = plex_download.get_latest_version()
    extra_vars = "plex_server_version: {}".format(plex_version)
    execution = plex_update_job_template.launch(extra_vars=extra_vars)
    return execution.status
