
import scrapy
from scrapy import Spider

from scrapy import Request


class WorldospiderSpider(Spider):
    name = 'worldospider'
    allowed_domains = ['www.worldometers.info', ]
    start_urls = 'https://www.worldometers.info/coronavirus'
    header = {'User_Agent': ' Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' }

    # This Function will Create Request to given url
    def start_requests(self):
        yield Request(url=self.start_urls, callback=self.parse,
                      headers=self.header,)

    # This function extract the data from the requested page and page is home page
    def parse(self, response):
        for anchor in response.xpath('//td/a'):
            name = anchor.xpath('.//text()').get()
            link = anchor.xpath('.//@href').get()
            absolute_link = response.urljoin(link)
            yield response.follow(link, callback=self.page2_parser, meta={'name': name})

    # This function extract the links from  another page
    def page2_parser(self, response):
        name = response.request.meta['name']
        total_cases: str = response.xpath(
            "(//div[@class = 'maincounter-number'])[1]/span/text()").get()
        total_deaths = response.xpath(
            "(//div[@class = 'maincounter-number'])[2]/span/text()").get()
        recovered = response.xpath(
            "(//div[@class = 'maincounter-number'])[3]/span/text()").get()
        yield {
            'country_name': name,
            'total_case': total_cases,
            'total_deaths': total_deaths,
            'recovered_cases': recovered
        }
