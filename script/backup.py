
from datetime import datetime
import logging
import os
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/home/cwakibi/mayanapp/backup.log', level=logging.DEBUG)

initialHour = datetime.now().hour

try:
    while True:
        if initialHour > datetime.now().hour:
            thedatetime = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            first = os.listdir('/home/cwakibi/mayanapp/backup/')
            result = os.system(f"sudo tar -zcvf  /home/cwakibi/mayanapp/backup/backup-{thedatetime}.tar.gz /docker-volumes/mayan-edms/")
            # result = os.system(f"sudo tar -zcvf  /home/cwakibi/mayanapp/backup/backup-{thedatetime}.tar.gz /home/cwakibi/joeldelete")  # Test
            entries = os.listdir('/home/cwakibi/mayanapp/backup/')
            logging.info(result)

            if first and (len(entries) > 1):
                os.system(f"sudo rm /home/cwakibi/mayanapp/backup/{first[0]}")
            initialHour = 1
            time.sleep(60*60*24)

        if not initialHour == 1:
            time.sleep(60*60)
except Exception as e:
    logging.error(str(e))

