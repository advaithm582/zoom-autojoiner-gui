import logging
from datetime import datetime
logging.basicConfig(filename='logs/%s.log' % (datetime.now().strftime("%Y%m%d-%H%M%S")), filemode='w', format='[%(asctime)s] [%(name)s:%(levelname)s] [pid:%(process)d, tid:%(thread)d] %(message)s', datefmt='%c', level=logging.INFO)
