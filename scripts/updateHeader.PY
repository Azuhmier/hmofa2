import requests
import lxml.html
import sys

url = sys.argv[1]
date_xpath    = '/html/body/div[2]/div[2]/article[1]/header/div/span[2]/time'
op_xpath = '/html/body/div[2]/div[2]/article[1]/div[4]'
response = requests.get(url, stream=True)
response.raw.decode_content = True
tree = lxml.html.parse(response.raw)
date = tree.xpath(date_xpath)[0].text
OP = tree.xpath(op_xpath)[0].text
thread_edition = (OP[-4:])
print ("---------#%s [ %s ]" % (thread_edition, date))

#from urllib.request import urlopen
#from lxml import etree
#response = urlopen(url)
#htmlparser = etree.HTMLParser()
#tree = etree.parse(response, htmlparser)
#session = requests.Session()
#r       = session.get(url)
#soup    = BeautifulSoup(r.content, 'html.parser')
#print(str(a))
#print(str(type(a)))
#print(str(type(a[0])))
#print(str(a[0].__dict__))
#print(str(a[0]))
#print(str(dir(a[0])))
#method_list = [method for method in dir(a[0]) if method.startswith('__') is False]
#print(method_list)
