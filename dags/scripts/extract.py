import requests
import config


def next_seed(seed):
    # create next permutation from given SEED above
    # order is importent
    # repetittion not allowed
    pass


def get_data(seed):
    # fetch data from API_URL defined in config and return the json data
    pass


def import_data():
    # Use multiprocessing or thread pool or concurrency
    # to generate next seed and then make parallal get api request and fetch single user data.
    # a total of 10000 api call need to be made
    # no api call should have same seed value.
    pass



def get_file_path():
    # should return a os file path with correct destination.
    # Do not change file name
    filename = "random_user.csv"
    filepath = ""
    return filepath


def transform_data(data_json):
    # create a pandas data frame
    # do any required pre-processing such as
    # fill-in or remove garbadge value if any
    # return data frame
    pass


def save_new_data_to_csv(data):
    # save the data to a csv file
    # file should be saved in the defined location
    # filename = get_file_path()
    pass


def main():
    pass


if __name__ == "__main__":
    main()
