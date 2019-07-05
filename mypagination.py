# coding: utf-8


# import logging
from rest_framework.response import Response


class MyPaginate(object):
    """自定义分页模块"""

    def __init__(self, data, page_size=None, page_num=None):
        self.data = data
        self.page_size = self.__set_page_size(page_size)
        self.data_length = len(data)
        self.page_total = self.__compute_page_total()
        self.page_num = self.__set_page_num(page_num)
        self.index = self.__get_index()

    def __set_page_size(self, page_size):
        """设置页面大小"""
        if page_size is None:
            # 默认5条数据
            return 5
        page_size = int(page_size)
        if page_size > 1000:
            # 最大1000条数据
            return 1000

        return page_size

    def __set_page_num(self, page_num):
        if page_num is None:
            # 默认第一页
            return 1

        return int(page_num)

    def __compute_page_total(self):
        """计算总页数"""
        if self.page_size == 0:
            return 0
        tmp_total = self.data_length / self.page_size
        remainder = self.data_length % self.page_size
        page_total = tmp_total + 1 if remainder > 0 else tmp_total
        return page_total

    def __get_index(self):
        """获取起始索引"""
        end_index = self.page_size + ((self.page_num - 1) * self.page_size)
        start_index = end_index - self.page_size
        return (start_index, end_index)

    def get_paginated_response(self, data):
        """返回response对象"""
        return Response({
            "pageSize": self.page_size,
            "total": self.data_length,
            "pageNum": self.page_num,
            "page_total": self.page_total,
            'results': data
        })

    @property
    def paginated_data(self):
        """分页的data 的list"""
        if self.page_total <= 0 or self.page_num <= 0 or self.page_num > self.page_total:
            return []
        elif self.page_total == self.page_num:
            return self.data[self.index[0]:]
        else:
            return self.data[self.index[0]:self.index[1]]
