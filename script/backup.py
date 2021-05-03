
from datetime import datetime
import logging
import os
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/home/cwakibi/mayanapp/backup.log', level=logging.DEBUG)

try:
    while True:
        thedatetime = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        # os.system(f"sudo tar -zcvf  '/home/cwakibi/mayanapp/backup-{thedatetime}.tar.gz' /docker-volumes/mayan-edms/") 
        result = os.system(f"sudo tar -zcvf  '/home/cwakibi/mayanapp/backup {thedatetime}.tar.gz' /home/cwakibi/joeldelete")  # Test
        logging.info(result)
        time.sleep(20)
except Exception as e:
    logging.error(str(e))

