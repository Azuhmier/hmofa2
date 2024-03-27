"""Module providing a function printing python version."""

import sys
import requests
import lxml.html

DATE_XPATH    = '/html/body/div[2]/div[2]/article[1]/header/div/span[2]/time'
OP_XPATH = '/html/body/div[2]/div[2]/article[1]/div[4]'

url = sys.argv[1]

response = requests.get(url, stream=True,timeout=10)
response.raw.decode_content = True

tree = lxml.html.parse(response.raw)

date = tree.xpath(DATE_XPATH)[0].text

op = tree.xpath(OP_XPATH)[0].text
thread_edition = op[-4:]

print(f"---------#{thread_edition} [ {date} ]")
