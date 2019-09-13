def create_ff_profile(path):
    from selenium import webdriver
    fp =webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir",path)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk",'text/plain')
    fp.update_preferences()
    return fp.path