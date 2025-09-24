import scrapy


class testspider(scrapy.Spider):
    name = 'testspider'
    start_urls = ['https://www.basketball-reference.com/leagues/']
    

    def parse(self, response):
        self.logger.info(f"Fetched URL: {response.url}")
        links = response.css('th a::attr(href)').getall()
        for link in links:
            year = link.split('_')[-1].replace('.html', '')
            if 2015 <=int(year)<=2025:
                yield {
                    'year' : year,
                    'link': response.urljoin(link)

                }
            
        

    