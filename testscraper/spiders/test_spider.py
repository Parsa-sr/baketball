import scrapy


class testspider(scrapy.Spider):
    name = 'testspider'
    start_urls = ['https://www.basketball-reference.com/leagues/']
    

    def parse(self, response):
        self.logger.info(f"Fetched URL: {response.url}")
        for match in response.xpath('//td[@data-stat="mvp"]'):
            yield {
                'name': match.css('a::text').get(),
                'link': match.css('a::attr(href)').get(),
                }
            
        

    