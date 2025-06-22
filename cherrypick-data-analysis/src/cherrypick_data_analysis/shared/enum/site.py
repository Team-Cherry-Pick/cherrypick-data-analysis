import enum

class Site(enum.Enum):
# color_code = https://colorhunt.co/palette/309898ff9f00f4631ecb0404
    def __new__(cls, site_name, deal_detail_url, deal_list_url, color):
        obj = object.__new__(cls)
        obj._value_ = (site_name, deal_detail_url)
        obj.site_name = site_name
        obj.deal_detail_url = deal_detail_url
        obj.deal_list_url = deal_list_url
        obj.color = color
        return obj

    FMKOREA = ("FMKOREA", "https://www.fmkorea.com//", "https://www.fmkorea.com/index.php?mid=hotdeal&page=", "#309898")
    PPOMPPU = ("PPOMPPU", "https://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&no=", "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page=", "#FF9F00")