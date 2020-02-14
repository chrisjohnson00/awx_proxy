from awx_proxy.models import PlexDownloads


def test_get_latest_version_from_plex():
    """
    Tests the download url to ensure it gives a proper response.
    If this fails, check the `plex_download_url` for valid-ness, it may have changed
    """
    plex = PlexDownloads()
    plex.get_latest_version_from_plex()
    latest_version = plex.get_latest_version()
    assert '1' in latest_version
