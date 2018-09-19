# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    school_name = scrapy.Field()
    school_introduction = scrapy.Field()
    major_name = scrapy.Field()
    major_introduction = scrapy.Field()
    job_name = scrapy.Field()
    job_introduction = scrapy.Field()
    company_name = scrapy.Field()
    company_introduction = scrapy.Field()
    locations_name = scrapy.Field()
    locations_introduction = scrapy.Field()
    business_name = scrapy.Field()
    business_introduction = scrapy.Field()
