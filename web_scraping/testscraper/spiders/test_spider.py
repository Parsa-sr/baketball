import scrapy

class testspider(scrapy.Spider):
    name = 'testspider'
    start_urls = ['https://www.basketball-reference.com/leagues/']
    def parse(self, response):

        links = response.css('th a::attr(href)').getall()
        for link in links:
            year = link.split('_')[-1].replace('.html', '')
            link = 'https://www.basketball-reference.com' + link
            print(link)
            if 2015 <=int(year)<=2025:

                yield response.follow(link, callback = self.parse_teams,meta={'year': year})

    # now we are in each seasn 

    def parse_teams(self, response):
        team_links = response.css('table#totals-team td[data-stat="team"] a::attr(href)').getall()
        year = response.meta['year']
        for team_link in team_links:

            # yield{
            #     'team_link': team_link
            #     'season ': year
            # }

            yield response.follow(team_link, callback = self.parse_player, meta={'year': year,'team_link':team_link})

    def parse_player(self,response):
        year = response.meta['year']
        team_link = response.meta['team_link']
        rows = response.css('table#roster tbody tr')
        if not rows:
            for c in response,xpath('/comment()/').getall():
                sel = selector(text=c)
                rows= sel.css('table#roster tbody tr')
                if rows: break

        for row in response.css('table#roster tbody tr'):

            yield {
                'season':year,
                'team_page': team_link,
                'player_link': response.css('td[data-stat="player"] a::attr(href)').get(),
                'playername': response.css('td[data-stat="player"] a::text').get(),
                'birth': response.css('td span::text').get(),
                'pos': response.css('td.center::text').get(),
                'ht': response.css('td[data-stat="height"]::text').get(),
                'wt': response.css('td[data-stat="weight"]::text').get(),
                'experience' : response.css('td[data-stat="years_experience"]::text').get()
            }




