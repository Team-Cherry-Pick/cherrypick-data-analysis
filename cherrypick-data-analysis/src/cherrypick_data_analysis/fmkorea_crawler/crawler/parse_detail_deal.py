from shared.enum.site import Site
from shared.util.redis_util import save_error_log


def get_next_page(deal_no, soup) :
    try :
        return str(soup.select_one("a#auto_next_button").get("href")).replace("/", "")
    except Exception as e:
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get next page \n {str(e)}")
        return None

def get_deal_user_name(deal_no, soup) :
    try :
        return soup.select_one("a.member_plate").get_text(strip=True)
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get deal user name \n {str(e)}")
        return None

def get_title(deal_no, soup) :
    try :
        return soup.select_one("h1.np_18px > span.np_18px_span").get_text(strip=True)
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get title \n {str(e)}")
        return None

def get_content(deal_no, soup) :
    try :
        return soup.select_one("article").get_text(strip=True)
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get content \n {str(e)}")
        return None

def get_original_price(deal_no, soup) :
    try :
        return soup.find("th", string="가격").find_next_sibling("td").get_text(strip=True)
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get original price \n {str(e)}")
        return None

def get_product_link(deal_no, soup) :
    try :
        return soup.select_one("td div.xe_content a").get("href")
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get product link \n {str(e)}")
        return None

def get_views(deal_no, soup) :
    try :
        info_box = soup.select("div.side.fr b")
        return int(info_box[0].get_text(strip=True))
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : no views \n {str(e)}")
        return None

def get_vote(deal_no, soup) :
    try :
        info_box = soup.select("div.side.fr b")
        return int(info_box[1].get_text(strip=True))
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : no vote \n {str(e)}")
        return None

def get_comment_count(deal_no, soup) :
    try :
        info_box = soup.select("div.side.fr b")
        return int(info_box[2].get_text(strip=True))
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : no comment count \n {str(e)}")
        return None

def get_is_expired(deal_no, soup) :
    try :
        return soup.select_one("div.hotdeal_var8Y_msg") is not None
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : is expired?????? error???????? \n {str(e)}")
        return None

def get_deal_create_at(deal_no, soup) :
    try :
        return soup.select_one("span.date.m_no").get_text(strip=True)
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : no deal 'created at' \n {str(e)}")
        return None
