import enum

class Site(enum.Enum):

    def __new__(cls, site_name, deal_detail_url):
        obj = object.__new__(cls)
        obj._value_ = (site_name, deal_detail_url)
        obj.site_name = site_name
        obj.deal_detail_url = deal_detail_url
        return obj

    FMKOREA = ("FMKOREA", "https://www.fmkorea.com//")
    PPOMPPU = ("PPOMPPU", "https://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&no=")