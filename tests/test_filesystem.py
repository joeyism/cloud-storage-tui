from snapshottest import TestCase

from cloudstoragetui.filesystem import generate_filesystem_from_path

class TestFilesystem(TestCase):

    def test_generate_filesystem_from_path(self):
        files = generate_filesystem_from_path("/User/joey/file")
        self.assertMatchSnapshot(files)
