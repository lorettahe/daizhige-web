from flask import Flask, render_template, request, url_for
from os import listdir, getcwd
from os.path import isfile, join
from math import ceil
import re
import urllib.request
import urllib.parse
import json

class Pagination(object):
    
    def __init__(self, page, page_numbers, total_count, no_of_pages):
        self.page = page
        self.page_numbers = page_numbers
        self.total_count = total_count
        self.no_of_pages = no_of_pages

    @property
    def not_has_prev(self):
        return self.page == 1

    @property
    def not_has_next(self):
        return self.page == self.no_of_pages

def url_for_other_page(page):
    params = request.args.copy()
    params["page"]=str(page)
    url_values = urllib.parse.urlencode(params)
    return request.path + "?" + url_values

class ListItem(object):
    def __init__(self, path, name, is_file):
        self.path = path
        self.name = name
        self.is_file = is_file

def get_list_items(relative_parent_path):
    parent_dir = join("data", relative_parent_path)
    files_and_dir_names = listdir(parent_dir)
    list_items = [ListItem(join(relative_parent_path, f), f, isfile(join(parent_dir, f))) for f in files_and_dir_names]
    return list_items

app = Flask(__name__)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.route("/")
def index():
    dirs = listdir("data")
    title = "殆知阁"
    return render_template("index.html", title=title, categories=dirs)

def article(path):
    article_name = re.search("([^/]+).txt", path).group(1)
    real_path = join("data", path)
    html_content = ""
    with open(real_path, "r") as article_content:
        is_title = True
        for line in article_content.readlines():
            if is_title:
                html_content = "<h2>" + line + "</h2>"
                is_title = False
            else:
                html_content = html_content + "<span>" + line + "</span><br/>"
    categories = listdir("data")
    return render_template("article.html", title=article_name, content=html_content, categories = categories)

def get_page_numbers(page_no, total_num_pages):
    if page_no <= 3:
        page_numbers = list(range(1, min(6, total_num_pages+1)))
    elif page_no >= total_num_pages - 2:
        page_numbers = list(range(max(1, total_num_pages-4), total_num_pages+1))
    else:
        page_numbers = list(range(page_no-2, page_no+3))
    return page_numbers

@app.route("/<path:path>", methods=['GET'])
def category(path=None):
    if path.endswith(".txt"):
        return article(path)
    categories = listdir("data")
    page_no_str = request.args.get('page', '1')
    page_no = int(page_no_str)
    offset = (page_no-1) * 10
    list_items = get_list_items(path)
    result_list = list_items[offset:offset+10]
    total_num_pages = ceil(len(list_items) / 10)
    page_numbers = get_page_numbers(page_no, total_num_pages)
    pagination = Pagination(page_no, page_numbers, len(list_items), total_num_pages)
    return render_template("lists.html", title=path, categories = categories, files=result_list, category = path, pagination = pagination)

def combine_search(search_token):
    return "".join(["+"+c for c in search_token])

@app.route("/search", methods=['GET'])
def search():
    categories = listdir("data")
    search_str = request.args.get("terms")
    search_tokens = search_str.split(" ")
    real_search_str = " ".join([combine_search(token) for token in search_tokens])
    page_no = int(request.args.get('page','1'))
    params = {"q" : real_search_str, "wt" : "json", "indent" : "true", "start" : str(10*(page_no-1))}
    url_values = urllib.parse.urlencode(params)
    full_url = "http://localhost:8983/solr/gettingstarted_shard1_replica1/select?" + url_values
    print(full_url)
    with urllib.request.urlopen(full_url) as response:
        solr_response = response.read().decode("utf-8")
        solr_response_obj = json.loads(solr_response)
        num_found = solr_response_obj["response"]["numFound"]
        total_num_pages = ceil(num_found / 10)
        actual_responses = solr_response_obj["response"]["docs"]
        files = [re.search("20140103/(\S+)$", f["id"]).group(1) for f in actual_responses]
        list_items = [ListItem(f, re.search("([^/]+)$", f).group(1), True) for f in files] 
        title_str = "搜索结果: {0}".format(search_str)
        page_numbers = get_page_numbers(page_no, total_num_pages)
        pagination = Pagination(page_no, page_numbers, num_found, total_num_pages)
    return render_template("lists.html", title=title_str, categories = categories, files = list_items, category=title_str, pagination = pagination)

@app.route("/contact")
def contact():
    categories = listdir("data")
    return render_template("contact.html", title="联系站长", categories = categories)

if __name__ == "__main__":
    app.run(debug=True)
