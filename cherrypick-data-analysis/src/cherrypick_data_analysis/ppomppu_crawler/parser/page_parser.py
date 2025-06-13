import bs4

from ppomppu_crawler.parser.comment_parser import parse_comment
from ppomppu_crawler.parser.deal_parser import parse_deal
from shared.process.page_dto import get_users, PageDTO
from shared.enum.site import Site


site = Site.PPOMPPU
def parse_ppomppu(no, soup: bs4.BeautifulSoup) :
    deal_dto = parse_deal(no, soup)
    comment_list = parse_comment(no, soup)
    user_list = get_users(site, deal_dto, comment_list)
    return PageDTO(deal=deal_dto, comments=comment_list, users=user_list, next_page=1)



