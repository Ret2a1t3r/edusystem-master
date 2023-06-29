import copy

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=15, page_param="page", skip=5):

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_param, '1')

        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.page_param = page_param
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()

        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.skip = skip

    def html(self):
        skip = 5
        if self.total_page_count <= 2 * skip + 1:
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            if self.page <= skip:
                start_page = 1
                end_page = 2 * skip + 1
            else:
                if (self.page + skip) > self.total_page_count:
                    start_page = self.total_page_count - skip * 2
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - skip
                    end_page = self.page + skip + 1

        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}"> 首页 </a></li>'.format(self.query_dict.urlencode()))

        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}"> << </a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}"> << </a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        for i in range(start_page, end_page):
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prov = '<li><a href="?{}"> >> </a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prov = '<li><a href="?{}"> >> </a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prov)

        self.query_dict.setlist(self.page_param, [self.total_page_count])
        last = '<li><a href="?{}"> 尾页 </a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(last)

        page_string = mark_safe(''.join(page_str_list))
        return page_string
