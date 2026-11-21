import re
from urllib.parse import urlparse
from lxml import etree, html
from models.models import adapter_urls, ModelPdp


class Parser:
    def parse_sitemap(self, xml: str):
        tree = etree.fromstring(xml.encode("utf-8"))
        urls = tree.xpath('//*[local-name()="url"]/*[local-name()="loc"]/text()')
        validated = adapter_urls.validate_python(urls)
        return [str(url) for url in validated]

    def parse_pdp(self, h: str, pdp_url: str):
        tree = html.fromstring(html=h)

        output_data = {
            "desc": tree.xpath(
                '//*[@class="job"]//span[@itemprop="description"]//p//text()'
            ),
            "comp_name": tree.xpath(
                'string(//*[@class="jobDisplayShell"]/meta[@itemprop="hiringOrganization"]/@content)'
            ),
            "job_title": (
                tree.xpath('string(//h1[@id="job-title"])').strip()
                or tree.xpath(
                    'string(//span[@data-careersite-propertyid="title"])'
                ).strip()
            ),
            "city": ", ".join(
                [
                    e.xpath("string(.)")
                    .strip()
                    .replace("RO", "")
                    .strip()
                    .replace(",", "")
                    for e in tree.xpath(
                        '//*[@id="job-location"]//*[@class="jobGeoLocation"]'
                    )
                    if e.xpath("string(.)").strip()
                ]
            ),
            "job_post_date": tree.xpath(
                'string(//*[@class="jobDisplayShell"]//meta[@itemprop="datePosted"]/@content)'
            ).strip(),
            "job_category": [
                re.sub(r"[,\s]+$", "", el.xpath("string(.)")).strip()
                for el in tree.xpath('//*[@id="similar-jobs-links"]//a')
            ],
        }

        pdp_result = {
            "CompanyName": output_data["comp_name"] or None,
            "JobTitle": output_data["job_title"] or None,
            "Country": "Romania",
            "City": output_data["city"] or None,
            "url": pdp_url,
            "JobPostedDate": output_data["job_post_date"] or None,
            "JobCategory": output_data["job_category"][0]
            if output_data["job_category"]
            else None,
            "local_job_id": list(filter(bool, urlparse(pdp_url).path.split("/")))[-1],
        }

        return ModelPdp.model_validate(pdp_result).model_dump(mode="json")
