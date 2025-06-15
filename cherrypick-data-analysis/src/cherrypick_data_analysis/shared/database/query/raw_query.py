from cherrypick_data_analysis.shared.database.database import get_session
from cherrypick_data_analysis.shared.database.model.raw_page import RawPage
from cherrypick_data_analysis.shared.enum.site import Site


def get_all_page_no(page_no_set, site : Site) :
    session = get_session()
    page_no_list = session.query(RawPage.page_no).filter(RawPage.page_no.in_(page_no_set), RawPage.source_site == site.name).all()
    session.close()

    return {str(d[0]) for d in page_no_list}

def get_all_raw_pages(site : Site) -> dict:
    session = get_session()
    page_list = session.query(RawPage.page_no, RawPage.raw_html).filter(RawPage.source_site == site.name).all()
    session.close()
    return {d[0]:d[1] for d in page_list}


def get_created_at(deal_no:int, site : Site):
    session = get_session()
    created_at = session.query(RawPage.created_at).filter(RawPage.page_no == deal_no, RawPage.source_site == site.name).first()
    session.close()
    return created_at[0]