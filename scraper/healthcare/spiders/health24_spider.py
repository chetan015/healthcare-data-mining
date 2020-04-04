import json
import re
import string

from scrapy import Request, Spider, signals


class Health24Spider(Spider):

    name = 'health24'
    page_size = 50  # number of pages to request while making post list request
    group_renames = {
        'GynaeDoc': 'Women Health',
        'Hearing management': 'Ear Health',
        'The Dietitians': 'Healthy Eating',
        'Fertility expert': 'Fertility',
        'Anti-ageing expert': 'Dermatology',
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Health24Spider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)

    def start_requests(self):
        start_url = 'https://www.health24.com/Experts/All'
        yield Request(url=start_url, callback=self.parse_expert_list)

    def parse_expert_list(self, response):
        expert_links = response.xpath(
            "//*[contains(@class, 'span8')]/li/a[contains(@href, 'Experts/Expert')]")
        for a in expert_links:
            yield response.follow(a, callback=self.parse_expert)
            break

    def parse_expert(self, response):
        group_name = response.css('#lnkCategoryHeading::text').get()
        galias = response.css('.subcat_header > h1::text').get()
        if group_name is None:
            if galias in self.group_renames:
                print(group_name, '#', galias, '#', self.group_renames.get(galias))
                group_name = self.group_renames.get(galias)
            else:
                print('########################', group_name, '#', galias)
                return
        else:
            print(group_name, '#', galias, '#', self.group_renames.get(group_name, group_name))
            group_name = self.group_renames.get(group_name, group_name)

        expert_id = response.css('#expertType').attrib['value']
        # This will return a JSON
        posts_url = f'https://www.health24.com/Services/HealthService.svc/GetExpertQuestionListing?expertID={expert_id}&pageSize={self.page_size}&pageNo=1'
        yield response.follow(posts_url,
                              callback=self.parse_post_list,
                              cb_kwargs=dict(group_name=group_name))

    def parse_post_list(self, response, group_name):
        # {
        #     "CanLoadMore": false,
        #     "ResultCount": 0,
        #     "Results": [{
        #         "CommentCount": 0,
        #         "Expert": "",
        #         "ExpertUrl": "",
        #         "Group": "",
        #         "IsAnswered": true,
        #         "PostedOn": "20/03/2016",
        #         "QuestionTextShort": "",
        #         "QuestionUrl": "https://www.health24.com/Medical/Asthma/Experts/Question/Is-asthma-a-curable-dearest-20160320",
        #         "Title": "Is asthma curable?"
        #     }]
        # }
        data = json.loads(response.text)
        for p in data['Results']:
            yield response.follow(p['QuestionUrl'],
                                  callback=self.parse_post,
                                  cb_kwargs=dict(group_name=group_name))

        # Pagination
        # if data['CanLoadMore']:
        #     page = int(re.search(r'&pageNo=(\d+)', response.url).group(1))
        #     next_url = re.sub(r'&pageNo=(\d+)', f'&pageNo={page+1}', response.url)
        #     yield response.follow(next_url,
        #                           callback=self.parse_post_list,
        #                           cb_kwargs=dict(group_name=group_name))

    def parse_post(self, response, group_name):
        post = response.css('.focus_block_experts > .expert_content')
        # ? in regex avoid matching trailing spaces greedily in author name
        author, posted = post.css('h6:last-of-type::text').re(r'Posted by:\s(.*?)\s*\|\s(.*)\s*')
        item = {
            'link': response.url,
            'group': group_name,
            'author': author if author else 'guest',  # if author was empty
            'created': posted,
            'heading': post.css('h2:last-of-type::text').get(),
            'content': ' '.join(post.css('p::text').getall()),
        }

        expert_reply = response.css('#expertAnswer')
        if expert_reply:
            item['replies'] = [{
                'author': expert_reply.css('#lnkExpert::text').get(),
                # ignore leading extra chars
                'created': expert_reply.css('.datestamp::text').get()[-10:],
                'content': ' '.join(expert_reply.css('hgroup+p::text').getall()),
            }]

        yield item
