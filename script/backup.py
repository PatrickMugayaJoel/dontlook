
from datetime import datetime
import logging
import sys
import subprocess
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/home/cwakibi/mayanapp/backup.log', level=logging.DEBUG)

try:
    while true:
        thedatetime = datetime.now().strftime("%m-%d-%Y")
        # python2 => subprocess.run(["ls", "-l"])
        # subprocess.call([f"sudo tar -zcvf  '/home/cwakibi/mayanapp/backup-{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}.tar.gz' /docker-volumes/mayan-edms/"]) 
        result = subprocess.call([f"sudo tar -zcvf  '/home/cwakibi/mayanapp/backup-{thedatetime}.tar.gz' ~/joeldelete/"])  # Test
        logging.info(result)
        time.sleep(20)
except:
    logging.error(sys.exc_info()[0])
