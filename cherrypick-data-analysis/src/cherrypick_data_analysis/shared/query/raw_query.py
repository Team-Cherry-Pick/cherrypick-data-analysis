from cherrypick_data_analysis.shared.database.database import get_session
from cherrypick_data_analysis.shared.database.model.raw_page import RawPage
from cherrypick_data_analysis.shared.enum.site import Site


def get_all_page_no(page_no_set, site : Site) :
    session = get_session()
    page_no_list = (session
                    .query(RawPage.page_id)
                    .filter(RawPage.page_no.in_(page_no_set), RawPage.source_site == site.name)
                    .all())
    session.close()

    return {d[0] for d in page_no_list}