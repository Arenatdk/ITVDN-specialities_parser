import bs4
import requests
import os

specReq=requests.get('https://itvdn.com/ru/specialities')
specHTML=bs4.BeautifulSoup(specReq.text, "html.parser")
spec = specHTML.find_all(attrs={"class": "specialities__item"})
for i in spec:
    print(i['href'])

    direname =i.contents[3].getText()
    for ch in "\/:*?<>|":
        direname= direname.replace(ch,"")
    os.makedirs('kurs/'+direname)
    print(i.contents[3].getText())


    s=requests.get('https://itvdn.com'+i['href'])

    b=bs4.BeautifulSoup(s.text, "html.parser")
    #print(b.prettify)

    kurs = b.find_all(attrs={"class": "catalog-item-line"})

    for kr in kurs:
        fn = kr.find('a').getText()
        for ch in "\/:*?<>|":
            fn= fn.replace(ch, "")

        f = open('kurs/'+direname+"/"+fn+".txt", 'w', encoding='utf-8')
        print("--------------------------------------------------------------------------" +kr.find('a').getText())
        kursHTML = requests.get('https://itvdn.com'+kr.find('a')["href"])#Страница курса
        BSkurs = bs4.BeautifulSoup(kursHTML.text, "html.parser")
        DataOfLess = BSkurs.find_all(attrs={"class":"video-lesson-item"})
        for NLess in DataOfLess:
            f.write(NLess.contents[1].contents[1].contents[1].getText()+"  ") # Номер
            f.write(NLess.contents[1].contents[3].getText()+"\n") # Имя

            print(NLess.contents[1].contents[1].contents[1].getText() +"   "+NLess.contents[1].contents[3].getText() )  # Номер
            #print(NLess.contents[1].contents[3].getText())  # Имя
           # print(NLess.contents[1]["href"])  # Ссылка

            tmHtml = requests.get('https://itvdn.com'+NLess.contents[1]["href"])
            Timeng = bs4.BeautifulSoup(tmHtml.text, "html.parser")
            times = Timeng.find_all(attrs={"class":"video-breakpoints-item"})
            for tm in times:
                f.write("       ")
                f.write(tm.contents[1].contents[3].getText().rstrip().lstrip()+" ")
                f.write(tm.contents[3].getText().rstrip().lstrip()+"\n")
                #print("*+++++")
                print("     "+tm.contents[1].contents[3].getText().rstrip().lstrip() + " " +tm.contents[3].getText().rstrip().lstrip() ) # Время
                #print(tm.contents[3].getText().rstrip().lstrip())  # Время
        f.close()

