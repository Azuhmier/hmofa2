"""doc"""
import re
import os
from bs4 import BeautifulSoup
from lib.fetch.fetch import Fetch
class Fetch_ops(Fetch):
    """ doc """

    #Runtime
    last_fetched_updated = None
    last_fetched = None
    page_list = None
    op = None
    page = None
    contents = None

    # payload
    page_url = None,
    max_page = 1000,
    mode = 'missing'
    


    def do_special(self, args) :
        """ doc """
        self.page_url = self.l_config['ops']['page_url']
        self.tgt_dir = self.l_config['ops']['tgt_dir']

        self.check_args(args)

        self.last_fetched_updated = False
        self.last_fetched = None


            
    def __get_last_fetched(self):
        """ doc """
        directory_list = self.list_dir(self.tgt_dir)
        res = [max(int(thread_num) for thread_num in directory_list)]
        self.last_fetched = res[0]

    def fetch_threads(self) :
        """ doc """

        self.start_page()

        while self.next_page() :
            print('Page '+str(self.page.idx + 1))

            while self.next_op() :
                print('Post '+str(self.op.number + str(1)))
                file_name = str(self.op.number) + ".html"

                if self.op.number == self.last_fetched :

                    if not self.last_fetched_updated:
                        print("updating thread " +str(self.op.number))
                        self.get_thread()
                        self.save_thread()
                        self.last_fetched_updated = True 
                    else :
                        print("thread " +str(self.op.number)+" is already updated")
                        if self.mode == 'new':
                            break
                        else :
                            continue

                elif os.path.exists(self.get_path(file_name)): 
                    if os.stat(self.get_path(file_name)).st_size == 0 :
                        print("creating thread " +str(self.op.number))
                        self.get_thread()
                        self.save_thread()
                else :
                    print("creating thread " +str(self.op.number))
                    self.get_thread()
                    self.save_thread()
                    if self.mode == 'new':
                        break
                    else :
                        continue


    def start_page(self):
        """ doc """
        self.page = Page(self.page_url)

    def next_page(self):
        """ doc """
        page = self.page
        return self.page.next_page()

    def next_op(self):
        """ doc """
        self.op = None
        res = self.page.next_op()
        if res is not None :
            op_post_number = res[1]
            op_url = res[0]
            self.op = Op(op_url,op_post_number)
        return res


    def save_thread(self):
        """ doc """
        file_name = self.op.number+".html"
        file_path = os.path.join(self.tgt_dir, file_name)

        self.export_to(file_path, self.op.r.text)
        


class Page(Fetch):
    """ doc """

    url = None
    idx = None
    op_idx = None
    soup = None
    r = None
    ops = None
    def __init__(self, url):
        """ doc """
        self.url = url
        self.idx = -1
        self.op_idx = -1

    def next_page(self):
        """ doc """
        next_page_url = None
        if self.idx == -1 :
            next_page_url = self.url
        else :
            next_button_disabled = self.soup.find_all( "li", { "class":re.compile("next disabled") })
            if not next_button_disabled :
                next_button = self.soup.find_all( "li", { "class":re.compile("next") })
                next_page_url = next_button[0].find("a")["href"]

        if next_page_url: 
            self.url = next_page_url
            self.get_content(self.url)
            self.soup = BeautifulSoup(self.r.content, 'html.parser')
            ops = self.soup.find_all( "article", { "class" : re.compile("post doc_id_") })
            self.ops = ops
            self.idx = self.idx+1
            self.op_idx = -1

        return next_page_url

    def next_op(self):
        """ doc """
        res = None
        if len(self.ops) >= (self.op_idx + 2):
            self.op_idx = self.op_idx + 1
            op = self.ops[self.op_idx]
            reply_button = op.find( "a", { "title" : "Reply to this post" })
            op_post_number = reply_button["data-post"]
            op_post_number = str(op_post_number).strip()
            op_url = reply_button["href"]
            res = [op_url, op_post_number]
        return res


class Op(Fetch):
    """ doc """
    url = None
    number = None
    r = None
    soup=None
    content=None
    def __init__(self,url,post_number):
        """ doc """
        self.url = url
        self.number = post_number

    def get_thread(self):
        """ doc """
        self.get_content(self.url)
        self.soup = BeautifulSoup(self.r.content, 'html.parser')
