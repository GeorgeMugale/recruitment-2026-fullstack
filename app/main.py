from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List # help with type hints
from app.scraper import scrape_zambia_constituencies
from app.cache import get_cache, set_cache
from app.utils import find_province_by_constituency
from app.schemas import ConstituencyResponse, HTTPValidationError, ProvinceConstituencyResponse , ValidationErrorItem 

app = FastAPI(title="Zambia Constituencies API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_data():
    cached = get_cache()
    if cached:
        return cached

    try:
        data = scrape_zambia_constituencies()
        set_cache(data)
        return data
    except Exception:
        if cached:
            return cached
        raise


@app.get("/api/provinces", response_model=List[str]) # explicitly document the return type
def get_provinces():
    """Get all provinces in Zambia"""
    data = load_data()
    return sorted(data.keys())


@app.get("/api/constituencies", response_model=List[str]) # explicitly document the return type
def get_all_constituencies():
    """Get all constituencies across all provinces"""
    data = load_data()
    # Flatten all constituencies into a single list
    all_constituencies = []
    for constituencies in data.values():
        all_constituencies.extend(constituencies)
    return sorted(all_constituencies) # return an array of string to match documentation (from {"Province1": ["C1", "C2"], "Province2": ["C3"]} to ["C1", "C2", "C3"])


@app.get(
    "/api/constituencies/{province}",
    response_model=ConstituencyResponse, # explicitly document the return type
    responses={404: {"description": "Province not found"},
               422: {"model": HTTPValidationError, "description": "Validation Error"}} # document possible error responses (404, 422)
)
def get_constituencies_by_province(province: str):
    """Get constituencies for a specific province"""
    data = load_data()

    if province not in data:
        raise HTTPException(status_code=404, detail="Province not found")

    return ConstituencyResponse(
        province=province,
        constituencies=data[province]
    ) # return a ConstituencyResponse() instance


@app.get(
    "/api/constituency/{name}",
    response_model=ProvinceConstituencyResponse, # explicitly document the return type
    responses={404: {"description": "Constituency not found"},
               422: {"model": HTTPValidationError, "description": "Validation Error"}}
)
def get_province_by_constituency(name: str):
    """Find which province a constituency belongs to"""
    data = load_data()

    province = find_province_by_constituency(data, name)

    if not province:
        raise HTTPException(status_code=404, detail="Constituency not found")

    return ProvinceConstituencyResponse(
        constituency=name,
        province=province
    ) # return a ProvinceConstituencyResponse() instance