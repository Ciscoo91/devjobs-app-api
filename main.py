import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["get"],
    allow_headers=["*"]
)

client = SearchClient.create(
    os.environ["ALGOLIA_APP_ID"], os.environ["ALGOLIA_SEARCH_API_KEY"])
index = client.init_index(os.environ["ALGOLIA_INDEX_NAME"])


@app.get('/')
def get_jobs():

    try:
        results = index.search("blogr")
        return {"jobs": results["hits"]}
    except Exception as e:
        print("Algolia search error: ", str(e))
        return JSONResponse(content={"error": "An error occured during search"}, status_code=500)


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    try:
        result = index.find_object(lambda hit: hit.get('id') == job_id)
        return result
    except Exception as e:
        print('Algolia search error: ', str(e))
        return JSONResponse(content={"error": "Job item not found"}, status_code=404)
