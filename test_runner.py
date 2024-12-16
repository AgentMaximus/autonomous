import unittest

loader = unittest.TestLoader()
start_dir = 'autonomous-repo/dev'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)