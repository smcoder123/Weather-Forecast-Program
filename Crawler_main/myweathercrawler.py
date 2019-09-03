
#weather forecasting program.
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# Taking place as input.
place = input(" Enter the place: ")
print("\n")
print(" Donot close the firefox window. ")
print(" Wait for a moment till the firefox window dissapears. ")

# Create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(15)

# Navigate to the application home page
driver.get("https://weather.com/en-IN/")

# get the search textbox
# get the list of elements which are displayed after the search
# currently on result page using find_elements_by_class_name method
search_field_xpath = "//input[@aria-label='Location Search']"
results_xpath = "//div[div/text()='Search results']/ul/li[1]/a"

try:
    # For search field
    search_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, search_field_xpath))
    )
    search_field.click()
    search_field.send_keys(place)
    
    # For result
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, results_xpath))
    )
    url = result.get_attribute("href")
except:
    print("\n Program terminated, your input location might not be correct or the internet connection might be slow ")
    sys.exit()
finally:
    driver.quit()
   

#creation of the soup.
print("\n Type of weather forecasting -> 'today','hourbyhour','5day','tenday','monthly'")
strr=input('\n Enter the type of weather forecasting else press enter for default execution: ');
if strr=='':
   strr='today'
print("\n Please wait for a moment ")
#URL input and important files extraction.


a,b=url.split('today')
url = a + strr + b

#url="https://weather.com/en-IN/weather/"+"/l/e401db6723f1167cfcd2c3313458cb481dde47ad15c34c2bfb2d31c04654dab5"
rr=requests.get(url)
soup=BeautifulSoup(rr.text,'html.parser')
if strr=='today':  
  for info in soup.find_all('section',class_="today_nowcard-container"):
      for temp in info.find_all('div',class_="today_nowcard-temp"):
          print(f' Current Temp ={temp.text}')  
      for cond in info.find_all('div',class_="today_nowcard-phrase"):
          print(f' Current weather ={cond.text}')
      for feels in info.find_all('span',class_="deg-feels"): 
          print(f' feels like {feels.text}')
      for H in info.find_all('div',class_="today_nowcard-hilo"): 
          print(H.text)

#Program to check the monthly basis.
elif strr=='monthly':   
     date=int(input(' Enter any date of the current month eg 21:  '))
     temp=[]
     for dayCell_opaque in soup.find_all('div',class_="temps"):
                 temp.append(dayCell_opaque.text)
     print(f" the high temp and low temp are respectively: {temp[date-1]}")

#program checking in rest techniques.       
else:
    table=soup.find('table')
    table_rows=table.find_all('tr')
    h=['']
    l = []
    for th in soup.find_all('th'):
        h.append(th.text)
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)
    l.remove([])
    df=pd.DataFrame(data=l,columns=h)
    print(df)    
    
###############END###########################################
    
