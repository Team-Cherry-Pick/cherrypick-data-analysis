import bs4

from ppomppu_crawler.parser.comment_parser import parse_comment
from ppomppu_crawler.parser.deal_parser import parse_deal
from shared.process.page_dto import PageDTO
from shared.enum.site import Site


site = Site.PPOMPPU
def parse_ppomppu(no, soup: bs4.BeautifulSoup) :
    deal_dto = parse_deal(no, soup)
    comment_list = parse_comment(no, soup)
    return PageDTO(deal=deal_dto, comments=comment_list)



