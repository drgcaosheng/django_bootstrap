import os
import hello
import unittest
import tempfile


class HelloTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd,hello.app.config['DATABASE'] = tempfile.mkstemp()
        hello.app.config['TESTING'] = True
        self.app = hello.app.test_client()
        hello.init_db()

    def testDown(self):
        os.close(self.db_fd)
        os.unlink(hello.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    def login(self,username,password):
        return self.app.post('/login',data=dict(
            username=username,
            password=password
        ),follow_redirects=True)

    def logout(self):
        return self.app.get('/logout',follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin','default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin','defauleaa')
        assert 'Invalid password' in rv.data

    def test_message(self):
        self.login('admin', 'default')
        rv = self.app.post('/add',data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ),follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()
