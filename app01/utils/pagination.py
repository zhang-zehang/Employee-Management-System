"""
Custom pagination component. If you want to use this pagination component in the future, you need to do the following:

In the view function:
    def pretty_list(request):

        # 1. Filter your data according to your own situation
        queryset = models.PrettyNum.objects.all()

        # 2. Instantiate the pagination object
        page_object = Pagination(request, queryset)

        context = {
            "queryset": page_object.page_queryset,  # Paginated data
            "page_string": page_object.html()       # Pagination HTML
        }
        return render(request, 'pretty_list.html', context)

In the HTML page:

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>

"""

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: Request object
        :param queryset: Filtered data (pagination is applied to this data)
        :param page_size: Number of records displayed per page
        :param page_param: Parameter used for pagination in the URL, e.g., /etty/list/?page=12
        :param plus: Number of pages displayed before and after the current page
        """

        from django.http.request import QueryDict
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        page = request.GET.get(page_param, "1")

        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # Calculate the pages to display before and after the current page
        if self.total_page_count <= 2 * self.plus + 1:
            # Not enough data for more than 11 pages.
            start_page = 1
            end_page = self.total_page_count
        else:
            # More than 11 pages of data in the database.

            # Current page is less than 5 (small boundary)
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # Current page is greater than 5
                # Current page + 5 > total number of pages
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # Pagination links
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">First</a></li>'.format(self.query_dict.urlencode()))

        # Previous page
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">Previous</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">Previous</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # Pages
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # Next page
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">Next</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">Next</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # Last page
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">Last</a></li>'.format(self.query_dict.urlencode()))

        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page"
                           style="position: relative;float:left;display: inline-block;width: 80px;border-radius: 0;"
                           type="text" class="form-control" placeholder="Page Number">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">Go</button>
                </form>
            </li>
            """

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
