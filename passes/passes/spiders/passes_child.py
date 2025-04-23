import scrapy
import json
import os
import re
from passes.spiders.utils import slugify
from passes.items import PassesItem

class PassesChildSpider(scrapy.Spider):
    name = "passes_child"
    start_urls = []  # not used
    output_file = "full_pass_data.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
            self.log(f"Deleted previous output file: {self.output_file}")

        self.data = []

    def start_requests(self):
        with open("parent_data.json", encoding="utf-8") as f:
            passes = json.load(f)

        for pass_info in passes:
            yield scrapy.Request(
                url=pass_info["url_pass"],
                callback=self.parse_pass,
                cb_kwargs={"meta_data": pass_info},
		dont_filter=True # tells Scrapy to not skip duplicate URLs
            )

    def parse_pass(self, response, meta_data):

        # Check if pass is labeled "Schotter" — skip if found
        if response.css("a.badge[title*='nicht asphaltierten']::text").get() == "Schotter":
            self.log(f"Skipped Schotter route: {meta_data['name']} ({meta_data['route_name']})", level=scrapy.logformatter.logging.INFO)
            return  # Skip this pass

        item = PassesItem()
        item["name"] = meta_data["name"]
        item["url_pass"] = meta_data["url_pass"]
        item["route_name"] = meta_data["route_name"]
        item["score"] = meta_data["score"]
        item["number_of_reviews"] = meta_data["number_of_reviews"]
        item["elevation"] = meta_data["elevation"]
        route_name = meta_data["route_name"] # define the variable 

        # Check if pass is labeled "dead end" 
        if response.css("a.badge[title*='Stichstraße mit nur einer Auffahrt.']::text").get() == "Sackgasse":
            deadend = "dead end"
        else:
            deadend = "not a dead end"

        item["deadend"] = deadend 

        gps_text = response.css("div.coords a::text").get()
        if gps_text:
            item["GPS"] = gps_text.strip()
      
        # get route URL
        slug_route = slugify(item["route_name"]) 
        route_URL = item["url_pass"].rstrip("/") + "/profile/" + slug_route
        item["url_route"] = route_URL

        # get route information # XPath to find the <a> containing the route name # Then get the next <small> element that follows
        xpath_expr = f'//a[contains(text(), "{route_name}")]/following-sibling::small[1]/text()'

        raw_text = response.xpath(xpath_expr).get()

        if raw_text:
            parts = [part.strip() for part in raw_text.strip().split("|")]

            if len(parts) >= 3:
                length = parts[0].replace("km", "").strip().replace(",", ".")
                elevation_gain = parts[1].replace("Hm", "").strip()
                gradient = parts[2].replace("%", "").strip().replace(",", ".")

                item["length"] = float(length)
                item["elevation_gain"] = int(elevation_gain)
                item["gradient"] = float(gradient)

       # yield item
        yield scrapy.Request(
        url = route_URL,
        callback=self.parse_route_gif,
        cb_kwargs={"item":item},
        dont_filter=True
        )

    def parse_route_gif(self, response, item):
        # Look for the gif image
        gif_url = response.xpath("//h2[text()='Höhenprofil']/following::img[1]/@src").get()

        if gif_url:
            # Convert relative to full URL if needed
            gif_url = response.urljoin(gif_url)
            item["url_gif"] = gif_url

        yield item


