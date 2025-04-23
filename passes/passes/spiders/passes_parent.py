import scrapy
import os
import re
import json

class PassesParentSpider(scrapy.Spider):
    name = "passes_parent"
    allowed_domains = ["quaeldich.de"]
    start_urls = ["https://www.quaeldich.de/regionen/alpen/schweiz/paesse/?n=600"] # filtering for Alpine passes and those in Switzerland
    output_file = "parent_data.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
            self.log(f"Deleted previous output file: {self.output_file}")

        self.data = []

    def parse(self, response):
        for pass_ in response.css("li > div.row"):
            pass_name = pass_.css("a::text").get()
            pass_url = pass_.css("a::attr(href)").get()

            elevation = pass_.css("div.d-none.d-sm-block.col-sm-2::text").re_first(r"\d+")
            if elevation:
                elevation = int(elevation)

            for pass_route in pass_.css("div.col-8.col-sm-5"):
                route_name = pass_route.css("::text").get()
                review_text = pass_route.xpath("following-sibling::div[@class='col-4 col-sm-2']/span/@title").get()

                rating, num_reviews = None, None
                if review_text:
                    match = re.search(r"(\d{1,2},\d)\s.*?(\d+)\sBewertungen", review_text)
                    if match:
                        rating = match.group(1)
                        num_reviews = match.group(2)

                if pass_name and route_name:
                    full_url = response.urljoin(pass_url.strip())
                    self.data.append({
                        "name": pass_name.strip(),
                        "url_pass": full_url,
                        "route_name": route_name.strip(),
                        "score": rating.strip().replace(",", ".") if rating else None,
                        "number_of_reviews": num_reviews.strip() if num_reviews else None,
                        "elevation": elevation
                    })

        # Save all at once when done
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        self.log(f"Saved {len(self.data)} pass entries to {self.output_file}")
