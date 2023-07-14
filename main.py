from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import json

def new_chat(user_name):
    new_chat = driver.find_element(By.XPATH, '//div[@class="_2_1wd copyable-text selectable-text"]')
    new_chat.send_keys(user_name)
    time.sleep(2)
    
    try:
        user = driver.find_element(By.XPATH, '//span[@title="{}"]'.format(user_name))
        user.click()
    except NoSuchElementException as se:
        print('Username not in contact list')
    except Exception as e:
        driver.close()
        print(e)


class Member:
    def __init__(self, name, xp, startxp, previous_xp):
        self.name = name
        self.xp = xp
        self.startxp = startxp
        self.previous_xp = previous_xp


    def __str__(self):
        return f'{self.name} hat gerade {self.xp} XP und hat mit {self.startxp} XP angefangen. {self.name} hat insgesamt {self.calc_xp_total_gain()} XP gewonnen und ist somit seit beginn des Wettbewerbs auf dem {self.calc_position(member_list)}. Platz. Seit letzter Messung hat {self.name} {self.calc_xp_partial_gain()} XP gesammelt. Gute Arbeit!'

    def __repr__(self):
        return f'(\'{self.name}\', {self.xp}, {self.startxp})'

    def calc_xp_total_gain(self):
        with open("members.json", "r") as readfile:
            data = json.load(readfile, object_hook=lambda d: Member(**d))
            readfile.close()
        
        for i in range(0, len(data)):
            if data[i].name == self.name:
                return self.xp - data[i].startxp
        return None  # Return None if no matching name is found
    
    def get_xp_by_name(self, name, member_list):
        for person in member_list:
            if person.name == name:
                return person.xp
        return None  # Return None if no matching name is found

    def calc_xp_partial_gain(self):
        # get list of classes from json
        with open("members.json", "r") as readfile:
            data = json.load(readfile, object_hook=lambda d: Member(**d))
            # print(data)
            readfile.close()

        # # Get the previous xp from the member
        previous_xp = None
        for member in data:
            if member.name == self.name:
                self.previous_xp = member.previous_xp
                self.xp = member.xp
                break
    
        return self.xp - self.previous_xp
    
    def calc_position(self, member_list):
        for i in range(0, len(member_list)):
            if self.name == member_list[i].name:
                return i+1
            
with open("login.json", "r") as readfile:
    data = json.load(readfile)
    readfile.close()

username = data["name"]
password = data["password"]
groupname = 'Test'

# ## firefox
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

#chrome
# options = webdriver.ChromeOptions()
# options.add_argument("user-data-dir=selenium")
# # options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)

# #  duolingo

driver.get('https://www.duolingo.com/')

###not needed with chrome
# login = WebDriverWait(driver, 20).until(lambda x: x.find_element(By.CSS_SELECTOR, 'button.WOZnx')).click() #I already have an account
login = WebDriverWait(driver, 20).until(lambda x: x.find_element(By.XPATH, '/html/body/div[1]/div[1]/header/div[2]/div[2]/div/button')).click() #I already have an account

overlay = driver.find_element(By.ID, 'overlays')
# email_input = overlay.find_element(By.XPATH("//*[@data-test='email-input']"))
email_input = overlay.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/form/div[1]/div[1]/div[1]/input")
# email_input = overlay.find_element(By.XPATH, "/div[3]/div/div/form/div[1]/div[1]/div[1]/input")

email_input.send_keys(username)

password_input = overlay.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/form/div[1]/div[1]/div[2]/input")
# password_input = overlay.find_element(By.CSS_SELECTOR("[data-test='password-input']"))
password_input.send_keys(password)

password_input.send_keys(Keys.RETURN)

WebDriverWait(driver, 20).until(lambda x: x.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[3]/div[6]/a/span'))#.click()

#friends list
driver.get('https://www.duolingo.com/profile/' + username + '/following')

WebDriverWait(driver, 20).until(lambda x: x.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[1]/a/div[2]/h3'))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


name_element = soup.find_all("h3", {"class" : "rPqLh lZue0"})
xp_element = soup.find_all("div", {"class" : "_2lira _1soKk"})

#profile
driver.get('https://www.duolingo.com/profile/' + username)
WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/div[3]/div[2]/div/div[2]/div/div/h4'))

user_xp = driver.find_elements(By.CLASS_NAME, "_3gX7q")[1]

name = [i.text for i in name_element]
xp = [int(i.text[:-2]) for i in xp_element]

name.append(username)
xp.append(int(user_xp.text))

driver.quit()

member_list = []

with open("members.json", "r") as file:
    json_data = file.read()

member_list = json.loads(json_data, object_hook=lambda d: Member(**d))

print(member_list)

# for name_it, xp_it in zip(name, xp):
#     # person = Member(name_it, xp_it)
#     # member_list.append(person)

# for member in range(0, len(member_list)):
#     for i in range(0, len(name)):
#         if name[i] == member_list[member].name:
#             member_list[i].previous_xp = member_list[i].xp
#             member_list[i].xp = xp[i]
#             break

for member in member_list:
    for i in range(len(name)):
        if name[i] == member.name:
            member.previous_xp = member.xp
            member.xp = xp[i]
            break

with open("members.json", "w") as file:
    json.dump(member_list, file, default=lambda obj: obj.__dict__, indent=4)
    file.close()

# json_member_list = json.dumps(member_list, default=lambda o: o.__dict__, indent=4)
# print(json_member_list)
# with open("members.json", "w") as file:
#     file.write(json_member_list)

# print(repr(member_list))

msg = []

member_list.sort(key=lambda x: x.xp-x.xp_, reverse=True)

for i in range(0, len(member_list)):
    msg.append(str(member_list[i]))
    print(member_list[i])

#### whatsapp
### from https://github.com/The-Assembly/Automate-WhatsApp-with-Selenium


# optionschrome = webdriver.ChromeOptions()
# optionschrome.add_argument("user-data-dir=selenium")
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=optionschrome)

# driver.get('https://web.whatsapp.com/')


# WebDriverWait(driver, 300).until(lambda x: x.find_element(By.XPATH, '/html/body/div[1]/div/div/div[4]/header/div[1]/div/img'))

# try:
#     driver = driver.find_element(By.XPATH, '//span[@title="{}"]'.format(groupname))
#     driver.click()
# except NoSuchElementException as se:
#     new_chat(groupname)
#     time.sleep(1)

# time.sleep(2)
# message_box = driver.find_element(By.XPATH, '//div[@class="_3Uu1_"]')
# time.sleep(2)

# for i in range(0, len(msg)):
#     message_box.send_keys(msg[i])
#     time.sleep(0.1)
#     message_box.send_keys(Keys.RETURN)

