from . import BaseTestClass


class EndpointClasesTest(BaseTestClass):

    def test_get_api(self):
        res = self.client.get('/api/class?page=1')
        self.assertEqual(200, res.status_code)
        assert b'image' in res.data
        assert b'page' in res.data
        assert b'text' in res.data
        assert b'total' in res.data
        assert b'type' in res.data
