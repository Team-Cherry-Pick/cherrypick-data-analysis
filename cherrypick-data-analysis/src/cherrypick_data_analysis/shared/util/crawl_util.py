from bs4 import BeautifulSoup
from shared.process.page_dto import DealDTO
import undetected_chromedriver as uc

def get_driver(headed=False):
    options = uc.ChromeOptions()
    if not headed : options.add_argument('--headless')  # 필요하면 제거
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--lang=ko-KR')
    options.add_argument("-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/114.0.0.0 Safari/537.36")

    driver = uc.Chrome(
        options=options,
        use_subprocess=True,
        driver_executable_path='/usr/bin/chromedriver'  # 이거 꼭 추가!
    )

    return driver


def parse_html(content) :
    return BeautifulSoup(content, 'html.parser')

def print_deal_dto(dto: DealDTO):
    print("┌───────────── DealDTO ─────────────┐")
    print(f"│ site           : {dto.source_site}")
    print(f"│ deal_no        : {dto.deal_no}")
    print(f"│ name       : {dto.name}")
    print(f"│ title          : {dto.title}")
    print(f"│ content        : {dto.content[:80]}." if dto.content else "│ content        : None")
    print(f"│ product_link   : {dto.product_link}")
    print(f"│ store          : {dto.store}")
    print(f"│ vote           : {dto.vote}")
    print(f"│ views          : {dto.views}")
    print(f"│ origin_price   : {dto.origin_price}")
    print(f"│ discounted_price: {dto.discounted_price}")
    print(f"│ created_at     : {dto.created_at}")
    print("└────────────────────────────────────┘")


def print_comment_dto(comment):
    print("┌───────────── CommentDTO ─────────────┐")
    print(f"│ name     : {comment.name}")
    print(f"│ created_at   : {comment.created_at}")
    print(f"│ upvote       : {comment.upvote}")
    print(f"│ downvote     : {comment.downvote}")
    print(f"│ content      : {comment.content[:80]}{'...' if len(comment.content) > 80 else ''}")
    print("└──────────────────────────────────────┘")

