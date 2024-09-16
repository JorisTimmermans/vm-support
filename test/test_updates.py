import os.path
import pytest
import shutil
from vm_support.updates import _is_newer_than, _clone_new_repo
import urllib.request
import zipfile

__author__ = "Tonio Fincke (Brockmann Consult GmbH)"

test_data_save_path = '/tmp/data-access-test_data.zip'
if not os.path.exists(test_data_save_path):
    urllib.request.urlretrieve('https://github.com/QCDIS/vm-support/raw/master/test/test_data.zip', test_data_save_path)
    with zipfile.ZipFile(test_data_save_path, 'r') as zip_ref:
        zip_ref.extractall('/tmp')
    zip_ref.close()
base_path = '/tmp/test_data/'


def test_is_newer_than():
    assert _is_newer_than('v0.4', 'v0.3')
    assert not _is_newer_than('v0.4', 'v0.4')
    assert not _is_newer_than('v0.4', 'v0.5')
    assert _is_newer_than('v0.4.1', 'v0.4')
    assert not _is_newer_than('v0.4.1', 'v0.4.1')
    assert not _is_newer_than('v0.4.1', 'v0.4.2')
    assert _is_newer_than('v0.4', 'v0.3.2')
    assert _is_newer_than('v1', 'v0.4.2')
    assert not _is_newer_than('v1.4.2', 'v2')

@pytest.mark.skip
def test_clone_new_repo():
    base_dir = base_path + 'test_dir_clone_repo'
    os.makedirs(base_dir)
    try:
        required_repo = {'name': 'MULTIPLY Inference Engine',
                         'path_on_github': 'https://github.com/multiply-org/inference-engine.git', 'branch': 'master'}
        _clone_new_repo(base_dir, required_repo)
    finally:
        if os.path.exists(base_dir):
            _remove_symlinks_recursively(base_dir)
            shutil.rmtree(base_dir)


def _remove_symlinks_recursively(dir: str):
    files = os.listdir(dir)
    for file in files:
        if os.path.islink(file):
            os.unlink(file)
        if os.path.isdir(file):
            _remove_symlinks_recursively(file)
