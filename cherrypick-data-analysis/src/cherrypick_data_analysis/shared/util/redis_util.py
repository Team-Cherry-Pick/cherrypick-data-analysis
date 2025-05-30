import json
from datetime import datetime

from redis import RedisError

from cherrypick_data_analysis.shared.config.redis import get_redis_client
from cherrypick_data_analysis.shared.enum.crawler_status import Status, DataKey
from cherrypick_data_analysis.shared.enum.site import Site


def set_crawler_status(site:Site, status:Status):
    try :
        r = get_redis_client()
        r.set(f"CRAWLER:{site.name}:STATUS", status.name)
    except RedisError as e:
        print(f"redis set error: {e}")
        return None


def get_crawler_status(site:Site):
    try:
        r = get_redis_client()
        value = str(r.get(f"CRAWLER:{site.name}:STATUS"))
        return Status(value)
    except RedisError as e:
        print(f"redis get error: {e}")
        return ""

def set_crawler_data(site:Site, data:DataKey, value)->bool:
    try :
        r = get_redis_client()
        r.hset(f"CRAWLER:{site.name}:DATA", data.name, str(value))
        return True
    except Exception as e:
        print(f"redis hset error: {e}")
        return False


def get_crawler_data(site:Site, data:DataKey):
    try :
        r = get_redis_client()
        value = str(r.hget(f"CRAWLER:{site.name}:DATA", data.name))
        #print(value)
        return value
    except Exception as e:
        print(f"redis hget error: {e}")
        return ""

def calculate_average_duration(site:Site) -> float:
    from datetime import datetime
    total_time = (datetime.now() - datetime.strptime(get_crawler_data(site, DataKey.START_TIME), "%Y-%m-%d %H:%M:%S")).total_seconds()
    total_count = int(get_crawler_data(site, DataKey.TOTAL_COUNT))
    if total_count > 0: return total_time / total_count
    else: return 0

def initialize_redis(site:Site):
    set_crawler_status(site, Status.RUNNING)
    set_crawler_data(site, DataKey.START_TIME, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    set_crawler_data(site, DataKey.TOTAL_COUNT, 0)
    set_crawler_data(site, DataKey.FAILURE_COUNT, 0)
    set_crawler_data(site, DataKey.QUEUED_COUNT, 0)
    set_crawler_data(site, DataKey.AVERAGE_DURATION, 0)
    if get_crawler_data(site, DataKey.NOW_CRAWLING) == "None" :
        set_crawler_data(site, DataKey.NOW_CRAWLING, 2)
    set_crawler_data(site, DataKey.LAST_SAVED_TIME, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if get_crawler_data(site, DataKey.DELAY_TIME) == "None" :
        set_crawler_data(site, DataKey.DELAY_TIME, 3)

    try :
        r = get_redis_client()
        r.delete(f"CRAWLER:{site.name}:ERRORS")
        save_error_log(site, "INITIALIZE", "INITIALIZE STREAMS")

    except Exception as e:
        print(f"redis STREAMS error: {e}")


def save_error_log(site:Site, error, message) :
    try :
        r = get_redis_client()
        print(f"error: {error}, message: {message}", flush=True)
        r.xadd(f"CRAWLER:{site.name}:ERRORS", {"error": str(error), "message": str(message)})
    except RedisError as e:
        print(f"redis log save error: {e}")

def get_start_page(site:Site) :
    return int(get_crawler_data(site, DataKey.NOW_CRAWLING))