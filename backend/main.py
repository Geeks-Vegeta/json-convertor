import uvicorn
from fastapi import FastAPI
from routes import csv_route, xlxs_route

description = """

## JSON CONVERTOR

You can **TRY OUT**.

Currently this API has access to all **origins**
<br>

* **/convert/xlsx** (REST API :- API for converting xlsx to json).
* **/convert/csv** (Webhook :- API for converting csv to json).
"""

app = FastAPI(
    title="JSON CONVERTOR",
    description=description,
    summary="JSON CONVERTOR API For MONGODB 🤖",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Backend",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/")
async def home():
  return {"status":"ok"}


app.include_router(csv_route.router)
app.include_router(xlxs_route.router)


if __name__ == "__main__":
  uvicorn.run("main:app",host="0.0.0.0",port=80, reload=True)