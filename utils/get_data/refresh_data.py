import utils.get_data.data_scraping as data_scraping
import os
import time

most_recent_refresh = None

def refresh_data():
    global most_recent_refresh
    if most_recent_refresh and time.time() - most_recent_refresh < 60*60:
        return
    most_recent_refresh = time.time()
    new_op_data = data_scraping.download_op_grants()
    new_op_data = new_op_data.text
    print('latest OP grant: ', new_op_data.split('\n')[1])
    op_data_path = os.path.abspath('./assets/data/openphil_grants.csv')
    with open(op_data_path, 'w') as f:
        f.write(new_op_data)


