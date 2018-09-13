import datetime
import logging
import sys

logfilename = sys.argv[0].split("/")[-1][:-3]
indexTime = datetime.datetime.now().strftime('%Y%m%d_%H')
logPath = '/Users/magic/PycharmProjects/zywa-spider-xiaociwei/zywa_test_others/logTest'
loggerfilename = logPath + "/{0}_{1}.log".format(logfilename, indexTime)

FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

handler = logging.FileHandler(loggerfilename, mode='a+', encoding="utf-8", delay=False)

# logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%a, %d %b %Y %H:%M:%S', filename=loggerfilename,filemode='w')

logging.basicConfig(level=logging.WARNING, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', handlers=[handler])

logging.info('test info')
logging.warning('test warning')
logging.error('test error')
