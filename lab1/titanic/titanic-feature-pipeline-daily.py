import modal

LOCAL = False

if not LOCAL:
    stub = modal.Stub()
    image = modal.Image.debian_slim().pip_install(["hopsworks==3.0.4"])


    @stub.function(image=image, secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
    # schedule=modal.Period(days=1)
    def titanic_feature_pipeline_daily():
        g()


def generate_passenger(passenger_id, survived):
    """
    Returns a single passenger as a single row in a DataFrame
    """
    import pandas as pd
    import numpy as np
    import random

    bins = [-np.infty, 20, 25, 29, 30, 40, np.infty]  # use same bins as in feature definition!
    age_bin_min = 0
    age_bin_max = len(bins) - 1

    random_age_bin = random.randint(age_bin_min, age_bin_max)
    random_sex = random.randint(0, 1)
    random_fare = random.uniform(0, 500)
    random_pclass = random.randint(1, 3)

    df = pd.DataFrame({"passengerid": [passenger_id],
                       "age": [random_age_bin],
                       "sex": [random_sex],
                       "fare": [random_fare],
                       "pclass": [random_pclass]})

    df['survived'] = survived
    return df


def get_random_titanic_passenger(passenger_id):
    """
    Returns a DataFrame containing one random passenger
    """
    import random

    # randomly pick one of these 3 and write it to the featurestore
    pick_random = random.uniform(0, 2)
    if pick_random >= 1:
        passenger_df = generate_passenger(passenger_id, 1)
        print("Survived Passenger added!")
    else:
        passenger_df = generate_passenger(passenger_id, 0)
        print("Didn't Survived Passenger added!")

    return passenger_df


def g():
    import hopsworks

    project = hopsworks.login()
    fs = project.get_feature_store()

    titanic_fg = fs.get_feature_group(name="titanic_modal", version=1)

    # get max id to generate new passenger id for the random passenger
    titanic_df = titanic_fg.read()
    passenger_id = titanic_df['passengerid'].max() + 1

    new_random_passenger_df = get_random_titanic_passenger(passenger_id)

    titanic_fg.insert(new_random_passenger_df, write_options={"wait_for_job": False})


if __name__ == "__main__":
    if LOCAL == True:
        g()
    else:
        #stub.deploy('titanic_feature_pipeline_daily')
        with stub.run():
            titanic_feature_pipeline_daily() #run the function f