import re
import os
import psutil
import sys
from time import time
from operator import add
from functools import reduce
from django.db import connection
from django.utils.deprecation import MiddlewareMixin


class StatsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request._mem = psutil.Process(os.getpid()).memory_info()

    def process_view(self, request, view_func, view_args, view_kwargs):
        '''
        In your base template, put this:
        <div id="stats">
        <!-- STATS: sql: %(db_queries)d  db: %(db_time).0fms  py: %(python_time).0fms  total: %(total_time).0fms ENDSTATS -->        </div>
        '''

        # Uncomment the following if you want to get stats on DEBUG=True only
        #if not settings.DEBUG:
        #    return None

        # get number of db queries before we do anything
        # n = len(connection.queries)

        # time the view
        start = time()
        response = view_func(request, *view_args, **view_kwargs)
        total_time = time() - start

        # compute the db time for the queries just run
        # db_queries = len(connection.queries) - n
        # if db_queries:
        #     db_time = reduce(add, [float(q['time'])
        #                            for q in connection.queries[n:]])
        # else:
        #     db_time = 0.0

        # and backout python time
        # python_time = total_time - db_time

        mem = psutil.Process(os.getpid()).memory_info()
        diff = mem.rss - request._mem.rss

        stats = {
            'total_time': total_time * 1000,
            # 'python_time': python_time * 1000,
            # 'db_time': db_time * 1000,
            # 'db_queries': db_queries,
            'memory_use': diff / 1024
        }

        # replace the comment if found
        if response:
            if (hasattr(response, 'is_rendered') and
                response.is_rendered or not
                    hasattr(response, 'is_rendered')) and response.content:
                s = response.content
                regexp = re.compile(r'(?P<cmt><!--\s*STATS:(?P<fmt>.*?)ENDSTATS\s*-->)')
                match = regexp.search(s)
                if match:
                    s = (s[:match.start('cmt')] +
                         match.group('fmt') % stats +
                         s[match.end('cmt'):])
                    response.content = s
        return response
