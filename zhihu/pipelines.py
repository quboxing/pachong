# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class ZhihuPipeline(object):
    def open_spider(self, spider):
        print('----------open_spider---------')
        self.db = pymysql.connect(
            host='114.116.90.109',
            port=3306,
            user='root',
            password='ka!Wu306',
            db='zms',
            charset='utf8'
        )
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        print('----------close_spider-------------')
        self.db.close()

    def process_item(self, item, spider):
        # 向数据库写入
        try:
            print('----------item写入数据库的Pipeline----------------')
            self.cursor.execute('insert into zhihu(name,school_name,school_introduction,major_name,major_introduction,job_name,job_introduction,company_name,company_introduction,locations_name,locations_introduction,business_name,business_introduction) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                args=(item['name'],
                                      item['school_name'],
                                      item['school_introduction'],
                                      item['major_name'],
                                      item['major_introduction'],
                                      item['job_name'],
                                      item['job_introduction'],
                                      item['company_name'],
                                      item['company_introduction'],
                                      item['locations_name'],
                                      item['locations_introduction'],
                                      item['business_name'],
                                      item['business_introduction']))
            self.db.commit()
            if self.cursor.rowcount >= 1:
                print(item['name'], '数据写入成功')

            return item
        except:
            pass
