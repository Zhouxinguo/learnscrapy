# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,time

class LearnscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class SPA4Pipeline(object):
    def __init__(self):
        self.conn : pymysql.connect = None
        self.cur : pymysql.cursors.Cursor
        self.queue = []
        self.count = 0

    def open_spider(self,spider):
        self.conn = pymysql.connect(host='0.0.0.0',user='root',password='mysql',db='test',port=3306,charset='utf8')
        self.cur = self.conn.cursor()

    def close_spider(self,spider):
        if len(self.queue) > 0:
            self.insert_datanase()
        self.cur.close()
        self.conn.close()

    def insert_datanase(self):
        sql = "insert into spa4 (code,published_at,title,updated_at,url,website) values (%s,%s,%s,%s,%s,%s)"
        self.cur.executemany(sql,self.queue)
        self.queue.clear()
        self.conn.commit()


    def process_item(self, item, spider):
        self.queue.append(
            (item['code'], item['published_at'], item['title'], item['updated_at'], item['url'], item['website']))
        if len(self.queue) > 3000:
            s = time.time()
            self.insert_datanase()
            print(time.time() - s)
        return item