from selenium import webdriver

from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
opts = Options()
opts.headless = True
assert opts.headless
driver = webdriver.Firefox(options=opts, executable_path=r'restapi/geckodriver.exe')
driver.maximize_window()



def proba(string):
    return string

def get_event_links_by_category(city, category):
    link1 = "https://allevents.in/" + city + "/" + category
    print(link1)
    driver.get(link1)

    events = driver.find_elements_by_xpath("//li[@class='item event-item  box-link']")
    print("dolzina events ", len(events))
    i = 0
    for event in events:
        print(" --- ", i)
        i += 1

        #print(event.text)
        #print(event.get_attribute("data-id"))
        print(event.get_attribute("data-link"))
        #print(event.get_attribute("data-name"))


#get_event_links_by_category("ljubljana", "entertainment")

def get_event_info(event):
    driver.get(event)
    driver.implicitly_wait(2)
    try:
        description = driver.find_element_by_xpath("//div[@id='event_description']")
        description = description.text
    except NoSuchElementException:
        description = ""
        #would it be better to have description = "No description available for this event" ?
    #print(description.text)
    try:
        time = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/span/span")
        #print(time.text)
        time = time.text
    except NoSuchElementException:
        #print("no time for this event")
        time = ""

    #print(time)
    try:
        title = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div[3]/div[1]/div[1]/span[1]")
       # print(title.text)
        title = title.text
    except NoSuchElementException:
        title = ""
        #print("missing title")
    try:
        location = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div[3]/div[2]/div[1]/div[4]/span/p/span[1]")
        #print(location.text)
        location = location.text
    except NoSuchElementException:
        location = ""
        #print("no location")


        #Error da se sredi not json serializable
        #description="bla bla"

    return {"Title":str(title), "Time": str(time), "Location": str(location), "Description": str(description)}
    #return [title, time, location, description]

#link = "https://allevents.in/ljubljana/pietro-mascagni-ruggiero-leoncavallo-cavalleria-rusticana-gluma%C4%8Ci/200020424472619"
#get_event_info(link)

def get_events_info(city, category):
    city_url = "https://allevents.in/" + city + "/" + category
    driver.get(city_url)
    events_data = []
    events = driver.find_elements_by_xpath("//li[@class='item event-item  box-link']")
    if len(events)==0:
        return "Nisto"
    #print("Number of events ", len(events))
    event_links = []
    for event in events:
        # get [title, time, location, description]
        #print(event)
        try:
            event_url = event.get_attribute("data-link")
            event_links.append(event_url)
        except:
            continue



    for event_url in event_links:
        #events_data.append(get_event_info(event_url))

        #DODADENO ZA AI
        prov=get_event_info(event_url)
        if prov["Title"]!="" and prov["Time"]!="" and prov["Location"]!="":
            return(prov)
            break
    return "Nisto"


#get_events_info("ljubljana", "arts")

# TO DO
# Fix StaleElement exceptions

#get_event_info("https://allevents.in/ljubljana/ski-opening-2020-bad-kleinkirchheim/200020150024449")

#add_to_cal = driver.find_element_by_xpath("//div[@class='wdiv location-box hidden-phone']")
# this line above prints the entire datetime location section and has extra lines
# can be used if the get info function doesn't work