import time,os
from threading import Thread
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from slacker import Slacker
# Authenticate with slacker
slack = Slacker(Slacktoken)
#variables
action_url="https://www.sampleurl.com"
def screenshot(login_url,navi_url,sample):
    password=os.environ["SEL_PASSWORD"] #Saving pass as env variable if possible or u can use access tokens
    email="vigneshkarthy3@gmail.com"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path="/opt/Selenium_Driver/chromedriver.exe",chrome_options=options)
    driver.set_window_size(1920, 1080)
    driver.get(login_url)
    print(driver.title) #title of the page
    user_ele=driver.find_element_by_css_selector("input[name='username']")
    pass_ele=driver.find_element_by_css_selector("input[name='password']")
    time.sleep(1)
    if user_ele.is_enabled()==True and pass_ele.is_enabled()==True:
        user_ele.send_keys(email)
        pass_ele.send_keys(password)
        driver.find_element_by_css_selector("button[type='submit']").click()
        time.sleep(8)
    driver.get(navi_url)
    time.sleep(8)
    driver.execute_script("$('button svg:nth(1)').click()")
    driver.execute_script("$(\"li[data-action='enterMaximizeMode']\").click()") ## get to know the li options of the action to be done
    #driver.switch_to_default_content
    time.sleep(3)
    name=sample+'.png'
    driver.save_screenshot(name)
    print('Screenshot done')
    slack.files.upload(file_=name,
                   channels=['#somechannel'], title=sample)
    print('File uploaded')
    driver.close()

if __name__ == '__main__':
## Multithreading just to instantiate multiple region data screenshot
    Thread(target=screenshot,args=[url,navi_url,'sample1']).start()
    Thread(target=screenshot,args=[url,navi_url,'sample2']).start()
    Thread(target=screenshot,args=[url,navi_url,'sample3']).start()
    Thread(target=screenshot,args=[url,navi_url,'sample4']).start()
    Thread(target=screenshot,args=[url,navi_url,'sample5']).start()
    slack.chat.post_message(channel='#somechannel',text='Please check the screenshots')