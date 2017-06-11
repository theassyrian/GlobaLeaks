import os
import SimpleHTTPServer
import twisted

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from OpenSSL import crypto, SSL

from globaleaks.handlers.admin import https
from globaleaks.models.config import PrivateFactory, NodeFactory
from globaleaks.orm import transact
from globaleaks.rest import errors
from globaleaks.settings import GLSettings

from globaleaks.tests import helpers
from globaleaks.tests.utils import test_tls


@transact
def set_dh_params(store, dh_params):
    PrivateFactory(store).set_val('https_dh_params', dh_params)


class TestFileHandler(helpers.TestHandler):
    _handler = https.FileHandler

    @inlineCallbacks
    def setUp(self):
        yield super(TestFileHandler, self).setUp()

        self.valid_setup = test_tls.get_valid_setup()
        yield set_dh_params(self.valid_setup['dh_params'])

    @inlineCallbacks
    def is_set(self, name, is_set):
        handler = self.request(role='admin', handler_cls=https.ConfigHandler)

        yield handler.get()
        resp = self.responses[-1]

        self.assertEqual(resp['files'][name]['set'], is_set)

    @transact
    def set_enabled(self, store):
        PrivateFactory(store).set_val('https_enabled', True)
        GLSettings.memory_copy.private.https_enabled = True

    @inlineCallbacks
    def test_priv_key_file(self):
        n = 'priv_key'

        yield self.is_set(n, False)

        # Try to upload an invalid key
        bad_key = 'donk donk donk donk donk donk'
        handler = self.request({'name': 'priv_key', 'content': bad_key}, role='admin')
        yield self.assertFailure(handler.post(n), errors.ValidationError)

        # Upload a valid key
        good_key = self.valid_setup['key']
        handler = self.request({'name': 'priv_key', 'content': good_key}, role='admin')
        yield handler.post(n)
        yield self.is_set(n, True)

        was_generated = self.responses[-1]['files']['priv_key']['gen']
        self.assertFalse(was_generated)

        handler = self.request(role='admin')
        yield self.assertFailure(handler.get(n), errors.MethodNotImplemented)

        # Test key generation
        yield handler.put(n)
        yield self.is_set(n, True)

        was_generated = self.responses[-1]['files']['priv_key']['gen']
        self.assertTrue(was_generated)

        # Try delete actions
        yield handler.delete(n)
        yield self.is_set(n, False)

    @inlineCallbacks
    def test_cert_file(self):
        n = 'cert'

        yield self.is_set(n, False)
        yield https.PrivKeyFileRes.create_file(self.valid_setup['key'])

        # Test bad cert
        body = {'name': 'cert', 'content': 'bonk bonk bonk'}
        handler = self.request(body, role='admin')
        yield self.assertFailure(handler.post(n), errors.ValidationError)

        # Upload a valid cert
        body = {'name': 'cert', 'content': self.valid_setup[n]}
        handler = self.request(body, role='admin')
        yield handler.post(n)
        yield self.is_set(n, True)

        handler = self.request(role='admin')
        yield handler.get(n)
        content = self.responses[-1]
        self.assertEqual(content, self.valid_setup[n])

        # Finally delete the cert
        yield handler.delete(n)
        yield self.is_set(n, False)

    @inlineCallbacks
    def test_chain_file(self):
        n = 'chain'

        yield self.is_set(n, False)
        yield https.PrivKeyFileRes.create_file(self.valid_setup['key'])
        yield https.CertFileRes.create_file(self.valid_setup['cert'])

        body = {'name': 'chain', 'content': self.valid_setup[n]}
        handler = self.request(body, role='admin')

        yield handler.post(n)
        yield self.is_set(n, True)

        handler = self.request(role='admin')
        yield handler.get(n)
        content = self.responses[-1]
        self.assertEqual(content, self.valid_setup[n])

        yield handler.delete(n)
        yield self.is_set(n, False)

    @inlineCallbacks
    def test_file_res_disabled(self):
        yield self.set_enabled()

        handler = self.request(role='admin')
        for n in ['priv_key', 'cert', 'chain', 'csr']:
            self.assertRaises(errors.FailedSanityCheck, handler.delete, n)
            self.assertRaises(errors.FailedSanityCheck, handler.put, n)
            handler = self.request({'name': n, 'content':''}, role='admin')
            self.assertRaises(errors.FailedSanityCheck, handler.post, n)
            self.assertRaises(errors.FailedSanityCheck, handler.get, n)


class TestConfigHandler(helpers.TestHandler):
    _handler = https.ConfigHandler

    @inlineCallbacks
    def test_all_methods(self):
        valid_setup = test_tls.get_valid_setup()

        yield set_dh_params(valid_setup['dh_params'])
        yield https.PrivKeyFileRes.create_file(valid_setup['key'])
        yield https.CertFileRes.create_file(valid_setup['cert'])
        yield https.ChainFileRes.create_file(valid_setup['chain'])

        handler = self.request(role='admin')

        yield handler.get()
        self.assertTrue(len(self.responses[-1]['status']['msg']) > 0)

        # Config is ready to go. So launch the subprocesses.
        yield handler.post()
        yield handler.get()
        self.assertTrue(self.responses[-1]['enabled'])

        self.test_reactor.pump([50])

        # TODO improve resilience of shutdown. The child processes will complain
        # loudly as they die.
        yield handler.put()
        yield handler.get()
        self.assertFalse(self.responses[-1]['enabled'])


class TestCSRHandler(helpers.TestHandler):
    _handler = https.CSRFileHandler

    @inlineCallbacks
    def test_post(self):
        n = 'csr'

        valid_setup = test_tls.get_valid_setup()
        yield set_dh_params(valid_setup['dh_params'])
        yield https.PrivKeyFileRes.create_file(valid_setup['key'])

        d = {
           'commonname': 'notreal.ns.com',
           'country': 'it',
           'province': 'regione',
           'city': 'citta',
           'company': 'azienda',
           'department': 'reparto',
           'email': 'indrizzio@email',
        }

        body = {'name': 'csr', 'content': d}
        handler = self.request(body, role='admin')
        yield handler.post(n)

        yield handler.get(n)

        csr_pem = self.responses[-1]

        pem_csr = crypto.load_certificate_request(SSL.FILETYPE_PEM, csr_pem)

        comps = pem_csr.get_subject().get_components()
        self.assertIn(('CN', 'notreal.ns.com'), comps)
        self.assertIn(('C', 'IT'), comps)
        self.assertIn(('L', 'citta'), comps)


from globaleaks.utils.lets_enc import ChallTok


class TestAcmeHandler(helpers.TestHandler):
    _handler = https.AcmeHandler

    @inlineCallbacks
    def test_post(self):
        hostname = 'gl.dl.localhost.com'
        GLSettings.memory_copy.hostname = hostname
        valid_setup = test_tls.get_valid_setup()
        yield https.PrivKeyFileRes.create_file(valid_setup['key'])

        handler = self.request(role='admin')
        yield handler.post()

        resp = self.responses[0]

        current_le_tos = 'https://letsencrypt.org/documents/LE-SA-v1.1.1-August-1-2016.pdf'
        self.assertEqual(resp['terms_of_service'], current_le_tos)

    @inlineCallbacks
    def test_put(self):
        valid_setup = test_tls.get_valid_setup()
        yield https.AcmeAccntKeyRes.create_file()
        yield https.AcmeAccntKeyRes.save_accnt_uri('TODO-keep-test-data-around')
        yield https.PrivKeyFileRes.create_file(valid_setup['key'])
        hostname = 'gl.dl.localhost.com'
        GLSettings.memory_copy.hostname = hostname

        d = {
           'commonname': hostname,
           'country': 'it',
           'province': 'regione',
           'city': 'citta',
           'company': 'azienda',
           'department': 'reparto',
           'email': 'indrizzio@email',
        }
        body = {'name': 'xxx', 'content': d}

        handler = self.request(body, role='admin')
        yield handler.put()


class TestAcmeChallResolver(helpers.TestHandler):
    _handler = https.AcmeChallResolver

    @inlineCallbacks
    def test_get(self):
        # tmp_chall_dict pollutes scope
        from globaleaks.handlers.admin.https import tmp_chall_dict
        tok = 'yT-RDI9dU7dJPxaTYOgY_YnYYByT4CVAVCC7W3zUDIw'
        v = '{}.5vh2ZRCJGmNUKEEBn-SN6esbMnSl1w8ZT0LDUwexTAM'.format(tok)
        ct = ChallTok(v)

        tmp_chall_dict.set(tok, ct)

        handler = self.request(role='admin')
        resp = yield handler.get(tok)

        self.assertEqual(self.responses[0], v)

class TestAdminTestHostnameHandler(helpers.TestHandler):
    _handler = https.AdminTestHostnameHandler

    @inlineCallbacks
    def setUp(self):
        yield super(TestAdminTestHostnameHandler, self).setUp()
        self.tmp_hn = GLSettings.memory_copy.hostname
        GLSettings.memory_copy.hostname = 'localhost:43434'

    @inlineCallbacks
    def test_post(self):
        handler = self.request(role='admin')

        # The first request must fail to the non-existent resource
        yield self.assertFailure(handler.post(), errors.ExternalResourceError)

        # Add a file to the tmp dir
        with open('./robots.txt', 'w') as f:
            f.write("User-agent: *\n" +
                    "Allow: /\n"+
                    "Sitemap: http://localhost/sitemap.xml")

        # Start the HTTP server proxy requests will be forwarded to.
        self.pp = helpers.SimpleServerPP()
        yield reactor.spawnProcess(self.pp, 'python', args=['python', '-m', 'SimpleHTTPServer', '43434'], usePTY=True)

        yield self.pp.start_defer

        yield handler.post()

        # TODO the sub proc startup is dying in strange ways
        # print(dir(self.pp), dir(self.pp.transport))
        os.kill(self.pp.transport.pid)

    @inlineCallbacks
    def tearDown(self):
        yield super(TestAdminTestHostnameHandler, self).tearDown()
        self.tmp_hn = GLSettings.memory_copy.hostname
        GLSettings.memory_copy.hostname = 'localhost'
