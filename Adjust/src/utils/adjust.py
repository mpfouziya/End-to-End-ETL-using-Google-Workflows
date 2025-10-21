import pandas as pd
import requests
from google.cloud import secretmanager

from src.config import PROJECT_ID, ADJUST_API_TOKEN, APP_TOKEN

class Adjust:
    def __init__(self):
        self.project_id = PROJECT_ID
        self.adjust_api_token = self.load_secret(ADJUST_API_TOKEN)
        self.app_token = self.load_secret(APP_TOKEN)

        # Define the endpoint URL
        self.url = 'https://automate.adjust.com/reports-service/report'

        self.revenue_total_d_fields = ','.join(f'revenue_total_d{n}' for n in range(0, 121))
        self.revenue_total_m_fields = ','.join(f'revenue_total_m{n}' for n in range(5, 13))
        self.revenue_total_fields = self.revenue_total_d_fields + ',' + self.revenue_total_m_fields

        self.ad_revenue_total_d_fields = ','.join(f'ad_revenue_total_d{n}' for n in range(0, 121))
        self.ad_revenue_total_m_fields = ','.join(f'ad_revenue_total_m{n}' for n in range(5, 13))
        self.ad_revenue_total_fields = self.ad_revenue_total_d_fields + ',' + self.ad_revenue_total_m_fields

        self.other_metrics = ('click_cost,paid_clicks,paid_impressions,impression_cost,'
                              'event_cost,adjust_cost,network_cost,network_ad_spend_skan,cost,cohort_size_d0')
        self.metrics = self.other_metrics + ',' + self.revenue_total_fields + ',' + self.ad_revenue_total_fields
        self.dimensions = (
            "day,app,app_token,store_id,store_type,currency,currency_code,"
            "network,campaign,campaign_id_network,campaign_network,"
            "adgroup,adgroup_network,adgroup_id_network,source_network,source_id_network,"
            "creative,creative_network,creative_id_network,country,country_code,"
            "partner_name,partner_id,partner,channel,os_name"
        )

    def load_secret(self,secret_name):
        """Load a secret from Secret Manager."""
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")

    def get_adjust_data(self, start_date, end_date):
        # Set the query parameters
        params = {
            'ad_spend_mode': 'network',
            'app_token__in': f'{self.app_token}',  # Specifying the app token
            'date_period': f'{start_date}:{end_date}',
            'dimensions': f'{self.dimensions}',
            'metrics': f'{self.metrics}'
        }

        # Set the headers, including the Adjust API token
        headers = {
            'Authorization': f'Bearer {self.adjust_api_token}'
        }

        # Make the GET request to the Adjust API
        response = requests.get(self.url, headers=headers, params=params)

        # Check the response status and print the result
        if response.status_code == 200:
            print("Data fetched successfully:")
            cohort_data = response.json()  # Print the JSON response data
            cohort_data = pd.DataFrame(cohort_data['rows'])
            return cohort_data
        else:
            print(f"Error fetching data: {response.status_code}")
            print(response.text)
            return None

    def process_adjust_data(self, cohort_data, end_date):
        columns_to_drop = [col for col in cohort_data.columns if 'revenue_total_m' in col]
        data = cohort_data.drop(columns=columns_to_drop)
        data = data.drop(['country'], axis=1)
        data.rename(columns={'day': 'install_date',
                             'partner': 'ad_network',
                             'country_code': 'country',
                             'campaign': 'campaign_id',
                             'cost': 'ad_spend',
                             'cohort_size_d0': 'cohort_users',
                             'paid_clicks': 'clicks',
                             'paid_impressions': 'impressions'}, inplace=True)

        # Convert columns starting with 'revenue_' to float
        revenue_columns = [col for col in data.columns if 'revenue' in col]
        data[revenue_columns] = data[revenue_columns].apply(pd.to_numeric)
        data['cohort_users'] = data['cohort_users'].astype(int)
        data['clicks'] = data['clicks'].astype(int)
        data['impressions'] = data['impressions'].astype(int)
        data['ad_spend'] = data['ad_spend'].astype(float)

        data['install_date'] = pd.to_datetime(data['install_date'])
        data['platform'] = data['os_name']
        data['country'] = data['country'].str.upper()

        include_columns = ['install_date', 'platform', 'country', 'ad_network', 'campaign_id', 'adgroup', 'creative']
        object_columns = data.select_dtypes(include=['object']).columns
        object_columns_to_exclude = [col for col in object_columns if col not in include_columns]
        data = data.drop(columns=object_columns_to_exclude)

        grouped_data = data.groupby(
            ['install_date', 'platform', 'country', 'ad_network', 'campaign_id', 'adgroup', 'creative']).sum()
        data = grouped_data.reset_index()

        data['breakdown'] = data['platform'] + data['country'] + data['ad_network'] + data['campaign_id'] + data[
            'adgroup'] + data['creative']

        iap_columns = [col for col in data.columns if col.startswith('revenue_')]
        ads_columns = [col for col in data.columns if col.startswith('ad_revenue_')]
        fixed_columns = [col for col in data.columns if 'revenue' not in col]

        iap_melted_df = data.melt(id_vars=fixed_columns, value_vars=iap_columns, var_name='days_since_install',
                                  value_name='cohort_iap_revenue')
        iap_melted_df['days_since_install'] = iap_melted_df['days_since_install'].apply(lambda x: int(x[15:]))

        ads_melted_df = data.melt(id_vars=fixed_columns, value_vars=ads_columns, var_name='days_since_install',
                                  value_name='cohort_ads_revenue')
        ads_melted_df['days_since_install'] = ads_melted_df['days_since_install'].apply(lambda x: int(x[18:]))

        melted_df = pd.merge(iap_melted_df, ads_melted_df, on=fixed_columns + ['days_since_install'], how='left')
        melted_df['age'] = (pd.to_datetime(end_date) - melted_df['install_date']).dt.days
        melted_df = melted_df.reset_index(drop=True)

        melted_df['iap_revenue'] = melted_df.groupby(['age', 'breakdown'])['cohort_iap_revenue'].diff(periods=1).fillna(
            melted_df['cohort_iap_revenue'])
        melted_df['ads_revenue'] = melted_df.groupby(['age', 'breakdown'])['cohort_ads_revenue'].diff(periods=1).fillna(
            melted_df['cohort_ads_revenue'])

        melted_df['current_gross_revenue'] = melted_df['cohort_iap_revenue'] + melted_df['cohort_ads_revenue']
        melted_df['current_net_revenue'] = (melted_df['cohort_iap_revenue'] * 0.7) + melted_df['cohort_ads_revenue']
        revenue_columns = ['cohort_iap_revenue', 'cohort_ads_revenue', 'iap_revenue', 'ads_revenue',
                           'current_gross_revenue', 'current_net_revenue']
        melted_df[revenue_columns] = melted_df[revenue_columns].astype(float)
        melted_df['event_date'] = melted_df['install_date'] + pd.to_timedelta(melted_df['days_since_install'], unit='D')
        return melted_df



   

    

