from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
import time

driver = webdriver.Chrome()


driver.get("https://www.linkedin.com/login")
# your email 
username = ""
# your password 
password = ""
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(15)  





search_term = "web developer"
encoded = quote(search_term)

driver.get(f"https://www.linkedin.com/jobs/search/?keywords={encoded}")


time.sleep(10)


number_of_jobs = driver.find_element(By.CLASS_NAME, "jobs-search-results-list__subtitle")
print(number_of_jobs.text)

# getting all cards

job_titles = []
cards = []

job_data = []

scrollable_div = driver.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div[1]/div')

cards_loaded_before = 0


for page in range(2):
    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(3)
        
        cards = driver.find_elements(By.CLASS_NAME,"job-card-container")
        
        
        
        
        current_loaded = len(cards)
        
        if cards_loaded_before == current_loaded:
            break
        
        cards_loaded_before = current_loaded



    for card in cards:
        driver.execute_script("arguments[0].scrollIntoView();", card)

        time.sleep(2)  # Allow right panel to load
        
        
        title = card.find_element(By.CLASS_NAME, "job-card-container__link")
        child = title.find_elements(By.XPATH,"./*")
        location = card.find_element(By.CLASS_NAME,"job-card-container__metadata-wrapper ").text
        job_data.append({
            "title": child[0].text, 
            "location" : location,
            })

    if page < 1:
        try:
            next_button = driver.find_element(By.CLASS_NAME, "jobs-search-pagination__button")
            if next_button.is_enabled():
                next_button.click()
                print("Clicked next page button")
                time.sleep(8) 
                scrollable_div = driver.find_element(By.CLASS_NAME,'//*[@id="main"]/div/div[2]/div[1]/div')
            else:
                print("Next button disabled - no more pages")
                break
        except Exception as e:
            print("Couldn't click next button:", e)
            break



for data in job_data:
    print(data)



driver.quit()
