""" doc """
import os
from lib.fetcher.single_fetcher import SingleFetcher
from lib.main import Main
from lib.controllers.single_file_controller import SingleFileController
from lib.parser.single_html_parser import SingleHtmlParser

class OpFetcher(SingleFetcher,SingleFileController):
    """doc"""


    #Runtime
    fext='html'
    last_fetched_updated = None
    last_fetched = None
    op = None
    page = None


    def do_args(self, args) :
        """ doc """


    def get_last_fetched(self):
        """ doc """
        dir_list = self.list_dir(self.tgt_dir)
        calc = [max(int(fname) for fname in dir_list)]
        self.last_fetched = calc[0]


    def fetch(self) :
        """ doc """

        self.start_page()

        while self.next_page() :
            print('Page '+str(self.page.idx + 1))

            while self.next_op() :
                print('Post '+str(self.op.number))

                if self.fname == self.last_fetched :

                    if not self.last_fetched_updated:
                        print("updating thread " +str(self.op.number))
                        self.export_to(self.relpath,self.contents)
                        self.last_fetched_updated = True 
                    else :
                        print("thread " +str(self.op.number)+" is already updated")
                        if self.mode == 'new':
                            break
                        else :
                            continue

                elif os.path.exists(self.get_abs_path(self.rel_path)): 
                    if os.stat(self.get_abs_path(self.rel_path)).st_size == 0 :
                        print("creating thread " +str(self.op.number))
                        self.export_to(self.relpath,self.contents)
                else :
                    print("creating thread " +str(self.op.number))
                    self.export_to(self.relpath,self.contents)
                    if self.mode == 'new':
                        break
                    else :
                        continue


    def start_page(self):
        """ doc """
        self.page = Page(url = self.l_config['ops']['page_url'])


    def next_page(self):
        """ doc """

        res = None
        res = self.page.next()

        if res is not None :
            self.op = Op(list=res)

        return res


    def next_op(self):
        """ doc """

        res = self.op.next()

        if res:
            self.contents = self.op.contents
            self.fname = self.op.number
            self.fname_commit()

        return res




class Page(SingleHtmlParser):
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
            res = None
            if self.url: 
                self.url = next_page_url
                res = self.soup.find_all( "article", { "class" : re.compile("post doc_id_") })
            return res




class Op(SingleFileController):


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



