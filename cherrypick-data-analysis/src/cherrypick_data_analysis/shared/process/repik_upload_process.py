import queue
from urllib.parse import parse_qs, unquote
from cherrypick_data_analysis.shared.adapter.repik_adapter import request_deal_info, upload_deal


def repik_upload_process(input_q : queue) :

    while True:
        deal = input_q.get().deal
        link = unwrap_link(deal.product_link)

        resp = None
        try :
            resp = request_deal_info(link)
        except Exception as e:
            print(e)
            continue

        is_success = upload_deal(resp)
        if is_success :



def unwrap_link(link: str) -> str:
    from urllib.parse import urlparse
    parsed = urlparse(link)
    query = parse_qs(parsed.query)
    raw_url = query.get("url", [""])[0]
    return unquote(raw_url)
