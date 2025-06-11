import bs4

from ppomppu_crawler.parser.page_parser import parse_deal
from shared.util.crawl_util import print_deal_dto
from shared.enum.site import Site
from time import sleep
site = Site.PPOMPPU

def parse_ppomppu(no, soup: bs4.BeautifulSoup) :
    deal_dto = parse_deal(no, soup)
    print_deal_dto(deal_dto)
    sleep(5)




