import pytest

from girder.plugin import loadedPlugins


@pytest.mark.plugin('girder_volview_dicomrt')
def test_import(server):
    assert 'girder_volview_dicomrt' in loadedPlugins()
