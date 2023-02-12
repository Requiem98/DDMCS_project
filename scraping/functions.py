from libraries import *



def get_driver(cdriver = "normal"):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_experimental_option("detach", True)
    #chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    #chrome_options.add_argument("--user-data-dir=/home/amedeo/.config/google-chrome/")
    
    if(cdriver == "uc"):
        driver = uc.Chrome(options=chrome_options, browser_executable_path="/usr/bin/google-chrome-stable")
    elif(cdriver == "normal"):
        driver = Chrome(options=chrome_options)
    else:
        raise Exception("chrome driver not selected")
        
    driver.implicitly_wait(20)
    
    return driver


def tweeter_login(driver, username = "*****", password = "******", cdriver="normal"):
    
    
    url = 'https://twitter.com/i/flow/login'
    driver.get(url)
    
    
    

    driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]').click()
    driver.find_element(By.TAG_NAME, 'input').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]').click()
    
    
    
    password_field = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div')
    password_field.click()
    password_field.find_element(By.TAG_NAME, 'input').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div').click()

    
    
def deny_notification_popup(driver):
        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/span')))
        notification_button = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]')
        notification_button.click()
        
def select_first_tweet(driver):
    tweet = driver.find_element(By.XPATH, '//div[@style="transform: translateY(0px); position: absolute; width: 100%; transition: opacity 0.3s ease-out 0s;"]')
    tweet_id = tweet.get_attribute("style")
    
    select_tweet(driver, tweet.find_element(By.TAG_NAME, "article"))
    return tweet_id

def allow_cookie_popup(driver):
    allow_button = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]')
    allow_button.click()
    
def query(driver, query):
    
    search_bar = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
    search_bar.click()
    search_bar.send_keys(query)
    
def select_latest_tweets(driver):
    latest_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]')
    latest_button.click()
    
def select_top_tweets(driver):
    top_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[1]')
    top_button.click()
    


def select_first_user(driver):
    
    user = driver.find_element(By.XPATH, '//div[starts-with(@style, "transform: translateY(0px);")]')
    user_id = user.get_attribute("style")[:46]
    
    try:
        user = user.find_element(By.PARTIAL_LINK_TEXT, "@")
        username = user.find_element(By.XPATH, f'//div[starts-with(@style, "{user_id}")]//span[starts-with(text(), "@")]').text
    
        followers = scrape_followers(driver, user)
    
    except NoSuchElementException as e:
        print(str(e))
        username = ""
        followers = []
    
    return user_id, username, followers

def scroll_users(driver, dataframe):
    
    print("\n\nStarting query...")
    print("\n\n")
    
    i = 1
    max_fail = 3 
        
    allow_cookie_popup(driver)
    
    #deny_notification_popup(driver)
    
    
    user_id, username, followers = select_first_user(driver)

    if(username.startswith("@") and not dataframe["username"].isin([username]).any()):
        dataframe.loc[len(dataframe)] = [username, followers]

    while(i<10000):
        
        try:  
            previous_user = driver.find_element(By.XPATH, f'//div[starts-with(@style, "{user_id}")]')
            
            time.sleep(0.3)
            
            next_user = driver.execute_script("""return arguments[0].nextElementSibling""", previous_user)
            
            if(user_id != next_user.get_attribute("style")[:46]):
                user_id = next_user.get_attribute("style")[:46]
                
            else:
                next_user = driver.execute_script("""return arguments[0].nextElementSibling""", next_user)
                user_id = next_user.get_attribute("style")[:46]
                
            
            driver.execute_script("arguments[0].scrollIntoView(false);", next_user)
                    
            user = next_user.find_element(By.PARTIAL_LINK_TEXT, "@")
            
            username = next_user.find_element(By.XPATH, f'//div[starts-with(@style, "{user_id}")]//span[starts-with(text(), "@")]').text
            
            if(not dataframe["username"].isin([username]).any()):
                       
                followers = scrape_followers(driver, user)
            
                dataframe.loc[len(dataframe)] = [username, followers]
            
                dataframe.to_pickle("Data/users_and_followers_data.pkl")
            
        
        except NoSuchElementException as e:
            print("\nNo such element\n")
            max_fail -= 1
            if(max_fail <= 0):
                max_fail = 3
                break
        except (WebDriverException, InvalidSessionIdException) as e:
            print(str(e))
            break
        finally:
            i += 1
            print(f"\nnumber of user saved: {i}\n")

    print("\n\n")
    print("Query done!")
        

            
def select_first_follower(driver):
    follower = driver.find_element(By.XPATH, '//div[starts-with(@style, "transform: translateY(0px);")]')
    follower_id = follower.get_attribute("style")[:46]
    
    follower_name = follower.find_element(By.XPATH, f'//div[starts-with(@style, "{follower_id}")]//span[starts-with(text(), "@")]').text
    
    
    return follower_id, follower_name
            

def scrape_followers(driver, user):
    
    print("start retriving followers...")
    
    followers = list()
    user.click()
    i = 2
    max_fail = 3
    #num_followers = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span').text
    num_followers = driver.find_element(By.XPATH, "//a[substring(@href, string-length(@href) - string-length('followers') +1) = 'followers']").find_elements(By.TAG_NAME, "span")[1].text
    
    if("K" in num_followers):
        num_followers = 1000
    elif("M" in num_followers):
        num_followers = 1000
    elif(int(num_followers.replace(",", "")) > 1000):
        num_followers = 1000
    else:
        num_followers = int(num_followers.replace(",", ""))
    
    
    
    #followers_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[2]/span')
    followers_button = driver.find_element(By.XPATH, '//span[text() = "Followers"]')
    followers_button.click()
    
    
        
    follower_id, follower_name = select_first_follower(driver)
    
    followers.append(follower_name)
        
    for i in tqdm(range(num_followers-5)):
        
        try: 
            
            previous_follower = driver.find_element(By.XPATH, f'//div[starts-with(@style, "{follower_id}")]')
            
            next_follower = driver.execute_script("""return arguments[0].nextElementSibling""", previous_follower)
            
        
            if(follower_id != next_follower.get_attribute("style")[:46]):
                follower_id = next_follower.get_attribute("style")[:46]
                
            else:
                next_follower = driver.execute_script("""return arguments[0].nextElementSibling""", next_follower)
                follower_id = next_follower.get_attribute("style")[:46]
                
            
            driver.execute_script("arguments[0].scrollIntoView(false);", next_follower)
            
            
            #follower_name = next_follower.find_elements(By.TAG_NAME, "a")[1].find_element(By.TAG_NAME, "span").text
            follower_name = next_follower.find_element(By.XPATH, f'//div[starts-with(@style, "{follower_id}")]//span[starts-with(text(), "@")]').text
            
            if(follower_name.startswith("@")):
                followers.append(follower_name)
        
        except (NoSuchElementException, AttributeError) as e:
            #traceback.print_exc()
            print("\nNo such element\n")
            max_fail -= 1
            if(max_fail <= 0):
                max_fail = 3
                break
        except (WebDriverException, InvalidSessionIdException) as e:
            print(str(e))
            break

    
    print("followers retrived")
    driver.back()
    driver.back()
        
    return followers

    

def get_usernames(queries):
    
    if(os.path.exists("Data/users_and_followers_data.pkl")):
        dataframe = pd.read_pickle("Data/users_and_followers_data.pkl")
    else:
        dataframe = pd.DataFrame(columns=["username", "followers"])
    
    
    for qry in tqdm(queries):
        for order in ["top", "latest"]:
            
            try:
                
                driver = get_driver(cdriver = "normal")
                
                tweeter_login(driver = driver)
                
                query(driver, qry)
                
                if(order == "top"):
                    select_top_tweets(driver)
                else:
                    select_latest_tweets(driver)
                
                scroll_users(driver, dataframe)
                
            except InvalidSessionIdException as e:
                pass
    



#==============================================================================
#==============================================================================
#==============================================================================

def select_first_tweet(driver):
    
    try:
        tweet = driver.find_element(By.XPATH, '//div[starts-with(@style, "transform: translateY(0px);")]')
        tweet_id = tweet.get_attribute("style")[:46]
        
        
        tweet = tweet.find_element(By.XPATH, f"//div[starts-with(@style, '{tweet_id}')]//div[@data-testid = 'tweetText']").text
    
    except NoSuchElementException as e:
        print("\nNo such element\n")
        tweet = ""
        tweet_id = ""
    
    return tweet_id, tweet


def scroll_tweets(driver, dataframe, user):
    
    
    
    i = 1
    max_fail = 2
        
        
    allow_cookie_popup(driver)
    
    #deny_notification_popup(driver)
    
    
    tweet_id, tweet = select_first_tweet(driver)

    if(tweet != ""):
        dataframe.loc[len(dataframe)] = [user, tweet]

    while(i<10000):
        
        try:  
            previous_tweet = driver.find_element(By.XPATH, f'//div[starts-with(@style, "{tweet_id}")]')
            
            time.sleep(0.3)
            
            
            next_tweet = driver.execute_script("""return arguments[0].nextElementSibling""", previous_tweet)
            
            try:
                if(tweet_id != next_tweet.get_attribute("style")[:46]):
                    tweet_id = next_tweet.get_attribute("style")[:46]
                    
                else:
                    next_tweet = driver.execute_script("""return arguments[0].nextElementSibling""", next_tweet)
                    tweet_id = next_tweet.get_attribute("style")[:46]
                    
            except AttributeError as e:
                break
            
            driver.execute_script("arguments[0].scrollIntoView(false);", next_tweet)
                    
            tweet = next_tweet.find_element(By.XPATH, f"//div[starts-with(@style, '{tweet_id}')]//div[@data-testid = 'tweetText']").text
            
            dataframe.loc[len(dataframe)] = [user, tweet]
            
            dataframe.to_pickle("Data/users_tweets_data.pkl")
            
        
        except NoSuchElementException as e:
            print("\nNo such element\n")
            max_fail -= 1
            if(max_fail <= 0):
                break
            
        except (WebDriverException, InvalidSessionIdException) as e:
            print("\n\nSession closed, starting new one...\n\n")
            break
        finally:
            i += 1

    



def get_tweets(users, queries):
    
    if(os.path.exists("Data/users_tweets_data.pkl")):
        dataframe = pd.read_pickle("Data/users_tweets_data.pkl")
    else:
        dataframe = pd.DataFrame(columns=["username", "tweet"])
    
    
    for user, qry in tqdm(zip(users, queries), total=len(users)):
        
        try:
            
            driver = get_driver(cdriver = "normal")
            
            tweeter_login(driver = driver)
            
            query(driver, qry)
            
            select_latest_tweets(driver)
            
            scroll_tweets(driver, dataframe, user)
            
        except InvalidSessionIdException as e:
            pass




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



