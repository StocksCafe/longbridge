## AutoSync

This project is to assist users in pulling data from their longbridge brokerage and sending the data to StocksCafe to sync

## Getting started

1) Apply for LongBridge API (https://open.longportapp.com/en/)
https://stocks.cafe/user/sync_api_key -> To get STOCKSCAFE_USER_ID, STOCKSCAFE_LABEL_ID and STOCKSCAFE_SYNC_API_KEY
https://open.longportapp.com/en/account -> To get LONGPORT_APP_KEY, LONGPORT_APP_SECRET and LONGPORT_ACCESS_TOKEN

2) Install Docker
For Mac -> https://docs.docker.com/desktop/setup/install/mac-install/
For Windows -> https://docs.docker.com/desktop/setup/install/windows-install/
For Linux -> https://docs.docker.com/desktop/setup/install/linux/ 

3) chmod +x autosync.sh

4) ./autosync.sh

5) Open browser (preferably Chrome) and goto http://localhost:8000/

## Docker Commands

- [Build] docker build -t autosync -f Dockerfile .
- [Run] docker run -d --env-file .env -v ./.env:/app/.env --name autosync -p 8000:8000 autosync
- [Remove] docker rm -f autosync
- [Logs] docker logs -ft autosync
- [Execute] docker exec -it autosync /bin/bash