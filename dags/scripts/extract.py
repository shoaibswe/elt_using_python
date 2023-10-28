import sys
sys.path.insert(0,'/opt/airflow/dags/scripts')
import requests
import config
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
    # print("response is : ", respose)
    # print("json data is : ", respose.json())
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
    num_requests= 100
    seed = [0]
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    def generate_seeds():
        nonlocal seed
        for _ in range(num_requests):
            yield seed
            seed = next_seed(seed)

    results = pool.map(get_data, generate_seeds())

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


def transform_data(data_json):
    user_data_list = []

    # create a pandas data frame
    # do any required pre-processing such as
    # fill-in or remove garbadge value if any
    # return data frame
    for dt in data_json:
        if dt is not None and 'results' in dt:
            results = dt['results']
            if isinstance(results, list) and len(results) > 0:
                user_data = results[0]
                gender = user_data['gender']
                first_name = user_data['name']['first']
                last_name = user_data['name']['last']
                dob = user_data['dob']['date']
                city = user_data['location']['city']
                state = user_data['location']['state']
                country = user_data['location']['country']
                postcode = user_data['location']['postcode']
                nat = user_data['nat']
                phone = user_data['phone']
                email = user_data['email']
                picture_large = user_data['picture']['large']
                user_data_dict = {
                    'Gender': gender,
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Date of Birth': dob,
                    'City': city,
                    'State': state,
                    'Country': country,
                    'Postcode': postcode,
                    'Country Code (nat)': nat,
                    'Phone': phone,
                    'Email': email,
                    'Picture Large': picture_large
                }  
                user_data_list.append(user_data_dict)

                if user_data_list:
                    data_df = pd.DataFrame(user_data_list)
                    return data_df             
                # df = df.dropna()
                # df = df.drop_duplicates()
                # data_frames.append(df)
                else:
                    print("No valid data to transform")
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