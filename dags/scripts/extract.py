import requests
import config
import multiprocessing
import os
import pandas as pd

API_URL= config.API_URL
FILENAME = "random_user.csv"

def next_seed(seed):
    # create next permutation from given SEED above
    # order is importent
    # repetittion not allowed
    pass


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
    seed = 0

    def generate_seeds():
        while seed<num_requests:
            yield seed
            seed +=1

    pool= multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(get_data,generate_seeds())

    pool.close()
    pool.json()
    # pass
    return results



def get_file_path():
    # should return a os file path with correct destination.
    # Do not change file name
    # filename = "random_user.csv"
    # filepath = ""
    # return filepath
    filepath = os.path.join(os.getcwd(),FILENAME)
    return filepath


def transform_data(data_json):
    # create a pandas data frame
    # do any required pre-processing such as
    # fill-in or remove garbadge value if any
    # return data frame
    if data_json:
        df = pd.DataFrame(data_json)
        return df
    else:
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
