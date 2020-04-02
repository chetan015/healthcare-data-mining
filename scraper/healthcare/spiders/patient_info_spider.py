import scrapy
import string


class PatientInfoSpider(scrapy.Spider):

    name = 'patient_info'
    authors = {}

    def start_requests(self):
        url_prefix = 'https://patient.info/forums/index-'
        # Get all medical groups from index pages starting with letter A to Z
        for l in string.ascii_lowercase:
            yield scrapy.Request(url=url_prefix + l, callback=self.parse_group_list)
            break

    def parse_group_list(self, response):
        # Get all the links from the groups table.
        # Note that this is for groups starting with a particular letter.
        group_links = response.css('.disc-forums.disc-a-z > table a')
        for link in group_links:
            yield response.follow(link, callback=self.parse_post_list)
            break

    def parse_post_list(self, response):
        post = response.css('article.post.item')
        # Get profiles of all authors for the group.
        author_links = post.css('.post__actions.post__user a::attr(href)').getall()
        # Get all post links for the group.
        post_links = post.css('.post__title > a')
        for alink, plink in zip(author_links, post_links):
            author_id = alink.split('/')[-1]
            author = self.authors.get(author_id, {})
            if 'discussions' in author:
                next
            yield response.follow(alink + '/discussions',
                                  callback=self.parse_author_discussions,
                                  cb_kwargs=dict(post_link=plink))
            break

    def parse_author_discussions(self, response, post_link):
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
        yield response.follow(post_link, callback=self.parse_post)

    def parse_post(self, response):
        post = response.css('.post__main > .post')
        post_content = post.css('#post_content')

        item = {
            'id': post.attrib['data-d'],
            'link': response.url,
            'heading': post.css('.post__title::text').get(),
            'author': post.css('.author__name').attrib['href'].split('/')[-1],
            'content': ' '.join(post_content.css('p:not(.post__stats)::text').getall()),
        }

        # Since the time shown on item page is the time of last reply, we are getting the time
        # of creation from the author's profile
        item['created'] = self.authors[item['author']]['discussions'][item['id']]['created']

        likes, replies = post_content.css('.post__stats').re(r'(\d+) like.?, (\d+) repl')
        item['replies'], item['likes'] = int(replies), int(likes)
        item['following'] = post.css('.post__header+.post__stats > span:last-child').re(
            r'(\d+) user.* following')[0]

        yield item
