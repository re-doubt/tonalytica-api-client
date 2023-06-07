import click
import requests
from tonalytica_client import TonalyticaAPIClient

template = u"""/*
Name: {name}
Data source: {data_source}
Created By: {created_by}
Last Updated At: {last_updated_at}
*/
{query}"""


def save_queries(queries):
    for query in queries:
        filename = "query_{}.sql".format(query["id"])
        with open(filename, "w") as f:
            content = template.format(
                name=query["name"],
                data_source=query["data_source_id"],
                created_by=query["user"]["name"],
                last_updated_at=query["updated_at"],
                query=query["query"],
            )
            f.write(content)


@click.command()
@click.argument("tonalytica_url")
@click.option(
    "--api-key",
    "api_key",
    required=True,
    envvar="TONALYTICA_API_KEY",
    show_envvar=True,
    prompt="API Key",
    help="User API Key",
)
def main(tonalytica_url, api_key):
    tonalytica = TonalyticaAPIClient(api_key, tonalytica_url)
    queries = tonalytica.paginate(tonalytica.queries)
    save_queries(queries)


if __name__ == "__main__":
    main()
