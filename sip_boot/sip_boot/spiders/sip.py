import scrapy
from scrapy.spiders import Spider, CrawlSpider, Rule, Request


class SipSpider(Spider):

    name = 'sip'
    allowed_domains = ['www.sipwhiskey.com'],
    start_url = 'https://sipwhiskey.com/collections/japanese-whisky'
    base_url = 'https://sipwhiskey.com/'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse,
                      headers={'User-Agent': self.user_agent},)

    def parse(self, response):
        for item in response.xpath('//div[@class = "block-inner"]'):
            link = item.xpath('.//a/@href').get()
            name = item.xpath('.//div[@class = "title"]/text()').get()
            abs_link = response.urljoin(link)
            yield response.follow(abs_link, callback=self.parse_product_page, meta={'name': name},
                                  headers={'User-Agent': self.user_agent}, dont_filter=True,)

    def parse_product_page(self, response):
        product_name = response.xpath(
            '//*[@id="shopify-section-product-template"]/div/div[2]/div[2]/h1/text()').get()
        product_price = response.xpath(
            '//*[@id="shopify-section-product-template"]/div/div[2]/div[2]/h2/span/text()').get()
        product_brand = response.xpath(
            '//*[@id="shopify-section-product-template"]/div/div[2]/div[2]/div[3]/div/a/text()').get()
        image = response.xpath(
            '//*[@id="shopify-section-product-template"]/div/div[2]/div[1]/div[1]/a/@href').get()

        yield {
            'product_name': product_name,
            'product_price': product_price,
            'product_brand': product_brand,
            'image': image,
        }