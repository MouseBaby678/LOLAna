import scrapy

from opggSpider.items import loldataItem


class loldataSpider(scrapy.Spider):
    name = "loldata"
    allowed_domains = ["op.gg"]
    tiers = ['iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master', 'grandmaster',
             'challenger']
    start_urls = [f"https://www.op.gg/champions?tier={tier}" for tier in tiers]

    def parse(self, response):
        tr_list = response.xpath('//*[@id="content-container"]/div[2]/main/div/table/tbody/tr')
        for tr in tr_list:
            item = loldataItem()
            item['hero'] = tr.xpath('./td[2]/a/strong/text()').extract_first()
            item['level'] = tr.xpath('./td[3]/text()').extract_first()
            item['role'] = tr.xpath('./td[4]/img/@alt').extract_first()
            item['win'] = tr.xpath('./td[5]/text()[1]').extract_first()
            item['pick'] = tr.xpath('./td[6]/text()[1]').extract_first()
            item['ban'] = tr.xpath('./td[7]/text()[1]').extract_first()
            item['tier'] = response.url.split('=')[-1]
            yield item
