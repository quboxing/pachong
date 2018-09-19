# -*- coding: utf-8 -*-
import re

import scrapy
import json

from zhihu.items import ZhihuItem




class ZhSpider(scrapy.Spider):
    name = 'zh'
    allowed_domains = ["www.zhihu.com"]
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    start_user = 'sizhuren'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield scrapy.Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)
        yield scrapy.Request(self.follows_url.format(user=self.start_user, include=self.follows_query, limit=20, offset=0),
                      self.parse_follows)
        yield scrapy.Request(self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),
                      self.parse_followers)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuItem()
        # print('打印开始')
        # print(result)
        item['name'] = ''.join(result.get('name'))
        # print('名字:',name)
        educations = str(result.get('educations'))

        item['school_name'] = ''.join(re.findall("school': {.*?name': '(.*?)'",educations))
        # print('学校名称:',school_name)
        item['school_introduction'] = ''.join(re.findall("school': {.*?introduction': '(.*?)'",educations))
        # print('学校介绍:',school_introduction)
        item['major_name'] = ''.join(re.findall("major': {.*?name': '(.*?)'",educations))
        # print('主修名称:',major_name)
        item['major_introduction'] = ''.join(re.findall("major': {.*?introduction': '(.*?)'",educations))
        # print('主修介绍:',major_introduction)
        employments = str(result.get('employments'))

        item['job_name'] = ''.join(re.findall("job': {.*?name': '(.*?)'",employments))
        # print('工作名称:',job_name)
        item['job_introduction'] = ''.join(re.findall("job': {.*?introduction': '(.*?)'",employments))
        # print('工作介绍:',job_introduction)
        item['company_name'] = ''.join(re.findall("company': {.*?name': '(.*?)'",employments))
        # print('公司名称:',company_name)
        item['company_introduction'] = ''.join(re.findall("company': {.*?introduction': '(.*?)'",employments))
        # print('公司介绍:',company_introduction)

        business = str(result.get('business'))

        item['business_name'] = ''.join(re.findall("name': '(.*?)'",business))
        # print('商业名称:',business_name)
        item['business_introduction'] = ''.join(re.findall("introduction': '(.*?)'",business))
        # print('商业介绍:',business_introduction)
        locations = str(result.get('locations'))
        item['locations_name'] = ''.join(re.findall("name': '(.*?)'",locations))
        # print('住址名称:',locations_name)
        item['locations_introduction'] = ''.join(re.findall("introduction': \"(.*?)\"",locations))
        # print('住址介绍:',locations_introduction)
        # print('打印结束')
        yield item


        yield scrapy.Request(
            self.follows_url.format(user=result.get('url_token'), include=self.follows_query, limit=20, offset=0),
            self.parse_follows)

        yield scrapy.Request(
            self.followers_url.format(user=result.get('url_token'), include=self.followers_query, limit=20, offset=0),
            self.parse_followers)

    def parse_follows(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page,
                          self.parse_follows)

    def parse_followers(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page,
                          self.parse_followers)

