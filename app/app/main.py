import prometheus_client
from fastapi.openapi.models import Response
from prometheus_client import Summary
from prometheus_client import Summary, Counter, Histogram, Gauge
from starlette.responses import PlainTextResponse

from fastapi import FastAPI, Request
import random
import time

from starlette.responses import JSONResponse

app = FastAPI()
REQUEST_TIME=Summary('request_processing_seconds', 'Time spent processing request')
_INF = float("inf")
graphs = {}
graphs['c'] = Counter('test_of_counter', 'Description of counter')
graphs['h'] = Histogram('test_of_histogram', 'Description of histogram', buckets=(1, 5, 10, 50, 100, 200, 500, _INF))
graphs['g'] = Gauge('test_of_gauge', 'Description of gauge')
graphs['s'] = Summary('test_of_summary', 'Description of summary')

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/update/count")
def update_count():
    graphs['c'].inc()
    return requests_count()
@app.get("/update/summary")
def update_count():
    graphs['s'].observe(4.7)
    return requests_count()

@app.get("/update/histogram")
def update_histogram(request: Request):

    k = float(request.query_params['search'])
    graphs['h'].observe(k)
    return requests_count()

@app.get("/update/gauge")
def update_gauge(request: Request):

    k = request.query_params['search']
    graphs['g'].set(k)
    return requests_count()




@app.get("/metrics")
def requests_count():
  res = [prometheus_client.generate_latest(graphs['c']),prometheus_client.generate_latest(graphs['s']), prometheus_client.generate_latest(graphs['h']), prometheus_client.generate_latest(graphs['g'])]
  str=""


  str+=res[0].decode("utf-8")+'\n'
  str += res[1].decode("utf-8") + '\n'
  str += res[2].decode("utf-8") + '\n'
  str += res[3].decode("utf-8")


  return PlainTextResponse(prometheus_client.generate_latest())
