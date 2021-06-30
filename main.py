from app import runner
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument('use_saved', help='use saved version of the data')
# parser.add_argument('use_processed', help='use saved PROCESSED version of the data')
parser.add_argument('--skip_indexing', default=False, help='use data already stored in algolia')

args = parser.parse_args()

if 'skip_indexing' in args:
    skip_indexing = args.skip_indexing
else:
    skip_indexing = False

runner.run(skip_indexing)
