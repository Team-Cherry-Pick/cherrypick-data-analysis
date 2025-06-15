import traceback
from selenium.webdriver.ie.webdriver import WebDriver
from time import sleep
from fmkorea_crawler.crawler.parse_commennts import get_comments
from fmkorea_crawler.crawler.parse_detail_deal import *
from shared.process.page_dto import DealDTO, CommentDTO, PageDTO, UserDTO, get_users
from shared.util.crawl_util import parse_html
from shared.util.global_parse_util import *
from shared.util.redis_util import save_error_log


def parse_fmkorea(driver: WebDriver, deal_no):
    driver.get(Site.FMKOREA.deal_detail_url + str(deal_no) + "?cpage=1")
    sleep(1)
    html = driver.page_source
    soup = parse_html(html)

    users = []
    comments = []
    page = PageDTO(
        deal=None,
        comments=None
    )
    try:
        print(f"FM_KOREA PARSE : {datetime.now()}")
        source_site = Site.FMKOREA

        next_page = get_next_page(deal_no, soup)
        page.next_page = next_page
        username = get_deal_user_name(deal_no, soup)
        title = get_title(deal_no, soup)
        content = get_content(deal_no, soup)

        origin_price = get_original_price(deal_no, soup)
        product_link = get_product_link(deal_no, soup)
        store = get_store(product_link)

        views = get_views(deal_no, soup)
        vote = get_vote(deal_no, soup)
        comment_count = get_comment_count(deal_no, soup)

        is_expired = get_is_expired(deal_no, soup)
        created_at = parse_date_time(get_deal_create_at(deal_no, soup))

        # DEAL
        deal = DealDTO(
            source_site=source_site,
            deal_no=deal_no,
            username=username,
            title=title,
            content=content,
            price_type=get_price_type(Site.FMKOREA, deal_no, origin_price),
            origin_price=str(origin_price),
            discounted_price=extract_price(Site.FMKOREA, origin_price, origin_price),
            vote=vote,
            views=views,
            comment_count=comment_count,
            is_expired=is_expired,
            store=store,
            product_link=product_link,
            created_at=created_at,
            is_blinded=False,
            category_id=None
        )

        #COMMENT
        comments = get_comments(deal_no, driver, soup, comment_count)

        page.deal = deal
        page.comments = comments
        return page

    except Exception as e:
        traceback.print_exc()
        save_error_log(Site.FMKOREA, "GLOBAL PARSING ERROR", f"DEAL_NO {deal_no} : {e}")
        return page



