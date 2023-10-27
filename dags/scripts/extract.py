import requests
from scripts import config
import multiprocessing
import os
import pandas as pd
import itertools

API_URL= config.API_URL
FILENAME = "random_user.csv"

def next_seed(seed):
    # create next permutation from given SEED above
    # order is importent
    # repetittion not allowed
    # seed_list = list((set(seed)))
    seed_list = list(map(str, set(seed)))  

    permutations =  list(itertools.permutations(seed_list))
    current_index= permutations.index(tuple(seed_list))
    next_index= (current_index+1)%len(permutations)
    next_permutation = list(permutations[next_index])

    # next_seed = seed.copy()
    # for x in range(len(seed)):
    #     next_seed[x] = next_permutation[x]
    # return next_seed
    next_seed_list = list(seed)
    for x in range(len(seed)):
        next_seed_list[x] = next_permutation[x]
    
    return ''.join(next_seed_list)    
    # pass


def get_data(seed):
    # fetch data from API_URL defined in config and return the json data
    respose = requests.get(f"{API_URL}/{seed}")
    if respose.status_code==200:
        return respose.json()
    else:
        return None
    # pass


def import_data():
    # Use multiprocessing or thread pool or concurrency
    # to generate next seed and then make parallal get api request and fetch single user data.
    # a total of 10000 api call need to be made
    # no api call should have same seed value.
    num_requests= 10000
    seed = [0]
    pool= multiprocessing.Pool(processes=multiprocessing.cpu_count())

    def generate_seeds():
        nonlocal seed
        for _ in range(num_requests):
            yield seed
            seed = next_seed(seed)

    results = pool.map(get_data,generate_seeds())

    pool.close()
    pool.join()

    return results
    # pass



def get_file_path():
    # should return a os file path with correct destination.
    # Do not change file name
    # filename = "random_user.csv"
    # filepath = ""
    # return filepath
    filepath = os.path.join(os.getcwd(),FILENAME)
    return filepath


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def transform_data(data_json):
    # create a pandas data frame
    # do any required pre-processing such as
    # fill-in or remove garbadge value if any
    # return data frame
    if data_json is not None and isinstance(data_json, list) and len(data_json) > 0:
        # def convert_lists_to_str(data_dict):
        #     for key, value in data_dict.items():
        #         if isinstance(value, list):
        #             data_dict[key] = str(value)
        #     return data_dict            

        # # valid_data = [item for item in data_json if item is not None]
        # valid_data = [convert_lists_to_str(item) for item in data_json if item is not None]
        flattened_data = [flatten_dict(item) for item in data_json if item is not None]

        if len(flattened_data) > 0:
            for item in flattened_data:
                for key, value in item.items():
                    if isinstance(value, list):
                        item[key] = ', '.join(map(str, value))

            keys = flattened_data[0].keys()
            df = pd.DataFrame(flattened_data, columns=keys)
            df = df.dropna()
            df = df.drop_duplicates()
            return df

        # df = pd.DataFrame(data_json)
        # return df
    else:
        print("No valid data to Transform")
        return None
    # pass


def save_new_data_to_csv(data):
    # save the data to a csv file
    # file should be saved in the defined location
    # filename = get_file_path()
    filepath = get_file_path()
    data.to_csv(filepath,index=False)
    # pass


def main():
    data_json = import_data()
    data_df= transform_data(data_json)
    # pass
    if data_df is not None:
        save_new_data_to_csv(data_df)

if __name__ == "__main__":
    main()


#Installed pandas lib