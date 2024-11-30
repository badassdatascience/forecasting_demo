#
# load useful libraries
#
import boto3
import pandas as pd
import numpy as np
import time
import datetime

#
# user settings
#

class ec2PriceData():

    #
    # constructor
    #
    def __init__(self):
        self.product_descriptions = ['Linux/UNIX']
        self.availability_zone = 'us-west-2a'

        self.instance_types = [
            'm2.xlarge',
        ]

        self.time_to_sleep_between_post_requests = 5
        self.number_of_times_to_run_post_requests = 5

        self.frequency_str = '1440min'
        self.output_directory = 'output'

    def fit(self):
        self.connect_to_ec2_API()
        self.pull_ec2_spot_price_data_from_AWS()
        self.assemble_and_clean_the_pull_data()
        self.resample()
        self.create_final_dataframe()
        
    #
    # create an ec2 client to facilitate communication with the AWS EC2 API
    #
    def connect_to_ec2_API(self):
        self.ec2 = boto3.client('ec2')

    #
    # pull ec2 spot price data from AWS
    #
    def pull_ec2_spot_price_data_from_AWS(self):
        spot_price_list = []
        self.df_pre_resample_list = []

        response = self.ec2.describe_spot_price_history(
            AvailabilityZone = self.availability_zone,
            ProductDescriptions = self.product_descriptions,
            InstanceTypes = self.instance_types,
        )
        spot_price_list.extend(response['SpotPriceHistory'])

        df_pre_resample_portion = pd.DataFrame(spot_price_list)
        self.df_pre_resample_list.append(df_pre_resample_portion)
        timestamp_min = np.min(df_pre_resample_portion['Timestamp'])

        for i in range(0, self.number_of_times_to_run_post_requests):
            time.sleep(self.time_to_sleep_between_post_requests)
            response = self.ec2.describe_spot_price_history(
                NextToken = response['NextToken'],
                AvailabilityZone = self.availability_zone,
                ProductDescriptions = self.product_descriptions,
                InstanceTypes = self.instance_types,
                EndTime = timestamp_min,
                StartTime = timestamp_min - datetime.timedelta(weeks=6)
            )

            spot_price_list.extend(response['SpotPriceHistory'])
            df_pre_resample_portion = pd.DataFrame(spot_price_list)
            self.df_pre_resample_list.append(df_pre_resample_portion)
            timestamp_min = np.min(df_pre_resample_portion['Timestamp'])

    #
    # assemble the queried data into one dataframe
    #
    def assemble_and_clean_the_pull_data(self):
        self.df_pre_resample = (
            pd.concat(
                self.df_pre_resample_list
            )
            .drop_duplicates()
            .sort_values(
                by = ['Timestamp']
            )
            .reset_index()
            .drop(
                columns = ['index']
            )
        )
        

    #
    # resample
    #
    def resample(self):
    
        def custom_resampler(arraylike):
            return np.mean([float(x) for x in arraylike])

        self.df_pre_resample.index = self.df_pre_resample['Timestamp']

        self.series = (
            self.df_pre_resample['SpotPrice']
            .resample(self.frequency_str)
            .apply(custom_resampler)
        )

    #
    # create final dataframe
    #
    def create_final_dataframe(self):
        self.df = pd.DataFrame({'spot_price' : self.series})

    def save(self, filename):
        self.df.to_csv(filename, index = True)

