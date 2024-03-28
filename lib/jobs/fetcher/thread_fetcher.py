""" doc """
import os
from lib.jobs.fetcher.fetcher import Fetcher 
from lib.utilities.iter import Iter
from lib.utilities.html_parser import HtmlParser

class ThreadFetcher(Fetcher):
    """doc"""

    last_fetched_updated = None
    last_fetched = None
    op = None
    page = None
    mode = 'New'



#    def get_last_fetched(self):
#        """ doc """
#        dir_list = self.list_dir()
#        calc = [max(int(fname) for fname in dir_list)]
#        self.last_fetched = calc[0]
#
#
#    def fetch(self) :
#        """ doc """
#
#        self.start_page()
#
#        while self.next_page() :
#            print('Page '+str(self.page.idx + 1))
#
#            while self.next_op() :
#                print('Post '+str(self.op.number))
#
#                if self.fname == self.last_fetched :
#
#                    if not self.last_fetched_updated:
#                        print("updating thread " +str(self.op.number))
#                        self.export()
#                        self.last_fetched_updated = True 
#                    else :
#                        print("thread " +str(self.fname)+" is already updated")
#                        if self.mode == 'new':
#                            break
#                        else :
#                            continue
#
#                elif os.path.exists(): 
#                    if os.stat().st_size == 0 :
#                        print("creating " +self.fname)
#                        self.export()
#                else :
#                    print("creating " +self.fname)
#                    self.export_to()
#                    if self.mode == 'new':
#                        break
#                    else :
#                        continue
#
#
#    def start_page(self):
#        """ doc """
#        self.page = Page(url = self.config['ops']['page_url'])
#
#
#    def next_page(self):
#        """ doc """
#
#        res = None
#        res = self.page.next()
#
#        if res is not None :
#            self.op = Op(list=res)
#
#        return res
#
#
#    def next_op(self):
#        """ doc """
#
#        res = self.op.next()
#
#        if res:
#            self.contents = self.op.contents
#            self.fname = self.op.number
#            self.fname_commit()
#
#        return res
#
#
#
#
class Page(HtmlParser,Iter):
    """ doc """


    def exists_next(self):
        """ doc """

        res = None

        if self.idx == -1 :

            res = self.url

        else :

            next_button_disabled = self.soup.find_all( "li", { "class":re.compile("next disabled") })

            if not next_button_disabled :
                next_button = self.soup.find_all( "li", { "class":re.compile("next") })
                res = next_button[0].find("a")["href"]

        return res


    def do(self):
        """ doc """
        res = None
        if self.url: 
            self.url = next_page_url
            res = self.soup.find_all( "article", { "class" : re.compile("post doc_id_") })
        return res




class Op(HtmlParser,Iter):
    """ doc """
    tgt_name = 'url'


    def get_tgt(self):
        """ doc """
        self.get_content()


    def exists_next(self):
        """ doc """

        res = None

        op_soup = self.list.pop(0)

        if res :
            reply_button = op_soup.find( "a", { "title" : "Reply to this post" })
            op_post_number = reply_button["data-post"]
            self.number = str(op_post_number).strip()
            res = reply_button["href"]

        return res



