import json
import re
import string
import time

from scrapy import Request, Spider, signals
from scrapy.selector import Selector


class MedHelpSpider(Spider):

    name = 'medhelp'
    headers = {'x-requested-with': 'XMLHttpRequest'}
    authors = {}
    replies = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MedHelpSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        # spider.logger.info(spider.authors)
        with open(self.name + '_authors.json', 'w') as f:
            json.dump(spider.authors, f)

    def clean_response_html(self, html):
        # Clean html of lot of escape chars
        html = html.replace('\\/', '/').replace('\\n', '\n')
        return html.replace('\\"', '"').replace("\\\'", "'")

    def clean_content(self, content):
        # Cleanup <br>s and smart quotes
        content = content.replace('\r<br>', ' ').replace('\n<br>', ' ')
        content = content.replace('’', "'").replace('‘', "'")
        return content.replace('“', '"').replace('”', '"')

    def start_requests(self):
        yield Request(url='https://medhelp.org/forums/list', callback=self.parse_communities_list)

    def parse_communities_list(self, response):
        communities = response.css('#az_forums_list .forums_link > a')

        # TESTING
        # communities = ['https://medhelp.org/forums/Allergy/show/67']
        for a in communities:
            yield response.follow(a, callback=self.parse_post_list_initial)
            break

    # Initial page that you see when you open a community
    def parse_post_list_initial(self, response):
        posts = response.css('.subj_title > a')
        for a in posts:
            yield response.follow(a, callback=self.parse_post_replies)
            break

        next_page = response.css('.vertical_scroll_link::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,
                                  callback=self.parse_post_list_paginated,
                                  headers=self.headers)

    def parse_post_list_paginated(self, response):
        # Extract post list content from the returned JS
        regex = r"""j\('\.subject_list_ctn'\)\.append\("\\n\\n      (<div class=\\"subj_entry\\">.*)\\n\\n"\);"""
        html = re.findall(regex, response.text)
        # The last page won't actually have any content
        if not html:
            return
        posts = Selector(text=self.clean_response_html(html[0])).css('.subj_title > a')
        for a in posts:
            yield response.follow(a, callback=self.parse_post_replies)
            break

        # Extract link for the Next Page
        forum = response.url.split('/')[4]
        regex = r'href=\\"(\/forums\/' + forum + r'\/show\/\d+\.js\?.*page=\d+)\\">Next Page'
        link = re.findall(regex, response.text)
        if link:
            time.sleep(0.1)  # debounce
            yield response.follow(link[0].replace('&amp;', '&'),
                                  callback=self.parse_post_list_paginated,
                                  headers=self.headers)

    def extract_replies_authors(self, reply_divs):
        replies = []
        authors = []
        for r in reply_divs:
            author = r.css('.username > a')
            # author_id = f'{author.css("span > span::text").get()}_{author.attrib["href"].split("/")[-1]}'
            author_id = author.attrib["href"].split("/")[-1]

            content = self.clean_content(r.css('.resp_body').get())
            content = Selector(text=content).css('.resp_body::text').get().strip()

            replies.append({
                'author': author_id,
                'created': r.css('.username > time').attrib['datetime'],
                'content': content
            })

            if author_id not in self.authors:
                authors.append(author[0])

        return replies, authors

    def parse_post_replies(self, response):
        post_id = response.url.split('/')[-1]
        self.replies[post_id] = self.replies.get(post_id, [])

        replies, authors = self.extract_replies_authors(response.css('.mh_vit_resp_ctn'))
        self.replies[post_id] += replies
        for a in authors:
            yield response.follow(a.attrib['href'], callback=self.parse_author)
            break

        next_page = response.css('.vertical_scroll_link::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,
                                  callback=self.parse_post_replies_paginated,
                                  cb_kwargs=dict(main_post_response=response),
                                  headers=self.headers)
        else:
            yield self.parse_post(response)

    def parse_post_replies_paginated(self, response, main_post_response):
        post_id = response.url.split('/')[-1].split('.js')[0]
        self.replies[post_id] = self.replies.get(post_id, [])

        # Extract post list content from the returned JS
        regex = r"""j\('\.post_list_ctn'\)\.append\("\s*(.*<\\/div>\\n)"\);"""
        html = re.findall(regex, response.text)
        reply_divs = Selector(text=self.clean_response_html(html[0])).css('.mh_vit_resp_ctn')

        replies, authors = self.extract_replies_authors(reply_divs)
        self.replies[post_id] += replies
        for a in authors:
            yield response.follow(a, callback=self.parse_author)
            break

        # Extract link for the Next Page of replies
        url_parts = response.url.split('/')
        post_part = url_parts[4] + r'\/' + url_parts[5]
        regex = r'href=\\"(\/posts\/' + post_part + r'\/show\/\d+\.js\?.*page=\d+)\\">Next Page'
        link = re.findall(regex, response.text)
        if link:
            time.sleep(0.1)  # debounce
            yield response.follow(link[0].replace('&amp;', '&'),
                                  callback=self.parse_post_replies_paginated,
                                  cb_kwargs=dict(main_post_response=main_post_response),
                                  headers=self.headers)
        else:
            yield self.parse_post(main_post_response)

    def parse_author(self, response):
        is_doctor = False
        if response.css('.doctor_name').get() is not None:
            is_doctor = True

        if is_doctor:
            author_name = response.css('.user_profile_title::text').get().strip()
        else:
            author_name = response.css('.page_title').re(r"\s*(.*)'s Profile")[0]

        author_id = response.url.split('/')[-1]
        self.authors[author_id] = {
            'author_name': author_name,
            'is_doctor': is_doctor,
            'best_answers': int(response.css('#best_answers_hover>div::text').get('0').strip())
        }

    def parse_post(self, response):
        container = response.css('#post_show_content')
        author = container.css('.username > a')
        # author_id = f'{author.css("span > span::text").get()}_{author.attrib["href"].split("/")[-1]}'
        item = {
            'id': response.url.split('/')[-1],
            'link': response.url,
            'group': response.css('.breadcrumb > a:last-of-type::text').get(),
            'author': author.attrib['href'].split('/')[-1],
            'created': container.css('.username > time').attrib['datetime'],
            'heading': container.css('.subj_title::text').get().strip(),
        }

        # Due to <br>s in the text, we are not able to get the text directly via ::text
        content_div = self.clean_content(container.css('#subject_msg').get())
        # regex = r'<div id="subject_msg" itemprop="text">\s*(.*)\s*<\/div>'
        # item['content'] = re.findall(regex, content_div)[0]
        item['content'] = Selector(text=content_div).css('#subject_msg::text').get().strip()

        item['numReplies'] = int(container.css('span[itemprop="answerCount"]::text').get())
        item['numFollowing'] = int(
            container.css('.desktop_follow_link > a').re(r'Follow\s*-\s*(\d+)')[0])

        item['replies'] = self.replies[item['id']]
        del self.replies[item['id']]  # clear up some memory

        return item
