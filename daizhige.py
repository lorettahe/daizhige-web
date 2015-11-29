from flask import Flask, render_template, request, url_for
from os import listdir, getcwd
from os.path import isfile, join
from math import ceil
import re
import urllib.request
import urllib.parse
import json
from pagination import Pagination, get_page_numbers
from search import search_for_terms


class Breadcrumb(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path


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
    parent_dir = join("../daizhige-data", relative_parent_path)
    files_and_dir_names = listdir(parent_dir)
    list_items = [ListItem(join(relative_parent_path, f), f, isfile(join(parent_dir, f))) for f in files_and_dir_names]
    return list_items

app = Flask(__name__)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.route("/")
def index():
    dirs = listdir("../daizhige-data")
    title = u"殆知阁"
    return render_template("index.html", title=title, categories=dirs)

def article(path):
    article_name = re.search("([^/]+).txt", path).group(1)
    real_path = join("../daizhige-data", path)
    html_content = ""
    with open(real_path, "r") as article_content:
        is_title = True
        for line in article_content.readlines():
            if is_title:
                html_content = "<h2>" + line + "</h2>"
                is_title = False
            else:
                html_content = html_content + "<span>" + line + "</span><br/>"
    categories = listdir("../daizhige-data")
    return render_template("article.html", title=article_name, content=html_content, categories = categories)


def get_bread_crumbs(path):
    path_parts = path.split("/")
    bread_crumbs = [Breadcrumb(u"殆知阁", "/")]
    current_path = ""
    for path_part in path_parts:
        current_path = current_path + "/" +  path_part
        bread_crumbs.append(Breadcrumb(path_part, current_path))
    return bread_crumbs

@app.route("/<path:path>", methods=['GET'])
def category(path=None):
    if path.endswith(".txt"):
        return article(path)
    categories = listdir("../daizhige-data")
    page_no_str = request.args.get('page', '1')
    page_no = int(page_no_str)
    offset = (page_no-1) * 10
    list_items = get_list_items(path)
    result_list = list_items[offset:offset+10]
    total_num_pages = ceil(len(list_items) / 10)
    page_numbers = get_page_numbers(page_no, total_num_pages)
    pagination = Pagination(page_no, page_numbers, len(list_items), total_num_pages)
    breadcrumbs = get_bread_crumbs(path)
    return render_template("lists.html", title=path, categories = categories, files=result_list, category = path, pagination = pagination, breadcrumbs = breadcrumbs)

def combine_search(search_token):
    return '"{0}"'.format(search_token)


@app.route("/search", methods=['GET'])
def search():
    categories = listdir("../daizhige-data")
    search_str = request.args.get("terms")
    page_no = int(request.args.get('page', '1'))
    offset = 10*(page_no-1)
    [num_found, search_results] = search_for_terms(search_str, offset)
    total_num_pages = ceil(num_found / 10)
    page_numbers = get_page_numbers(page_no, total_num_pages)
    pagination = Pagination(page_no, page_numbers, num_found, total_num_pages)
    return render_template("search.html", categories=categories, terms=search_str,
                           list_items=search_results, pagination=pagination)

@app.route("/contact")
def contact():
    categories = listdir("../daizhige-data")
    return render_template("contact.html", title=u"联系站长", categories = categories)

if __name__ == "__main__":
    app.run(debug=True)
