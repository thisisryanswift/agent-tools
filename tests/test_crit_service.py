"""Exercise deployed service permissions against a separately launched Crit daemon."""
import configparser
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import uuid

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'scripts'))
from crit_reviews import Registry


@unittest.skipUnless(os.environ.get('CRIT_TEST_SYSTEMD') == '1',
                     'set CRIT_TEST_SYSTEMD=1 with access to the user manager')
class ServicePermissions(unittest.TestCase):
    def test_service_can_verify_a_review_launched_outside_its_sandbox(self):
        binary = os.environ.get('CRIT_TEST_BINARY', str(Path.home() / '.local/bin/crit'))
        # A home fixture matches real daemon placement; PrivateTmp must not hide
        # the fixture and produce a different failure from /proc identity checks.
        state = Path.home() / '.local/state'
        with tempfile.TemporaryDirectory(prefix='crit-service-test-', dir=state) as directory:
            root = Path(directory)
            (root / 'note.md').write_text('# Synthetic service permission test\n')
            (root / '.crit.config.json').write_text('{"disable_stats":true}')
            registry = Registry(root / 'registry', binary)
            with mock.patch.dict(os.environ, CRIT_SHARE_URL='http://127.0.0.1:1'):
                review = registry.start('service-permission-test', str(root), ['note.md'])
            try:
                config = configparser.ConfigParser(interpolation=None)
                config.read(REPO / 'deploy/crit-reviews/crit-review-router.service')
                options = []
                for key in ('NoNewPrivileges', 'PrivateTmp', 'ProtectSystem',
                            'PrivateUsers', 'ProtectProc', 'ProcSubset'):
                    if key in config['Service']:
                        options += ['-p', key + '=' + config['Service'][key]]
                code = (
                    'import sys; sys.path.insert(0,sys.argv[1]); '
                    'from crit_reviews import Registry; '
                    'r=Registry(sys.argv[2],sys.argv[3]); '
                    'print(r.verified(sys.argv[4])["state"])'
                )
                result = subprocess.run(
                    ['systemd-run', '--user', '--wait', '--pipe', '--collect',
                     '--unit=crit-permission-test-' + uuid.uuid4().hex[:12],
                     *options, sys.executable, '-c', code, str(REPO / 'scripts'),
                     str(registry.root), binary, review['id']],
                    capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('active', result.stdout)
            finally:
                registry.stop(review['id'])
                try:
                    os.waitpid(review['generation']['pid'], 0)
                except ChildProcessError:
                    pass


if __name__ == '__main__':
    unittest.main()
