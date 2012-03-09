"""Tests for the notebook web services."""

import os
import shutil
import sys
from subprocess import Popen, PIPE, STDOUT
import tempfile
from unittest import TestCase

from IPython.core.profiledir import ProfileDir
from zmq.utils import jsonapi

import requests

TMP_TEST_DIR = tempfile.mkdtemp()
HOME_TEST_DIR = os.path.join(TMP_TEST_DIR, "home_test_dir")
IP_TEST_DIR = os.path.join(HOME_TEST_DIR,'.ipython')

PORT = 12345

def setup():
    global process, profiles, baseurl
    os.makedirs(IP_TEST_DIR)
    profiles = []
    baseurl = 'http://127.0.0.1:%d'%PORT
    for i in range(3):
        pname = 'test%d'%i
        pd = ProfileDir.create_profile_dir_by_name(IP_TEST_DIR, pname)
        profiles.append((pname,pd.location))
    args = [
        sys.executable,
        '-c',
        'from IPython.frontend.html.notebook.notebookapp import launch_new_instance; launch_new_instance()',
        '--no-browser',
        '--port=%d'%PORT
    ]
    process = Popen(args,stdout=PIPE,stderr=PIPE,stdin=PIPE,env=os.environ)


class TestClusterManager(TestCase):

    def setUp(self):
        self.url = baseurl+'/clusters'

    def test_profile_list(self):
        r = requests.get(self.url+'/')
        data = jsonapi.loads(r.content)
        expected = []
        for pname, pdir in profiles:
            expected.append({'profile':pname,'status':'stopped','profile_dir':pdir})
        self.assertEquals(data,expected)

    


def teardown():
    shutil.rmtree(TMP_TEST_DIR)
    process.kill()
