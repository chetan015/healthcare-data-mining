import json
import re
import string

from scrapy import Request, Spider, signals


class Health24Spider(Spider):

    name = 'health24'
    page_size = 100  # number of pages to request while making post list request
    group_renames = {
        'GynaeDoc': 'Women Health',
        'Hearing management': 'Ear Health',
        'The Dietitians': 'Healthy Eating',
        'Fertility expert': 'Fertility',
        'Anti-ageing expert': 'Dermatology',
    }
    experts = None

    def start_requests(self):
        yield Request(url='https://www.health24.com/Experts/All', callback=self.parse_expert_list)

    def parse_expert_list(self, response):
        expert_links = response.xpath(
            "//*[contains(@class, 'span8')]/li/a[contains(@href, 'Experts/Expert')]")
        for a in expert_links:
            yield response.follow(a, callback=self.parse_expert)

    def parse_expert(self, response):
        group_name = response.css('#lnkCategoryHeading::text').get()
        group_alias = response.css('.subcat_header > h1::text').get()
        if group_name is None:
            if group_alias in self.group_renames:
                # print(group_name, '#', group_alias, '#', self.group_renames.get(group_alias))
                group_name = self.group_renames.get(group_alias)
            else:
                # CyberDoc, CyberShrink, etc groups do not really fall into any proper category
                # print('IGNORED GROUP', group_name, '#', group_alias)
                return
        else:
            # print(group_name, '#', group_alias, '#', self.group_renames.get(group_name, group_name))
            group_name = self.group_renames.get(group_name, group_name)

        # Get expert_ids of all experts if not already gotten
        # if self.experts is None:
        #     self.experts = {}
        #     for option in response.css('#ddlExperts > option'):
        #         self.experts[option.xpath('text()').get()] = option.attrib['value']
        #     print('###################################### Experts', self.experts)
        # else:
        #     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Experts', self.experts)

        # expert_id = self.experts.get(group_alias, response.css('#expertType').attrib['value'])

        # Following is the only reliable way to get expert_id
        # https://cdn.24.co.za/experts2//29272567-1f8d-4a75-a493-134cbb25a992_L.jpg?updated=2014/01/06 15:55:00
        expert_id = response.css('#imgExpertThumb').attrib['src'].split('/')[5].split('_')[0]
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
        if data['CanLoadMore']:
            page = int(re.search(r'&pageNo=(\d+)', response.url).group(1))
            next_url = re.sub(r'&pageNo=(\d+)', f'&pageNo={page+1}', response.url)
            yield response.follow(next_url,
                                  callback=self.parse_post_list,
                                  cb_kwargs=dict(group_name=group_name))

    def parse_post(self, response, group_name):
        post = response.css('.focus_block_experts > .expert_content')
        # ? in regex avoid matching trailing spaces greedily in author name
        author, posted = post.css('h6:last-of-type::text').re(r'Posted by:\s*(.*?)\s*\|\s*(.*)\s*')
        item = {
            'link': response.url,
            'group': group_name,
            'author': author if author else 'guest',  # if author was empty
            'created': posted.strip()[-10:],
            'heading': post.css('h2:last-of-type').xpath('string()').get(),
            'content': ' '.join(post.css('p::text').getall()),
            'numReplies': 0
        }

        expert_reply = response.css('#expertAnswer')
        if expert_reply:
            created = expert_reply.css('.datestamp::text').get()
            # If it is an old post (before 2012), the expert answer doesn't have timestamp
            # It is present in the expert comment below
            if created is None:
                created = response.css('.user_comments+.expert_content > h6::text').get()
            # If it is still not present, use the original post's time
            if created is None:
                created = item['created']
            reply_selector = '#expertAnswer > p::text, #expertAnswer > div:not(.disclaimer_top)::text'
            item['replies'] = [{
                'author': expert_reply.css('#lnkExpert::text').get(),
                # ignore leading extra chars
                'created': created.strip()[-10:],
                'content': ' '.join(response.css(reply_selector).getall()),
            }]
            item['numReplies'] = 1

        yield item
