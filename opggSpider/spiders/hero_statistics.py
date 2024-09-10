import scrapy
from opggSpider.items import hero_statisticsItem


class HeroStatisticsSpider(scrapy.Spider):
    name = "hero_statistics"
    allowed_domains = ["op.gg"]
    start_urls = ["https://www.op.gg/statistics/champions"]

    def parse(self, response):
        tr_list = response.xpath('//*[@id="content-container"]/div[2]/table/tbody/tr')
        print(tr_list)
        for tr in tr_list:
            item = hero_statisticsItem()
            item['hero'] = tr.xpath('./td[2]/a/strong/text()').get()
            item['games_played'] = tr.xpath('./td[3]/text()').get()
            item['kda'] = tr.xpath('./td[4]/span/text()[1]').get()
            item['cs'] = tr.xpath('./td[8]/text()').get()
            item['gold'] = tr.xpath('./td[9]/text()').get()
            item['win'] = tr.xpath('./td[5]/div/div[2]/text()[1]').get()
            item['pick'] = tr.xpath('./td[6]/div/div[2]/text()[1]').get()
            item['ban'] = tr.xpath('./td[7]/text()[1]').get()
            item['queue_type'] = 'a'
            item['tier'] = 'b'
            item['region'] = 'c'
            print(item)
            # yield item


