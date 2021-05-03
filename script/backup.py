
from datetime import datetime
import logging
import os
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/home/cwakibi/mayanapp/backup.log', level=logging.DEBUG)

try:
    while True:
        thedatetime = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        # os.system(f"sudo tar -zcvf  /home/cwakibi/mayanapp/backup/backup-{thedatetime}.tar.gz /docker-volumes/mayan-edms/")
        first = os.listdir('/home/cwakibi/mayanapp/backup/')
        result = os.system(f"sudo tar -zcvf  /home/cwakibi/mayanapp/backup/backup-{thedatetime}.tar.gz /home/cwakibi/joeldelete")  # Test
        entries = os.listdir('/home/cwakibi/mayanapp/backup/')
        logging.info(result)

        if first and (entries > 1):
            os.system(f"sudo rm /home/cwakibi/mayanapp/backup/{first[0]}")

        time.sleep(30)
except Exception as e:
    logging.error(str(e))

