import json
import pickle
import traceback
from datetime import datetime
from redis import RedisError
from cherrypick_data_analysis.shared.config.redis import get_redis_client, get_redis_client_not_decode
from cherrypick_data_analysis.shared.enum.crawler_status import Status, DataKey
from cherrypick_data_analysis.shared.enum.site import Site
from cherrypick_data_analysis.shared.enum.cachekey import CacheKey
from cherrypick_data_analysis.shared.database.query.deal_query import get_all_deals_dataframe, get_deal_count
from cherrypick_data_analysis.shared.database.query.comment_query import get_comment_count
from cherrypick_data_analysis.shared.database.query.comment_query import get_all_comment_dataframe


def set_crawler_status(site:Site, status:Status):
    r = get_redis_client()
    try :
        r.set(f"CRAWLER:{site.name}:STATUS", status.name)
    except RedisError as e:
        print(f"redis set error: {e}")
        return None
    finally:
        r.close()


def get_crawler_status(site:Site):
    r = get_redis_client()
    try:
        value = str(r.get(f"CRAWLER:{site.name}:STATUS"))
        return Status(value)
    except RedisError as e:
        print(f"redis get error: {e}")
        return ""
    finally:
        r.close()

def set_crawler_data(site:Site, data:DataKey, value)->bool:
    r = get_redis_client()
    try :
        r.hset(f"CRAWLER:{site.name}:DATA", data.name, str(value))
        return True
    except Exception as e:
        print(f"redis hset error: {e}")
        return False
    finally:
        r.close()


def get_crawler_data(site:Site, data:DataKey):
    r = get_redis_client()
    try :
        value = str(r.hget(f"CRAWLER:{site.name}:DATA", data.name))
        #print(value)
        return value
    except Exception as e:
        print(f"redis hget error: {e}")
        return ""
    finally:
        r.close()

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
    finally:
        r.close()


def save_error_log(site:Site, error, message) :
    r = get_redis_client()
    try :
        print(f"error: {error}, message: {message}", flush=True)
        r.xadd(f"CRAWLER:{site.name}:ERRORS", {"error": str(error), "message": str(message)})
    except RedisError as e:
        print(f"redis log save error: {e}")
    finally:
        r.close()

def get_error_logs(site:Site) :
    r = get_redis_client()
    try :
        logs = r.xrevrange(f"CRAWLER:{site.name}:ERRORS", count=30)
        return logs
    except RedisError as e:
        print(f"redis log get error: {e}")
    finally:
        r.close()



def get_start_page(site:Site) :
    return int(get_crawler_data(site, DataKey.NOW_CRAWLING))

def set_cache(key : CacheKey, value) :
    r = get_redis_client_not_decode()
    try :
        r.set(key.value, pickle.dumps(value))
        r.close()
    except RedisError as e:
        print(f"redis cache set error: {e}")
        return None
    finally:
        r.close()


def get_cache(key: CacheKey):
    r = get_redis_client_not_decode()
    try:
        raw = r.get(key.value)
        if raw is None:
            return None
        result = pickle.loads(raw)
        return result
    except Exception as e:
        print(f"[RedisCacheError] {e}")
        return None
    finally:
        r.close()


def cache_init() :
    deals = get_all_deals_dataframe()
    deal_count = get_deal_count()
    comment_count = get_comment_count()
    set_cache(CacheKey.DEAL_ALL, deals)
    set_cache(CacheKey.SITE_DEAL_COUNT, deal_count)
    set_cache(CacheKey.SITE_COMMENT_COUNT, comment_count)

def get_memo_list(key:str) -> list:
    r = get_redis_client_not_decode()
    try :
         memo_list = r.lrange(f"SERVE:MEMO:{key}", 0 ,-1)
         memo_list = [pickle.loads(raw) for raw in memo_list]
         memo_list.reverse()
         return memo_list
    except Exception as e:
        print(f"redis cache get error: {e}")
        return []
    finally:
        r.close()

def push_memo(key, memo) :
    r = get_redis_client_not_decode()
    try :
        r.lpush(f"SERVE:MEMO:{key}", pickle.dumps(memo))
    except RedisError as e:
        print(f"redis cache get error: {e}")
    finally:
        r.close()