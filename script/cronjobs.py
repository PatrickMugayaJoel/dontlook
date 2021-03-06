#   sudo python3 cronjobs.py &> /dev/null &
#   ps aux | grep SimpleHTTPServer/backup.py NOTE: anything with "grep --color=auto" is auto generated
#   sudo kill 111

from datetime import datetime
import logging
import os
import time
import requests

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/home/cwakibi/mayanapp/backup.log', level=logging.DEBUG)

try:
    while True:

        ### backup script
        if datetime.now().hour == 0:
            thedatetime = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            first = os.listdir('/home/cwakibi/mayanapp/backup/')
            result = os.system(f"sudo tar -zcvf  /home/cwakibi/mayanapp/backup/backup-{thedatetime}.tar.gz /docker-volumes/mayan-edms/")
            # result = os.system(f"sudo tar -zcvf  /home/cwakibi/mayanapp/backup/backup-{thedatetime}.tar.gz /home/cwakibi/joeldelete")  # Test
            entries = os.listdir('/home/cwakibi/mayanapp/backup/')
            logging.info(result)

            if first and (len(entries) > 1):
                os.system(f"sudo rm /home/cwakibi/mayanapp/backup/{first[0]}")

        ### reminder mails script
        if (datetime.now().hour == 8) and (datetime.now().weekday() < 5):
            resp = requests.get(f"http://{os.environ.get('MAYAN_APP_HOST')}/api/send/reminders/", auth=(os.environ.get("MAYAN_APP_USER_NAME"), os.environ.get("MAYAN_APP_USER_PASS")))
            logging.info(resp.reason)

        time.sleep(60*60)
except Exception as e:
    logging.error(str(e))

