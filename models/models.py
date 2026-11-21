from pydantic import BaseModel, HttpUrl, TypeAdapter

adapter_urls = TypeAdapter(list[HttpUrl])


class ModelPdp(BaseModel):
    CompanyName: str | None = None
    JobTitle: str | None = None
    Country: str = "Romania"
    City: str | None = None
    url: HttpUrl
    JobPostedDate: str | None = None
    JobCategory: str | None = None
    local_job_id: str
