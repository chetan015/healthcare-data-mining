import json
import string

from scrapy import Request, Spider, signals


class PatientInfoSpider(Spider):

    name = 'patient_info'
    authors = {}
    replies = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PatientInfoSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        # spider.logger.info(spider.authors)
        with open('authors.json', 'w') as f:
            json.dump(spider.authors, f)

    def start_requests(self):
        url_prefix = 'https://patient.info/forums/index-'
        # Get all medical groups from index pages starting with letter A to Z
        for l in string.ascii_lowercase:
            yield Request(url=url_prefix + l, callback=self.parse_group_list)
            break

    def parse_group_list(self, response):
        # Get all the links from the groups table.
        # Note that this is for groups starting with a particular letter.
        group_links = response.css('.disc-forums.disc-a-z > table a')
        for link in group_links:
            yield response.follow(link, callback=self.parse_post_list)
            break

    def parse_post_list(self, response):
        post = response.css('article.post')
        # Get profiles of all authors for the group.
        author_links = post.css('.post__actions.post__user a::attr(href)').getall()
        # Get all post links for the group.
        post_links = post.css('.post__title > a::attr(href)').getall()

        # Testing
        # author_links = ['https://patient.info/forums/profiles/talos-1069042']
        # post_links = ['https://patient.info/forums/discuss/do-my-turbinates-look-normal--602417']

        for alink, plink in zip(author_links, post_links):
            author_id = alink.split('/')[-1]
            author = self.authors.get(author_id, {})
            if 'discussions' in author:
                next
            yield response.follow(alink + '/discussions',
                                  callback=self.parse_author_discussions,
                                  cb_kwargs=dict(post_link=plink))
            break

        next_link = response.css('a.reply__control').xpath(
            "//span[text()='Next']/parent::a/@href").get()
        if next_link is not None:
            yield response.follow(next_link, callback=self.parse_post_list)

    def parse_author_discussions(self, response, post_link):
        # If discussions tab exists for author, scrape it otherwise directly go to post
        if response.status != 404:
            posts = response.css('#main-body > ol > li')
            author_id = response.url.split('/')[-2]
            author = self.authors.get(author_id, {})
            author['discussions'] = {}
            for post in posts:
                post_id = post.css('h3 > a').attrib['href'].split('-')[-1]
                author['discussions'][post_id] = {
                    'created': post.css('.commented-on > time').attrib['datetime']
                }
            self.authors[author_id] = author
        else:
            self.crawler.stats.inc_value('failed_url_count')

        yield response.follow(post_link + '?order=mostvotes', callback=self.parse_post_replies)

    def parse_post_replies(self, response):
        post_id = response.css('.post__main > .post').attrib['data-d']
        self.replies[post_id] = self.replies.get(post_id, [])

        replies = response.css('ul.comments > li > article.post')
        for r in replies:
            author_id = r.css('.author__name').attrib['href'].split('/')[-1]
            likes = int(r.css('.post__actions > .post__like > .post__count::text').get('0'))
            author = self.authors.get(author_id, {})
            author['replies'] = author.get('replies', {})
            author['replies']['likeCounts'] = author['replies'].get('likeCounts', [])
            author['replies']['likeCounts'].append(likes)
            self.authors[author_id] = author

            self.replies[post_id].append({
                'author': author_id,
                'created': r.css('.post__header time').attrib['datetime'],
                'content': r.css('.moderation-conent').attrib['value'],
                'numLikes': likes
            })

        next_link = response.css('a.reply__control').xpath(
            "//span[text()='Next']/parent::a/@href").get()
        if next_link is not None:
            yield response.follow(next_link, callback=self.parse_post_replies)
        else:
            yield self.parse_post(response)

    def parse_post(self, response):
        post = response.css('.post__main > .post')
        post_content = post.css('#post_content')

        item = {
            'id': post.attrib['data-d'],
            'link': response.url.split('?')[0],
            'group': response.css('header .breadcrumb-item:last-child span::text').get().strip(),
            'heading': post.css('.post__title::text').get(),
            'author': post.css('.author__name').attrib['href'].split('/')[-1],
            'content': ' '.join(post_content.css('p:not(.post__stats)::text').getall()),
        }

        likes, replies = post_content.css('.post__stats').re(r'(\d+) like.?, (\d+) repl')
        item['numReplies'], item['numLikes'] = int(replies), int(likes)

        post_stats = post.css('.post__header+.post__stats')
        item['numFollowing'] = int(post_stats.re(r'(\d+) user.* following')[0])

        item['created'] = post_stats.xpath("//span[contains(text(),'Posted')]/time/@datetime").get()
        if item['created'] is None:
            # If posted time is not available on the post page, try to get it from user's profile
            item['created'] = self.authors[item['author']]['discussions'][item['id']]['created']

        item['replies'] = self.replies[item['id']]
        del self.replies[item['id']]  # clear up some memory

        # print(item)
        return item
