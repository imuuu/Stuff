import time
from selenium import webdriver


timeToload=1

#login settings
print("Give your username")
username=input("Username: ")
print("Give your password")
password=input("Password:")


x="."
for i in range(50):
    
    print(x)
    x=x+"."
    time.sleep(0.05)
x="."

try:
    timeToload=int(input("How fast your internet is 1-10 (1 is fastest and 10 is lowest): "))
except:
    timeToload=11
if timeToload >=1 and timeToload<=10:
    print("Your internet value has been added...")
else:
    print("Internet value has been but to 1")
    timeToload=1
for i in range(50):
    
    print(x)
    x=x+"."
    time.sleep(0.01)
x="."
print("Launching webdriver Chrome...")
browser=webdriver.Chrome()
sitee="https://www.verkkokauppa.com/fi/etusivu"
print("Going to site",sitee)
browser.get(sitee)


#go to login
elem = browser.find_element_by_css_selector('#app > div > div > header > div > nav > a.navigation-icons__link.navigation-icons__link--account.navigation-icons__link--logged-out > span')
elem.click()

time.sleep(4)

#give username
elem = browser.find_element_by_css_selector('#login-form-email')
elem.click()
elem.send_keys(username)

#give pass
elem = browser.find_element_by_css_selector('#login-form-password')
elem.click()
elem.send_keys(password)

#log in
elem = browser.find_element_by_css_selector('#app > div > div > div > div > div > div:nth-child(1) > div:nth-child(1) > form > fieldset.auth-form__fieldset.auth-form > button')
elem.click()

time.sleep(4)

#go to product website https://www.verkkokauppa.com/fi/product/39787/hbmdh/Acer-Iconia-B3-A30-10-1-16-Gt-Wi-Fi-Android-6-0-tablet-valko
orderReady=0
attempt=0

browser.get('https://www.verkkokauppa.com/fi/product/39787/hbmdh/Acer-Iconia-B3-A30-10-1-16-Gt-Wi-Fi-Android-6-0-tablet-valko')

while orderReady==0:
    time.sleep(timeToload)
    
    elem=browser.find_element_by_css_selector('#app > div > div > div > div > section > aside > div.main-view__info > section.product-basic-details > div.add-to-cart > div > button')
    elem.click()
    
    time.sleep(timeToload)
    
    
    
    try:
        elem2=browser.find_element_by_css_selector('#app > div > div > div.cart-dropdown-container.cart-dropdown-container-loaded > div.cart-dropdown-submit > button.vk-button.vk-button--full-width.vk-button--primary.vk-button--large')
        print("ORDER HAS BEEN ADDED")
        orderReady=1
        
    except:
        print(str(attempt)+"."+" ORDER HASN'T ADDED")
        orderReady=0
        attempt+=1
    
        browser.refresh()
if orderReady==1:
    elem2.click()
    print("Now you are ready to buy it!")
    print("DO NOT CLOSE THIS BLACK Window, If you do.. it will close web browser too..")
