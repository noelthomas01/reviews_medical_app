from selenium import webdriver
from selenium.webdriver import Firefox
import time
import pandas as pd 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import gensim
from gensim.summarization import summarize
# for task 3
def func(row): # for task 3 
    if row.Rating >3: 
        return "Positive Review"
    else: #summarising the negative reviews 
        stop_words = set(stopwords.words('english'))
        rev = row.Reviews.lower() #to be able to be compared with stopwords
        if len(sent_tokenize(rev)) > 1:
           rev = summarize(rev, ratio=0.4) 
           if rev == "":
               rev = row.Reviews.lower()
        templist = word_tokenize(rev)
        for w in templist:
            if w in stop_words:
                templist.remove(w) #removing stopwords 
        text = " ".join(templist)
    return text
#the dictionary has the competitors with their google play store review links
websites = {'Lybrate':'https://play.google.com/store/apps/details?id=com.lybrate.phoenix&hl=en_IN&gl=US&showAllReviews=true','Practo':'https://play.google.com/store/apps/details?id=com.practo.fabric&hl=en_IN&gl=US&showAllReviews=true','Zocdoc':'https://play.google.com/store/apps/details?id=com.zocdoc.android&hl=en_IN&gl=US&showAllReviews=true','DocsApp':'https://play.google.com/store/apps/details?id=com.docsapp.patients&hl=en_IN&gl=US&showAllReviews=true','Doctor on Demand':'https://play.google.com/store/apps/details?id=com.doctorondemand.android.patient&hl=en_IN&gl=US&showAllReviews=true','MDLive':'https://play.google.com/store/apps/details?id=com.mdlive.mobile&hl=en_IN&gl=US&showAllReviews=true','Amwell':'https://play.google.com/store/apps/details?id=com.americanwell.android.member.amwell&hl=en_IN&gl=US&showAllReviews=true','Lemonaid Health':'https://play.google.com/store/apps/details?id=com.polkadoc.ocp&hl=en_IN&gl=US&showAllReviews=true','Hey Doctor':'https://play.google.com/store/apps/details?id=co.heydoctor.android&hl=en_IN&gl=US&showAllReviews=true'}
websites_list = list(websites.values())
names = list(websites.keys())

path = 'C:/geckodriver.exe'
driver = webdriver.Firefox(executable_path=path)
comp = []
review = []
rating = []
for i in range(len(websites_list)): #iterating for each competitor 
    url = websites_list[i]
    driver.get(url)
#     time.sleep(10)
    for j in range(40): #no of reviews to take
        comp.append(names[i])
        rate = driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div/div["+str(j+1)+"]/div/div[2]/div[1]/div[1]/div/span[1]/div/div")
        star = rate.get_attribute('aria-label') #will return 'Rated x out of five stars'
        star = int(star[6]) #getting the number and converting to int
        rating.append(star)
        rev = driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div/div["+str(j+1)+"]/div/div[2]/div[2]/span[1]").text #getting the reviews
        review.append(rev)
df = pd.DataFrame({'Website':comp,'Reviews':review,'Rating':rating})

df['Reviews Summary'] = df.apply(func,axis = 1)
df = df.sort_values(by = 'Rating')
df.to_excel("competitors_reviews.xlsx")
