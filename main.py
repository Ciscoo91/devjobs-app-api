import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv

from model.model import RequestParams

load_dotenv()

app = FastAPI()


origins = [
    "https://devjobs-app-api.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET', 'POST'],
    allow_headers=["*"]
)

client = SearchClient.create(
    os.environ["ALGOLIA_APP_ID"], os.environ["ALGOLIA_SEARCH_API_KEY"])
index = client.init_index(os.environ["ALGOLIA_INDEX_NAME"])


@app.get('/')
def get_jobs():

    try:
        results = index.search("")
        return results["hits"]
    except Exception as e:
        print("Algolia search error: ", str(e))
        return JSONResponse(content={"error": "An error occured during search"}, status_code=500)


@app.post("/query")
def search_by_query_params(req: RequestParams):

    try:
        results = None
        search = f"{req.filter} {req.location}"
        if req.fulltime == None:
            results = index.search(search)
        else:
            facet = f"contract:'{req.fulltime}'"
            query_params = {
                "filters": facet
            }
            results = index.search(search, query_params)

        if results["nbHits"] == 0:
            return JSONResponse(content={"not found": "No job post found"}, status_code=404)

        return results["hits"]

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"An error occurred during search: {e}"})


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    try:
        result = index.find_object(lambda hit: hit.get('id') == job_id)
        return result
    except Exception as e:
        print('Algolia search error: ', str(e))
        return JSONResponse(content={"error": "Job item not found"}, status_code=404)
