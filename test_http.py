import unittest
import time

class MyTestCase(unittest.TestCase):
    def test_something(self):
        import logentries
        import logging
        handler = logentries.LogentriesWHHandler("")
        logging.root.addHandler(handler)
        logging.warning("TEST 1 2 3")
        time.sleep(60)


if __name__ == '__main__':
    unittest.main()
