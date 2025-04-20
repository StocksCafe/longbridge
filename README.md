## AutoSync

This project is to assist users in pulling data from their longbridge brokerage and sending the data to StocksCafe to sync

## Getting started

1) git clone https://github.com/StocksCafe/longbridge

2) Apply for LongBridge API (https://open.longportapp.com/en/)

3) Install Docker on your computer
For Mac -> https://docs.docker.com/desktop/setup/install/mac-install/
For Windows -> https://docs.docker.com/desktop/setup/install/windows-install/
For Linux -> https://docs.docker.com/desktop/setup/install/linux/ 

4) From command prompt, goto the directory where code is cloned and run "chmod +x autosync.sh"

5) Then run "./autosync.sh"

6) Open browser (preferably Chrome) and goto http://localhost:8000/

7) Enter values for the fields 
https://stocks.cafe/user/sync_api_key -> To get STOCKSCAFE_USER_ID, STOCKSCAFE_LABEL_ID and STOCKSCAFE_SYNC_API_KEY
https://open.longportapp.com/en/account -> To get LONGPORT_APP_KEY, LONGPORT_APP_SECRET and LONGPORT_ACCESS_TOKEN