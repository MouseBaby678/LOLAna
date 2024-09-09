import scrapy

from opggSpider.items import OpggspiderItem


class OpggSpider(scrapy.Spider):
    name = "opgg"
    allowed_domains = ["op.gg"]
    start_urls = ["https://www.op.gg/champions"]

    def parse(self, response):
        tr_list = response.xpath('//*[@id="content-container"]/div[2]/main/div/table/tbody/tr')
        for tr in tr_list:
            item = OpggspiderItem()
            item['hero'] = tr.xpath('./td[2]/a/strong/text()').extract_first()
            item['tier'] = tr.xpath('./td[3]/text()').extract_first()
            item['role'] = tr.xpath('./td[4]/img/@alt').extract_first()
            item['win'] = tr.xpath('./td[5]/text()[1]').extract_first()
            item['pick'] = tr.xpath('./td[6]/text()[1]').extract_first()
            item['ban'] = tr.xpath('./td[7]/text()[1]').extract_first()
            print(item)
        pass
