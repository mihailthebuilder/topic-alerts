# Facebook Keyword Alerts
A Python script that generates email alerts when specific keywords are mentioned in Facebook group posts. Uses Selenium, Gmail's API and the Firefox browser.

# Table of contents
- [Facebook Keyword Alerts](#facebook-keyword-alerts)
- [Table of contents](#table-of-contents)
- [Requirements](#requirements)
- [How it works](#how-it-works)
- [Selenium](#selenium)
- [Gmail API](#gmail-api)
- [Limitations](#limitations)
- [Features to consider](#features-to-consider)

# Requirements

The script requires a number of items in order to run:

- [Firefox browser](https://www.mozilla.org/firefox/new/) installed on your local machine.
- [geckodriver file](https://github.com/mozilla/geckodriver/releases) downloaded in this folder. The file will enable you to run Firefox using Selenium.
- A [Gmail account](https://gmail.com/).
- A `credentials.json` file in this folder, which contains credentials enabling Gmail API on your gmail account. You need to download this file from [here](https://developers.google.com/gmail/api/quickstart/python) by clicking the `Enable the Gmail API` button.
  
  [gmail api](./demo/gmail_api.png)
  
- An `input.json` file that contains the Facebook group URLs, keywords used for alerts, sender and receiver email addresses.
  
  The file also needs to hold the path to the Firefox profile you wish to use with the browser. You can find it by opening `about:support` in the Firefox browser and looking at the path in the `Profile Directory` row - see [this](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data) for more details.

  This is how the json file should be structured:

```json
{
  "alerts": [
    {
      "url": "https://www.facebook.com/groups/SaaSgrowthhacking/",
      "keywords": ["marketing", "sales"]
    },
    {
      "url": "https://www.facebook.com/groups/DeepNetGroup/",
      "keywords": ["pytorch", "nvidia"]
    }
  ],
  "firefox_profile_path": "/home/jon/.mozilla/firefox/yy6ndmx3.default-release",
  "gmail": {
    "sender": "mihail.automated.alerts@gmail.com",
    "receiver": "mihailmarian12@gmail.com"
  }
}
```

# How it works

# Selenium

# Gmail API

# Limitations

# Features to consider
