# load Required libraries and method

import Links
from requests import session
from datetime import datetime
from json import loads
from lxml import html
from os import environ
from deta import Deta
from dateutil.tz import gettz

deta = Deta(environ.get("DETA_PROJECT_KEY"))


class Logger:

    """Docstring for MyClass."""

    def __init__(self, Branch):
        self.branch = Branch
        self.cred = self.PreProcess()

    def PreProcess(self):

        USERNAME = environ.get(f"USERNAME_{self.branch}")
        PASSWORD = environ.get(f"PASSWORD_{self.branch}")
        LOGIN_URL = "http://op2020.mitsgwalior.in/login/index.php"

        cred0 = [LOGIN_URL, USERNAME, PASSWORD]
        return cred0

    def Ret_Links(self):

        LOGIN_URL, USERNAME, PASSWORD = self.cred
        # Aporach Schedule
        print("Loging in...", end="\r")

        # Setup session and cookies
        session_requests = session()

        # Get login csrf token
        result = session_requests.get(LOGIN_URL)
        tree = html.fromstring(result.text)
        authenticity_token = list(
            set(tree.xpath("//input[@name='logintoken']/@value"))
        )[0]

        # Create payload
        payload = {
            "username": USERNAME,
            "password": PASSWORD,
            "logintoken": authenticity_token,
        }

        # Perform login
        result = session_requests.post(
            LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL)
        )

        if result.url == LOGIN_URL:
            print("Invalid Credentials: Edit .env variables")
            exit(0)
        else:
            print("Logged in...")

        # Mark Atendance

        with open("./metadata/metadata.json", mode="r") as my_file:
            lectures = loads(my_file.read())[f"{self.branch}"]

        Detail_object = Links.Scraper(session_requests)

        dtobj = datetime.now(tz=gettz("Asia/Kolkata"))

        Details = {
            "key": "2wuho2fvwmnh",
            "last_updated": str(dtobj),
            "data": {"assignments": [], "quizes": []},
        }

        for lecture in lectures:
            try:
                Details["data"]["assignments"].extend(Detail_object.Scrape(lecture))
                print("\n+_+_+_+_+_+_+_+_+\n")

            except Exception as e:
                print(e)
        try:
            Details["data"]["assignments"] = sorted(
                Details["data"]["assignments"],
                key=lambda k: int(k["time_left"].split(" ")[0])
                if len(k["time_left"].split(" ")) >= 3
                else 0,
            )
            Details["data"]["assignments"] = sorted(
                Details["data"]["assignments"], key=lambda k: k["due"]
            )
        except Exception as e:
            print(e)

        db = deta.Base(self.branch)
        db.put(Details)

        return Details
