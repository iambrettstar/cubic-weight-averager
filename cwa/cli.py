import requests
import typer


app = typer.Typer()


CONVERSION_FACTOR = 250


def fetch_data(api_url: str):
    '''
    Fetch data from the specified URL and return json response

    :param api_url: string url
    :return: json response
    '''
    result = requests.get(api_url)
    if result.status_code != 200:
        result.raise_for_status()

    return result.json()


def calculate_cubic_weight(item: dict):
    '''
    Calculate the cubic weight of the given item.

    Assumes that the size is given in cm

    :param item: dict formatted as per the API, with a field "size" containing 3 fields "length", "width" and "height"
    :return: cubic weight in kgs
    '''
    size = item['size']

    # dimensions in cm
    length = size['length']
    width = size['width']
    height = size['height']

    volume_in_cubic_metres = (length / 100) * (width / 100) * (height / 100)

    cubic_weight = volume_in_cubic_metres * CONVERSION_FACTOR

    return cubic_weight


@app.command()
def average_cubic_weight(
        category: str = 'Air Conditioners',
        api_url_base: str = 'http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com',
        starting_path: str = '/api/products/1'
):
    # tuple containing total cubic weight and number of items
    weights = (0, 0)

    result_data = {'next': starting_path}

    # API returns next path, loop over results until next is None
    while result_data.get('next'):
        next_result = fetch_data(f'{api_url_base}{result_data["next"]}')

        for item in next_result.get('objects'):
            if item.get('category') != category:
                continue

            cubic_weight = calculate_cubic_weight(item)

            # append total weight and increment number of items
            weights = (weights[0] + cubic_weight, weights[1] + 1)

        result_data = next_result

    # after iterating over all items available via the API, calculate the average
    ave_cubic_weight = weights[0] / weights[1] if weights[1] > 0 else 0

    # make pretty to read
    formatted_average = '{:.2f}'.format(ave_cubic_weight)

    typer.echo(f'Average cubic weight: {formatted_average}kg')

    return ave_cubic_weight


# Callable via poetry's script
def main():
    app()


# Also callable without poetry
if __name__ == '__main__':
    app()
