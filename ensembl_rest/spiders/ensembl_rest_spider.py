# Run with scrapy runspider ensembl_rest_spider.py

import scrapy
import json


ensembl_rest_url = 'https://rest.ensembl.org/'



class EnsemblRESTSpider(scrapy.Spider):
    """
    Spider to extract data from the Ensembl REST API documentation.
    """
    name = "ensembl_rest"
    
    start_urls = [ensembl_rest_url]
    
    def parse(self, response):
        """Extract the API data from the webpage.
        
        The information we need for each REST endpoint is:
            - Endpoint url structure.
            - Endpoint description.
            - Endpoint documentation webpage.
        """        
        endpoints = {name : data for name,data in self.parse_endpoints(response)}
        api_version = self.parse_api_version(response)
        
        api_data = { 
            'base_url' : response.url,
            'api_version' : api_version,
            'endpoints' : endpoints
        }
            
        # --- Data has been retrieved. Prepare for output
        output_selector = {ensembl_rest_url : 'ensembl_rest_endpoints.json'}
        
        with open(output_selector[response.url], 'w') as outf:
            json.dump(api_data, outf, indent=2)
    # ---
    
    def parse_api_version(self, response):
        "Return the REST API version."
        footer = response.css('footer')
        return footer.re_first('\(Version ([0-9.]+)\)')
    # ---
    
    def parse_endpoints(self, response):
        "Return a list of the fully extracted endpoints divided by categories."
        raw_by_category = response.css('tbody')
        
        for category in raw_by_category:
            endpoints = category.css('tr')
            endpoints_data = (self.extract_endpoint(ep) for ep in endpoints)
            yield from endpoints_data
    # ---
    
    def extract_endpoint(self, raw_endpoint):
        "Unpack the information for the endpoint."
        
        extract = lambda query: (
            raw_endpoint.css(query).extract_first().strip()
        )
        
        documentation_link = extract('a::attr(href)')
        
        endpoint = {
            'resource'           : extract('a::text'),
            'documentation_link' : documentation_link,
            'description'        : extract('td:last-of-type::text')
        }
            
        endpoint_name = documentation_link.split('/').pop()
        
        return endpoint_name, endpoint
    # ---

    
    
        
