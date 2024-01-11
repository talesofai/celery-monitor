
from fastapi import APIRouter, Request, HTTPException
from celery import Celery
from celery.app.control import Inspect
from collections import defaultdict
import pydantic
from typing import Dict

from global_config import global_config

DEFAULT_CELERY_BROKER_URL = "redis://:Talesofai123!@r-rj91bdythkt2uwm3tupd.redis.rds.aliyuncs.com:6379/10"

api_router = APIRouter()


class CeleryMetrics(pydantic.BaseModel):
    all_workers_num: int
    active_tasks_num: int
    vacancy_rate: float
    queue_stats: Dict = {}

@api_router.get("/celery-metrics")
def celery_metrics():
    celery_broker_url = global_config.get_env('CELERY_BROKER_URL', DEFAULT_CELERY_BROKER_URL)
    if not celery_broker_url:
        message = "environmental variable CELERY_BROKER_URL does not exist"
        raise HTTPException(status_code=500, detail=message)
    app = Celery(broker=celery_broker_url)
    i = Inspect(app=app)

    active_tasks_num = 0
    queue_stats = defaultdict(int)
    
    dict1 = i.active()
    dict1 = dict1 if dict1 else {}
    all_workers_num = len(dict1)
    for key in dict1:
            active_tasks_num += len(dict1[key])

    for worker, tasks in dict1.items():
            for task in tasks:
                queue = task.get('delivery_info', {}).get('routing_key')
                if queue:
                    queue_stats[queue] += 1

    if all_workers_num == 0:
        vacancy_rate = 0
    else:
        vacancy_rate = round((1-active_tasks_num/all_workers_num)*100, 2)

    return CeleryMetrics(all_workers_num=all_workers_num,
                         active_tasks_num=active_tasks_num,
                         vacancy_rate=vacancy_rate,
                         queue_stats = dict(queue_stats)
                         )
