from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getAllCourseURLs(path=None):
    if path==None:
        return set()

    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs

    chrome_prefs["profile.default_content_settings"] = {"popups": 1}
    driver = webdriver.Chrome('/Users/sanyamgupta/PycharmProjects/Web-Scraping/chromedriver', chrome_options=option)
    driver.get(path)

    elem = driver.find_element_by_id('load-more-button')
    MAX_PAGE_LOADS = 10
    numPageLoads = 0
    while (numPageLoads<MAX_PAGE_LOADS and elem.is_displayed()): #keep on doing till either load more button is not inactivated or End Of Results is reached
        closeButtons = driver.find_elements_by_class_name("close")
        for closeB in closeButtons:
            if closeB.is_displayed():
                closeB.click()
        try:
            elem.click()
            numPageLoads = numPageLoads+1
        except:
            pass #if we are in a situation where the page is not loaded completelu and thus the click fails - retry
        #todo after opening page sometime it opens a popup which doesn't have the below button and thus the while condition fails
        elem = driver.find_element_by_id('load-more-button')

    courses_elems = driver.find_elements_by_class_name('resultlist-unit')
    print('Courses Lenght: '+ str(len(courses_elems)))
    urlSet = set()
    for course in courses_elems:
        # <li class="resultlist-unit" data-unittourl="/course/1444/edx/programming-in-scratch-harveymudd">\n
        div_html_str = course.get_attribute('outerHTML')
        length = len(div_html_str)
        start = div_html_str.find(r"/course", 0, length)
        end = div_html_str.find('">\n', 0, length)
        if start >= 0 and end >= 0:
            url = div_html_str[start: end]
            urlSet.add(url)
        else:
            print("start: " + start)
            print("end: " + end)

    driver.close()
    return urlSet

print(len(getAllCourseURLs('https://www.coursebuffet.com/sub/computer-science')))