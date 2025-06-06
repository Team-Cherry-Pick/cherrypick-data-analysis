from shared.util.redis_util import save_error_log
from shared.enum.site import Site

def get_comment_count(soup, no):
    try:
        comment_count = len([tag for tag in soup.find('font', class_='pagelist_han').children if getattr(tag, 'name', None)])
        return comment_count
    except Exception as e:
        save_error_log(Site.PPOMPPU, "COMMENT PARSING ERROR", {"message" : e, "is_blinded" : True if "해당글은 운영자에 의해 블라인드 처리된 글입니다." in soup.text else False, "no" : no})
        return 0