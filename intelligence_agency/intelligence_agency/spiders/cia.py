import scrapy

# links = xpath('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()
# title = xpath('//h1[@class="documentFirstHeading"]/text()').get()
# paragraph =  xpath('//div[@class="field-item even"]//p[not(@class)]/text()').getall()


class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/library/readingroom/historical-collections']

    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_desclassified = response.xpath(
            '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()
        for link in links_desclassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})
            # urljoin allow us to join the secondary link got by the scraper with the main link

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(
            '//h1[@class="documentFirstHeading"]/text()').get()
        paragraph = response.xpath(
            '//div[@class="field-item even"]//p[not(@class)]/text()').getall()  # you can send the list of paragraphs or just the first

        if len(paragraph[0]) > 30:
            paragraph = paragraph[0]
        else:
            paragraph = paragraph[1]

        yield {
            'url': link,
            'title': title,
            'body': paragraph
        }
