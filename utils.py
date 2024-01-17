import urllib.parse, os, re
import docx2txt, glob
import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI


def create_mailto(to, role, companyname, resp):
    return f"https://mail.google.com/mail/?view=cm&fs=1&to={urllib.parse.quote(to)}&su=Applying+for+{urllib.parse.quote(role)}+at+{urllib.parse.quote(urllib.parse.quote(role))}&body={urllib.parse.quote(resp)}"


def get_jd(jd_link):
    return (
        "\n".join(
            [
                re.sub("\s", " ", line.strip())
                for line in BeautifulSoup(
                    requests.get(jd_link).content, features="html.parser"
                )
                .text.replace("\r", "\n")
                .split("\n")
                if line.strip()
            ]
        )
        if jd_link
        else ""
    )


def get_resume(url):
    os.system(f"gdown {url.split('/')[-2]}")
    with open(glob.glob("*.docx")[0], "rb") as infile:
        return docx2txt.process(infile)


def get(q):
    return ChatGoogleGenerativeAI(model="gemini-pro").invoke(q)
