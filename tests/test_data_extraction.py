import unittest
from unittest.mock import patch
from unittest.mock import Mock
# Replace the import paths below according to your actual project structure.
from src.etl.data_extraction import make_request, fetch_financial_metrics

# Mock HTML based on the provided table structure
MOCKED_HTML_FINANCIAL_METRICS = '''
<table class="slpEwd">
  <tr class="roXhBd">
    <td class="J9Jhg">
      <div class="rsPbEe">Revenue</div>
    </td>
    <td class="QXDnM">134.38B</td>
  </tr>
</table>
'''

class TestMakeRequest(unittest.TestCase):
    
    @patch('src.etl.data_extraction.requests.get')
    def test_make_request_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = "Success"
        mock_get.return_value = mock_response
        self.assertEqual(make_request('https://www.google.com/finance/quote/AMZN:NASDAQ?hl=en'), "Success")
        
    @patch('src.etl.data_extraction.requests.get')
    def test_make_request_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        self.assertIsNone(make_request('https://www.google.com/finance/quote/AMZN:NASDAQ?hl=en'))

class TestFetchFinancialMetrics(unittest.TestCase):
    
    @patch('src.etl.data_extraction.make_request')
    def test_fetch_financial_metrics(self, mock_make_request):
        mock_make_request.return_value = MOCKED_HTML_FINANCIAL_METRICS
        self.assertEqual(fetch_financial_metrics('AMZN', 'NASDAQ'), {'Revenue': '134.38B'})

if __name__ == '__main__':
    unittest.main()
