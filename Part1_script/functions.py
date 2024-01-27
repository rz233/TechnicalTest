import requests
import time
import csv



def fetch_all_pages(base_url, params=None):
    """
    Fetches all data from url.
    Note: the first element is page metadata, and the second element is a list
    :param base_url: base_url
    :param params: url query parameters
    :return: list of all data
    """
    if params is None:
        params = {}

    all_data = []
    current_page_index = 1
    total_data_count = None

    while True:
        print(f"Fetching page {current_page_index}...")
        params['page'] = current_page_index  # Set the page parameter
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad status codes

        data = response.json()
        # print("Raw data:", data)

        print("Page info: ", data[0])
        if total_data_count is None:
            total_data_count = data[0]['total']  # Get the total from the first page

        all_data.extend(data[1])  # Append query data into all data

        time.sleep(0.05)  # wait 200ms before next request

        num_total_pages = data[0]['pages']
        # Check if we've reached the last page
        if current_page_index < num_total_pages:
            current_page_index += 1
        else:
            break

    if total_data_count != len(all_data):
        raise ValueError(f"Expected {total_data_count} items, got {len(all_data)} items")

    return all_data




# indicator and country is nested in above data
def flatten_data(dataset):
    flattened = {}
    for key, value in dataset.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flattened[f"{key}.{sub_key}"] = sub_value
        else:
            flattened[key] = value
    return flattened






def write_to_file(output_file_name, dataset):
    # Get the headers (column names) from the keys of the first item in the list
    headers = dataset[0].keys()

    with open(output_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write the data rows
        for row in dataset:
            writer.writerow(row)






def verifyData(data):
    # Verifications
    # 1. Check if "unit" and "obs_status" columns have no data
    no_data_in_unit_and_obs_status = all(row.get('unit') == '' and row.get('obs_status') == '' for row in data)

    units = {row.get('unit') for row in data}
    obs_status = {row.get('obs_status') for row in data}
    print("units:", units)
    print("obs_status:", obs_status)

    # 2. Check if all values in "decimal" and "indicator.value" are identical
    decimal_values = {row.get('decimal') for row in data}
    indicator_values = {row.get('indicator.value') for row in data}
    indicator_ids = {row.get('indicator.id') for row in data}
    print("decimal_values:", decimal_values)
    print("indicator_values:", indicator_values)
    print("indicator_ids:", indicator_ids)
    all_decimal_identical = len(decimal_values) == 1
    all_indicator_value_identical = len(indicator_values) == 1
    all_indicator_id_identical = len(indicator_ids) == 1

    # 3. Check for rows where "date" is from 1960 to 1999 and if they have "value"
    #any_data_present_between_1960_to_1999 = any((1960 <= int(row.get('year')) <= 1999) and (row.get('value') is not None) for row in data)

    # Results
    #            True                            True                      True                         True                     False
    print(no_data_in_unit_and_obs_status, all_decimal_identical, all_indicator_value_identical, all_indicator_id_identical)
