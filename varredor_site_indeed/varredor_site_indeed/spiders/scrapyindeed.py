# https://br.indeed.com/jobs?q=python&l&from=searchOnHP&vjk=ef1205fc3520566b
import scrapy
from urllib.parse import urlencode

API_KEY = 'c18ece14-5df7-46d9-b027-ccbba19f13da'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class IndeedPythonSpider(scrapy.Spider):
    # identidade
    name = 'vagabot'
    # request

    def start_requests(self):
        urls = [
            'https://br.indeed.com/jobs?q=python&l&from=searchOnHP&vjk=ef1205fc3520566b']
        for url in urls:
            yield scrapy.Request(url=get_proxy_url(url), callback=self.parse)
    # response

    def parse(self, response):
        # varrer cada grupo de informação e seus detalhes
        for item in response.xpath("//td[@class='resultContent']"):
            yield {
                'cargo': item.xpath(".//span[1]/text()").get(),
                'nome empresa': item.xpath(".//span[@class='companyName']/text()").get(),
                'local': item.xpath(".//div[@class='companyLocation']/span/text()").get(),
                'link': 'https://br.indeed.com' + item.xpath(".//a/@href").get()
            }
        try:
            link_proxima_pagina = response.xpath(
                "//a[@aria-label='Próxima']/@href").get()
            if link_proxima_pagina is not None:
                link_proxima_pagina_completo = 'https://br.indeed.com' + link_proxima_pagina
                yield scrapy.Request(get_proxy_url(link_proxima_pagina_completo), callback=self.parse)
        except:
            print('CHEGAMOS NA ÚLTIMA PÁGINA')