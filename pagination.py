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


def get_page_numbers(page_no, total_num_pages):
    if page_no <= 3:
        page_numbers = list(range(1, min(6, total_num_pages+1)))
    elif page_no >= total_num_pages - 2:
        page_numbers = list(range(max(1, total_num_pages-4), total_num_pages+1))
    else:
        page_numbers = list(range(page_no-2, page_no+3))
    return page_numbers