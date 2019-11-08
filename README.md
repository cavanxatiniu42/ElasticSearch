                                ===========Installation Guide============
1. Download and install ElasticSearch
- This project was built on macos so the current version of elasticsearch is for macos.
If you are using other operating system, please go to https://www.elastic.co/guide/en/elasticsearch/reference/7.4/install-elasticsearch.html
to find the suitable version of elasticsearch
- Extract the compressed file to the project folder. Please refer the above link for instalation guide for each operating system.
- For this project, using ./bin/elasticsearch to start elasticsearch
- Go to browser and type localhost:9200 to make sure the application is running fine

2. Install necessary python packages
- Try pip install -r requirement.txt

3. Crawl and index data
- Try python3 crawl_sendo_data
- Go to browser and type localhost:9200/men-wears/_search to see all the data crawled are indexed in elasticsearch

4. Run application
- Try python3 search_engine.py
- Go to browser and type localhost:8005 to see the application





                                =============Explanation================
1. Create mapping to index data
- There is a function called create_mapping() in crawl_sendo_data.py to define template to new index
- In this example, I just use three properties of sendo data, they are name, price and image and define their index property and data type
We can add more properties as many as we want.
- Create men-wears index by calling function create_men_wears_index() in crawl_sendo_data.py
This index is defined following the created template mentioned aboved

2. Crawl sendo data
- Simply crawl sendo data by using public API. In this example, I am using https://www.sendo.vn/thoi-trang-nam data
- For each product in the response, I add its name, price and image to my current index men-wears

3. Searching
- There are 2 options of searching are search by name and aggregate by price but we can combine them to make the third option


4. API defined:
- Go to browser and type localhost:8005 and using following API

- Search by name:
GET /search_result_by_name?search_term=

- Aggregate by price:
GET /search_result_by_price?gtprice=&ltprice=

- Search by both name and price:
GET /search_by_name_price?search_term=&gtprice=&ltprice=

In name searching, if search term has more than one token, they should be separated by '+'
In price searching:
- gtprice means greater than price, that is the lower limit of price
- ltprice means less than price, that is the upper limit of price
