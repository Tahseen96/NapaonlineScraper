import csv
from time import sleep
from humanBehavior import *
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


# creating class for napaonline scraper
class NapaOnlineScraper:
    # Initial functions to be fired when instance of this class is created
    def __init__(self):
        
        # website url from where data has to be scraped
        self.url = "https://www.napaonline.com/"

        # launching chrome instance
        self.driver = self.createChromeInstance()

        # all us states to search
        self.usStates = ["labama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
                         "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

        # all center types
        self.centerTypes = ["ACTSC", "ACMEC"]
        
        # scraped data storage
        self.centersData = []

    # function to launch chrome browser
    @staticmethod
    def createChromeInstance():
        driver = uc.Chrome(service=ChromeService(
            ChromeDriverManager().install()))
        return driver

    # function to scrape data from
    def scrapeCenters(self):
        # XPATHS
        searchBarXpath = "//input[@id='geo-inputText']"
        findAutocareCentersXpath = "//button[text()='Find an Autocare Center']"
        searchCentersInputXpath = "//input[@id='autocare-search-input']"
        searchCentersInputId = "autocare-search-input"
        searchCentersButtonXpath = "//a[@id='autocare-search-button']"
        selectCentersTypeXpath = "//select[@id='autocare-type-select']"
        seeMoreButtonXpath = "//a[@id='see_more' and @style='display: block;']"
        allCentersElementXpath = "//div[@class='store-item']"
        centerElementXpath = "(//div[@class='store-item'])[{}]"
        noCenterFoundXpath = "//div[text()='There are no results. Try again.']"
        centerTitleXpath = "//a[@class='store-item-title']"
        centerAddressXpath = "//div[@class='store-item-address']"
        phoneNumberXpath = "//div[@class='store-item-address']/following-sibling::div[1]"
        memberIdXpath = "//div[@class='store-item-address']/following-sibling::div[2]"

        # loading website in the launched browser
        self.driver.get(self.url)

        # waiting for website to load completely
        waitForElement(self.driver, searchBarXpath, 30)

        # scrolling to end of the page using javascript
        self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)")

        # clicking on find autocare centers button
        humanClick(self.driver, findAutocareCentersXpath)

        # iterating over all center types to search for each type
        for centerType in self.centerTypes:

            # selecting center type from the center types dropdown
            selectOption(self.driver, selectCentersTypeXpath, centerType)

            # iterating over all us states to search centers according the states
            for state in self.usStates:

                # clearing search field
                clearSearchField(self.driver, searchCentersInputId)

                # typing state in the city search field
                humanTyper(self.driver, searchCentersInputXpath, state)

                # searching for the centers by clicking on the search button
                humanClick(self.driver, searchCentersButtonXpath)

                # waiting for queried data to load
                randomWait(5, 7)

                while True:
                    try:
                        # clicking on see more button to show all centers in the specific state
                        humanClick(self.driver, seeMoreButtonXpath)
                        randomWait(3, 5)
                    except:
                        # break the loop when there is no see more button available
                        break
                    
                try:
                    # checking if there is no center available in the state, don't go further and move to next iteration
                    waitForElement(self.driver,noCenterFoundXpath,5)
                    continue
                except: ()
                
                try:
                    # iterating all over the queried results
                    allCenters = getElements(self.driver,allCentersElementXpath)
                    for counter in range(1,len(allCenters) + 1):
                        try:
                            # extracting title from the center element
                            centerTitle = self.driver.find_element(By.XPATH,centerElementXpath.format(counter) + centerTitleXpath).text.replace("\n", " ")
                            # extracting address from the center element
                            centerAddress = self.driver.find_element(By.XPATH,centerElementXpath.format(counter) + centerAddressXpath).text.replace("\n", " ")
                            # extracting phone number from the center element
                            centerPhoneNumber = self.driver.find_element(By.XPATH,centerElementXpath.format(counter) + phoneNumberXpath).text
                            # extracting member id from the center element
                            centerMemberId = self.driver.find_element(By.XPATH,centerElementXpath.format(counter) + memberIdXpath).text
                            # the state used for the queried search results
                            centerState = state
                            
                            # storing data into the list
                            self.centersData.append([centerTitle,centerAddress,centerPhoneNumber,centerMemberId,centerState])
                            self.storeScrapedDataIntoCsv()
                        except Exception as e:
                            print(e)
                except: 
                    # if service is down restart the website
                    self.driver.get(self.url)
                    
                    # waiting for website to load completely
                    waitForElement(self.driver, searchBarXpath, 30)

                    # scrolling to end of the page using javascript
                    self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

                    randomWait(2,3)
                    
                    # clicking on find autocare centers button
                    humanClick(self.driver, findAutocareCentersXpath)
                    
                    # waiting for queried data to load
                    randomWait(5, 7)
                    
                    # selecting center type from the center types dropdown
                    selectOption(self.driver, selectCentersTypeXpath, centerType)
                    
    
    def storeScrapedDataIntoCsv(self):
        with open('centers_data.csv', mode='w') as csv_file:
            data_writer = csv.writer(csv_file, delimiter=',')
            data_writer.writerow(["Center Title","Center Address","Center Phone Number","Center Member Id","Center State"])
            for item in self.centersData:
                data_writer.writerow(item)
                    

if __name__ == "__main__":
    napaOnlineScraper = NapaOnlineScraper()
    napaOnlineScraper.scrapeCenters()
    sleep(1000)
