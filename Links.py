# Import WebScraping and Form Filling Libraries

from bs4 import BeautifulSoup
import requests
import lxml
import cchardet
from datetime import datetime
from deta import Deta
from os import environ

deta = Deta(environ.get("DETA_PROJECT_KEY"))
db = deta.Base("Completed")

class Scraper():

    """
        Attendance class defing and allocating prerequisits which are required before marking attendance
    """

    def __init__(self, Session):

        self.Checked = db.get("ignore")["links"]
        self.session = Session
        self.id = 0

    def Assingment_To_Json(self,Title,Details):
        now = datetime.now()
        Pretty = []
        Completed = self.Checked

        for Detail in Details:
            Time_Left = str(datetime.strptime(Detail[1],"%A, %d %B %Y, %I:%M %p") - now)[:-7]
            Det = {
                    "id": self.id,
                    "subject":Title,
                    "title":Detail[0],
                    "due_date":Detail[1],
                    "status":Detail[2],
                    "link":Detail[3],
                    "time_left": Time_Left,
                    }

            if (Time_Left[0] == "-"):
                Det["time_left"] = Det["time_left"][1:]
                Det["due"]=True
                Completed.append(int(Det["link"][-4:]))

            else:
                Det["due"]=False
                Pretty.append(Det)

            self.id += 1

        db.put({"key":"ignore","links":Completed})

        return Pretty;

    def Scrape(self,Lecture):

        result = self.session.get(Lecture, headers = dict(referer = Lecture))
        soup = BeautifulSoup(result.content, 'lxml')
        Sections = soup.find_all("li",attrs={"class":"section main clearfix"})

        for_All = []
        for Section in Sections:
            Assingments_Links = []
            Quizes_Links = []

            try:
                Title = Section.find("h3",attrs={"class":"sectionname"}).find('a').contents[0]

                try:
                    Assingments = Section.find_all("li", attrs={"class":"activity assign modtype_assign"})
                    Assingments_Links = [ Itter.find("a",attrs={"class":"aalink"})['href'] for Itter in Assingments ]

                except Exception:
                    pass


                Assingment_Details = []

                for Assingment_Link in Assingments_Links:
                    Assingment_Details.append(self.Find_Assingments(Lecture,Assingment_Link))

                if Assingment_Details != []:
                    for_All.extend(self.Assingment_To_Json(Title, Assingment_Details))

            except Exception as e:
                print(e)

        return for_All

    def Find_Assingments(self,Lecture, Link):

        result = self.session.get(Link , headers = dict(referer = Lecture))
        soup = BeautifulSoup(result.content, 'lxml')

        Table = soup.find("table",attrs={"class":"generaltable"})
        Main = soup.find("div", attrs={"role":"main"})

        Title = Main.find("h2").contents[0]

        try:
            Table.find("td", attrs={"class":"submissionstatussubmitted cell c1 lastcol"}).contents[0]
            Due = Table.find("td",attrs={"class":"cell c1 lastcol"}).contents[0]
            Status = "Done";

        except Exception as e:
            Due = Table.find_all("td",attrs={"class":"cell c1 lastcol"})[1].contents[0]
            Status = "Due";

        return [Title,Due,Status,Link]
