import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/parallel-search-api/scripts/search.py'


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'Search helper must exist')
        spec = importlib.util.spec_from_file_location('search', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_request_and_response(self):
        response = {'search_id': 's1', 'session_id': 'session1', 'results': [], 'warnings': [{'message': 'warning'}]}
        with patch.object(self.module.urllib.request, 'urlopen', return_value=io.BytesIO(json.dumps(response).encode())) as call:
            self.assertEqual(self.module.search({'search_queries': ['python official documentation']}, 'secret'), response)
        request = call.call_args.args[0]
        self.assertEqual(request.full_url, 'https://api.parallel.ai/v1/search')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.get_header('X-api-key'), 'secret')
        self.assertEqual(json.loads(request.data), {'search_queries': ['python official documentation']})

    def test_missing_key_does_not_send(self):
        with patch.object(self.module.urllib.request, 'urlopen') as call:
            with self.assertRaisesRegex(ValueError, 'PARALLEL_API_KEY'):
                self.module.search({'search_queries': ['test']}, '')
            call.assert_not_called()

    def test_http_error_is_actionable_and_does_not_leak_body(self):
        for code in (401, 403, 422, 429, 500):
            error = HTTPError('https://api.parallel.ai/v1/search', code, 'error', {}, io.BytesIO(b'secret'))
            with patch.object(self.module.urllib.request, 'urlopen', side_effect=error) as call:
                with self.assertRaises(RuntimeError) as caught:
                    self.module.search({'search_queries': ['test']}, 'secret')
                self.assertIn(str(code), str(caught.exception))
                self.assertNotIn('secret', str(caught.exception))
                self.assertEqual(call.call_count, 1)

    def test_network_failure(self):
        with patch.object(self.module.urllib.request, 'urlopen', side_effect=URLError('secret')):
            with self.assertRaisesRegex(RuntimeError, 'network'):
                self.module.search({'search_queries': ['test']}, 'secret')

    def test_invalid_json(self):
        with patch.object(self.module.urllib.request, 'urlopen', return_value=io.BytesIO(b'not json')):
            with self.assertRaisesRegex(RuntimeError, 'JSON'):
                self.module.search({'search_queries': ['test']}, 'secret')


if __name__ == '__main__':
    unittest.main()
