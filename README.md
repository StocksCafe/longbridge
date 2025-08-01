## AutoSync

This project is to assist users in pulling data from their longbridge brokerage and sending the data to StocksCafe to sync

## First Run

1) Apply for LongBridge API (https://open.longportapp.com/en/)

2) Install Docker on your computer
- For Mac -> https://docs.docker.com/desktop/setup/install/mac-install/
- For Windows -> https://docs.docker.com/desktop/setup/install/windows-install/
- For Linux -> https://docs.docker.com/desktop/setup/install/linux/ 

3) Open command prompt, goto directory that you want for StocksCafe, run "git clone https://github.com/StocksCafe/longbridge"

4) Go into "longbridge" directory (i.e. where code is cloned) and run "chmod +x autosync.sh"

5) Then run "./autosync.sh"

6) Open browser (recommended Chrome) and goto http://localhost:8000/

7) Enter values for the fields 
- https://stocks.cafe/user/sync_api_key -> To get STOCKSCAFE_USER_ID, STOCKSCAFE_LABEL_ID and STOCKSCAFE_SYNC_API_KEY
- https://open.longportapp.com/en/account -> To get LONGPORT_APP_KEY, LONGPORT_APP_SECRET and LONGPORT_ACCESS_TOKEN

8) Click "Update Settings" then click "Sync LongBridge Data"
Note: It will sync both cash transactions (both deposits and withdrawal) and orders (including stocks and options)

9) Goto https://stocks.cafe and see that your longbridge data is now sync into StocksCafe!
    
10) Also, you should run "Sync Cash Balance Dividend" (Choose 'Sync All') on this page (https://stocks.cafe/portfolio/viewcashdetails) to populate dividends

## Subsequent Run

1) Ensure that Docker Desktop is running

2) Open command prompt, goto directory where you previously cloned longbrigde to.

3) Simply run "./autosync.sh" in command prompt

4) Open browser (recommended Chrome) and goto http://localhost:8000/

5) Click on "Sync LongBridge Data"

## Token Expired

1) If you see some "Token Expired" error after clicking the "Sync LongBridge Data"

2) Simply go to this page (https://open.longportapp.com/en/account) and click "Reset Token"

3) Then update LONGPORT_ACCESS_TOKEN and try clicking on "Sync LongBridge Data". It should now work.

## Pull New Updates

1) Go into "longbridge" directory (i.e. where code is cloned)

2) Run "git pull"
