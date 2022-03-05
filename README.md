# ETORO BOT

Automate posting your content on Etoro.com


# KNOWN BUGS
Posts with gif as the image file fails sometimes.

In a known captured case, Etoro Website popped up an alert that prevents the submit button from getting clicked.

Content: A good quote to remember $Tesla
Picture Used: media/test-images/failedpost_image.gif

### Reported Error Info
Failed to Upload for Unknown reason, Title: eToro, 

Cookies: [
    {'domain': 'www.etoro.com', 'expiry': 1646225463, 'httpOnly': True, 'name': '__cflb', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '02e4PVHN79Wo1jpTKkB1Xf7RERbz5QPGeRXryKoixQjeuMAGC42BuNVisTsJf41mYk7fxVpP9pRJHRzhkqMeu1JtV5q4rPp3gec97JFvjcLFict8buovkaVF4QWUs3sP7GU3F3kEgCEfT896ySsWLSyXcZfktJH7CDTer1bZrUXbaiCWGK44pBMnfVp9wkdKZbGCCuAKcNf41qvXtBpwfzV6k'},

    {'domain': '.etoro.com', 'expiry': 1646747468, 'httpOnly': False, 'name': 'intercom-session-x8o64ufr', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'SzhlMmQvUWxQZitWM3lncng2b0hGWVpJK0pUM2pnU0RmS2ZLSmwyc3JqMWpTeEoyUVBzQ09nTE1xNER2bEh6Yy0tbTkvanVZdjhHdjB2dVV1TjI2Y1F3dz09--fff784c8e197f7131583324c2e71cafefb31fa65'},

    {'domain': 'www.etoro.com', 'expiry': 4107592261, 'httpOnly': False, 'name': 'etoroHPRedirect', 'path': '/', 'secure': False, 'value': '1'},
    {'domain': 'www.etoro.com', 'httpOnly': False, 'name': 'eToroLocale', 'path': '/', 'secure': False, 'value': 'en-gb'},
    {'domain': '.etoro.com', 'expiry': 1709214620, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.299879743.1646142620'},
    {'domain': '.etoro.com', 'httpOnly': True, 'name': '__cfruid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'f2ffa7e25fa7a3cc450681489fc0c3cc42ea1f64-1646142661'},

    {'domain': '.etoro.com', 'expiry': 1646144414, 'httpOnly': True, 'name': '__cf_bm', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'O2SoN7N2mCvPoqWorMwr_tMBV.aBsoOvHNclPzFlJLk-1646142614-0-AcoSA+/21K+gJj0nQ+m/SU3CMDmbmz9LsRz0b8ui4HWDtDAmQdvP0UkEfwg9k5supdLCbPfj3Jq59rAX5IE0ACjtkZJO1P7xNhle+wy1ZQwxCloZK3DlVbkrZ+r3xuVglzCB+2ex3bC+idBlVJxLAmWDFZCVBxZU/gFBoLZv5APQQ0559Azobv4Q6ChioYcuGA=='},

    {'domain': '.www.etoro.com', 'expiry': 253402257600, 'httpOnly': False, 'name': 'G_ENABLED_IDPS', 'path': '/', 'secure': False, 'value': 'google'},

    {'domain': '.etoro.com', 'expiry': 1646229020, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.1229411596.1646142620'},

    {'domain': '.etoro.com', 'expiry': 1647352214, 'httpOnly': False, 'name': 'TMIS2', 'path': '/', 'secure': False, 'value': '9a74f2a102375b6ba855cb9f58ddc75d0220a7fb2ff2f27e87e26676563d568c2940998ff9040b6befa1699466f5b09986ce3b79a71eaa764038686ab5b59d9af2ec06e743fbda02da7a60805e8e84e54ed03b66c94c4a7273c637e320713c28016eac86a86dc6883911c3166ac574f8f1c03866afc81b86597e2624080b93'},

    {'domain': 'www.etoro.com', 'httpOnly': False, 'name': 'TS01047baf', 'path': '/', 'secure': False, 'value': '01d53e5818b2aa5bf5fc04a643a6aa4464279c8e14f7ddaf349b26fb7411b123cf3c591de4afeff64e19ac54f68e01d7d535d11928'}

],

Exception: Traceback (most recent call last):
      File "/home/ubuntu/etbot/autopost/tasks.py", line 166, in upload_post
        write_post_wrapper.find_element_by_class_name('write-post-button').click()
      File "/home/ubuntu/etbot/.venv/lib/python3.8/site-packages/selenium/webdriver/remote/webelement.py", line 81, in click
        self._execute(Command.CLICK_ELEMENT)
      File "/home/ubuntu/etbot/.venv/lib/python3.8/site-packages/selenium/webdriver/remote/webelement.py", line 710, in _execute
        return self._parent.execute(command, params)
      File "/home/ubuntu/etbot/.venv/lib/python3.8/site-packages/selenium/webdriver/remote/webdriver.py", line 424, in execute
        self.error_handler.check_response(response)
      File "/home/ubuntu/etbot/.venv/lib/python3.8/site-packages/selenium/webdriver/remote/errorhandler.py", line 247, in check_response
        raise exception_class(message, screen, stacktrace)
    selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <button _ngcontent-rsn-c71="" automation-id="write-post-popup-btn-post" class="write-post-button">...</button> is not clickable at point (751, 421). Other element would receive the click: <div _ngcontent-rsn-c62="" automation-id="auto-complete-search-result" class="auto-complete-search-result pointer active ng-star-inserted" id="1111">...</div>
      (Session info: chrome=93.0.4577.82)
