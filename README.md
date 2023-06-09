# TONalytica-API-Client

[![PyPI version fury.io](https://badge.fury.io/py/tonalytica-client.svg)](https://pypi.org/project/tonalytica-client/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/tonalytica-client.svg)](https://pypi.python.org/pypi/tonalytica-client/)
[![PyPI license](https://img.shields.io/pypi/l/tonalytica-client.svg)](https://pypi.python.org/pypi/tonalytica-client/)


The official API client and utilities to manage a TONalytica instance written in Python.

- [INSTALLATION](#installation)
- [EXAMPLE SCRIPTS](#example-scripts)


## Installation

To install it you will need Python 3.6 or above. We recommend that you use a [virtual environment].


```bash
pip install --upgrade tonalytica-client
```

This command will update `tonalytica-client` if you have already installed it.

[virtual environment]: https://pythonbasics.org/virtualenv/

## API Authentication
All the API calls support authentication with an API key. TONalytica has two types of API keys:

 - **User API Key:** has the same permissions as the user who owns it. Can be found on a user profile page.
 - **Query API Key:** has access only to the query and its results. Can be found on the query page.

 - Whenever possible we recommend using a Query API key

## Getting Started

```python
from tonalytica_client import TonalyticaAPIClient

# Create API client instance
"""
    :args:
    API_KEY
    TONALYTICA_HOST (optional): `https://tonalytica.redoubt.online/` by default
"""
tonalytica = TonalyticaAPIClient(API_KEY)
```

## API REFERENCE

### Common Endpoints

Below is an incomplete list of TONalytica's API endpoints as of V9. These may change in future versions of TONalytica.

Each endpoint is appended to your TONalytica base URL. For example:

- `https://tonalytica.redoubt.online/<slug>`

### Queries

`/queries`
+ GET: Returns a paginated array of query objects.
	- Includes the most recent `query_result_id` for non-parameterized queries.
  
  	```python 
    tonalytica.queries()
    ```

+ POST: Create a new query object

`/queries/<id>`
+ GET: Returns an individual query object
  	
    ```python 
    tonalytica.get_query(query_id="")
    ```
  
+ POST: Edit an existing query object.
+ DELETE: Archive this query. 


`/queries/<id>/results`


+ GET: Get a cached result for this query ID.
    - Only works for non parameterized queries. If you attempt to GET results
for a parameterized query you'll receive the error: `no cached result found
for this query`. See POST instructions for this endpoint to get results for
parameterized queries.

+ POST: Initiates a new query execution or returns a cached result.
    - The API prefers to return a cached result. If a cached result is not
available then a new execution job begins and the job object is returned. To
bypass a stale cache, include a `max_age` key which is an integer number of
seconds. If the cached result is older than `max_age`, the cache is ignored
and a new execution begins. If you set `max_age` to `0` this guarantees a new
execution.
    - If passing parameters, they must be included in the JSON request body as
a `parameters` object.


Here's an example JSON object including different parameter types:

```
{ 
    "parameters": {
    	"number_param": 100,
    	"date_param": "2020-01-01",
    	"date_range_param": {
    		"start": "2020-01-01",
    		"end": "2020-12-31"
    		}
    	},
      "max_age": 1800
    }
}
```


### Jobs

`/jobs/<job_id>`
+ GET: Returns a query task result (job)
	+ Possible statuses:
		- 1 == PENDING (waiting to be executed)
		- 2 == STARTED (executing)
		- 3 == SUCCESS
		- 4 == FAILURE
		- 5 == CANCELLED
	+ When status is success, the job will include a `query_result_id`

### Query Results

`/query_results/<query_result_id>`
+ GET: Returns a query result
	- Appending a filetype of `.csv` or `.json` to this request will return a downloadable file. If you append your `api_key` in the query string, this link will work for non-logged-in users.

### Dashboards

`/dashboards`
+ GET: Returns a paginated array of dashboard objects.

	```python 
    tonalytica.dashboards()
    ```
 
+ POST: Create a new dashboard object

`/dashboards/<dashboard_slug>`
+ GET: Returns an individual dashboard object.

	```python 
    tonalytica.get_dashboard(id="")
    ```
 
+ DELETE: Archive this dashboard

`/dashboards/<dashboard_id>`
+ POST: Edit an existing dashboard object.


## Example scripts

With `tonalytica-client` installed you will have access to several example CLI scripts within your terminal.

```text

gdpr-scrub                  Search for a string term in  your TONalytica queries
                            and query results. The script returns a list of
                            URLs in your instance that contain references to
                            the search term you provide
find-tables                 Search the text of queries against a data source
                            to see which table names are used in queries of
                            that source. This script relies on regex that is
                            tested against ANSI SQL.
clone-dashboard-and-queries Completely duplicate a dashboard by copying all 
                            its queries and visualizations.
export-queries              Export all the queries of your TONalytica instance
                            as text files.
```

## Documentation

[TONalytica API at GitBook](https://docs.tonalytica.redoubt.online/api-reference#api-authentication)


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
