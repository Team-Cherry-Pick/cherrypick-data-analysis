from fmkorea_crawler.fmkorea_total_crawl import get_new_links
from shared.enum.crawler_status import DataKey, Status
from shared.util.crawl_util import get_driver
from shared.util.redis_util import set_crawler_data, set_crawler_status
from shared.util.slack_util import send_slack
from time import sleep

def message_slack_from(text) :
    send_slack(f"[FMKOREA 내구도 테스트] \n {text}")

def test_start(start_page=None):
    print("FMKOREA 내구도 테스트 시작")
    message_slack_from("차단 주기를 알아내겠습니다 😎")

    block_second = 0
    waiting_second = 0
    page = 1
    driver = get_driver()
    while True:
        from shared.enum.site import Site
        set_crawler_data(Site.FMKOREA, DataKey.NOW_CRAWLING, page)
        # 현재 페이지에서 크롤링 해야할 링크 선별
        # 중복 저장 방지
        links = get_new_links(driver, page)
        # 링크 받아오는 과정에서 오류가 나면 None, 이후 break
        if links is None:
            set_crawler_status(Site.FMKOREA, Status.WAITING)
            send_slack(
                f"{Site.FMKOREA.name} 접근이 차단 당했습니다 😭😭😭 \n{start_page - page}p 페이지를 긁었습니다 ! \n 어슬렁 거리다가 다시 잠입하겠습니다...😎")
            sleep(10800)
            send_slack(f"키키키 {Site.FMKOREA.name} 다시 접근해보겠습니다 😃😃😃")
            continue

    print("cancel crawling . . .")
    send_slack(f"{Site.FMKOREA} Crawler 성공적으로 종료했습니다 ! 😎 {start_page - page}p 페이지를 긁었습니다 !\n다음에는 {page}p 부터 시작하면 됩니다 !")
    driver.quit()