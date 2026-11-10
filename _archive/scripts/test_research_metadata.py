import unittest
from research_metadata import compact


class Metadata(unittest.TestCase):
    def test_retains_public_research_and_discards_bulk_playback_data(self):
        source = {'id': 'abc', 'title': 'A title', 'timestamp': 123, 'upload_date': '20261028',
                  'view_count': 42, 'duration': 24, 'thumbnails': [{'url': 'https://example.org/a.jpg'}],
                  'availability': 'public', 'channel_id': 'UC123',
                  'automatic_captions': {'en': ['large'] * 10000},
                  'formats': [{'url': 'https://example.org/temporary-playback'}],
                  'requested_downloads': [{'url': 'https://example.org/temporary-playback'}]}
        result = compact(source)
        self.assertEqual(result['thumbnails'], source['thumbnails'])
        self.assertEqual(result['timestamp'], 123)
        self.assertEqual(result['availability'], 'public')
        self.assertFalse(set(result) & {'automatic_captions', 'formats', 'requested_downloads'})
        self.assertEqual(compact(result), result)
        self.assertGreater(len(str(source)), len(str(result)) * 100)


if __name__ == '__main__':
    unittest.main()
