from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import requests
import random
import json
import time
import sys

print("\t\tmeproBot by Ai-man\n")

URL_LOGIN = "https://mepro.pearson.com/login"
URL_PostActivityLogDetails = "https://mepro.pearson.com/CallToServer.aspx/PostActivityLogDetails"

chrome_options = Options()
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options, keep_alive=True)

driver.get(URL_LOGIN)

def send_answer(request_urls: list):
    if URL_PostActivityLogDetails in request_urls:
        cookie = str(driver.get_cookie("ASP.NET_SessionId")['value'])
        
        cookies = {
            "ASP.NET_SessionId": cookie,
        }

        headers = {
            "Content-Type": "application/json",
            "Cookie": f"ASP.NET_SessionId={cookie}"
        }
        
        post_data = {
            "obj": {
                "ActivityScore": random.randrange(71, 100), 
                "ActivityStatus": "completed",
                "TimeSpent": f"00:{random.randrange(3, 20)}:{random.randrange(0, 59)}"
            }
        }
        
        time.sleep(5)
        
        response = requests.post(URL_PostActivityLogDetails, headers=headers, cookies=cookies, json=post_data)
        print(f"\nstatus code : {response.status_code}")
        print("This Task is done !")
            
def main():
    try:
        while True:
            logs = driver.get_log("performance")
            
            for entry in logs:
                log_msg = json.loads(entry["message"])
                
                if log_msg["message"]["method"] == "Network.requestWillBeSent":
                    request_urls = log_msg["message"]["params"]["request"]["url"]
                    
                    send_answer(request_urls)
                    
    except KeyboardInterrupt:
        driver.quit()
        sys.exit()                   
                                
if __name__ == "__main__":
    main()
