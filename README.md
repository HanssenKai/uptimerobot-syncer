# Uptimerobot-syncer
Simple python app to sync a yaml file with endpoints you wish to monitor to uptimerobot.  

Ensure `API_KEY` is part of env and run `update-monitors.py`.  
There are no api rate limiting safegueards, run again after a minute or so 
if you add/update/delete a large number of endpoints.

Can easily be integrated into a CI pipeline

