from pathlib import Path

from girder import plugin


class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'VolView DICOM-RT'

    def load(self, info):
        plugin.registerPluginStaticContent(
            plugin='girder_volview_dicomrt',
            css=[],
            js=['/girder-plugin-volview-dicomrt.umd.cjs'],
            staticDir=Path(__file__).parent / 'web_client' / 'dist',
            tree=info['serverRoot'],
        )
