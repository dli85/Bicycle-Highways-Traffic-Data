# Traffic Data Scraper

A web scraper to collect information about traffic data. main.py is 
to download from https://scerisecm.boston.gov/ScerIS/CmPublic. Downloads are
stored in a download folder in repository root.

## Requirements

Use pip to install the required libraries

```bash
pip install requirements.txt
```

The chromedriver is included in the driver folder. Chromedriver may need to be 
updated based on your [Chrome version](https://chromedriver.chromium.org/downloads).

Reinstall urllib3 to fix any issues regarding urllib3.poolmanager
