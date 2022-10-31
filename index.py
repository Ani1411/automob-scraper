import pandas as pd

# bikes_df = pd.read_csv('csvs/bikes_company_data.csv')
# bikes_company_list = bikes_df['company_name'].to_list()
#
# cars_df = pd.read_csv('csvs/cars_company_data.csv')
# cars_company_list = cars_df['company_name'].to_list()
#
# company_df = pd.concat([bikes_df, cars_df], axis=0)
# company_df.rename(columns={
#     'link': 'src_link',
#     'company_name': 'company',
#     'title': 'sub_company',
#     'logo_img': 'logo',
#     'number_of_wheels': 'wheeler_type'
# }, inplace=True)
#
# company_df = company_df[['company', 'sub_company', 'logo', 'about', 'wheeler_type', 'src_link']]
# company_df.to_csv('csvs/companies.csv', index=False)
# print(company_df.columns.values)

# company_df = pd.read_csv('csvs/api.company.csv')
# company_df = company_df[['id', 'sub_company']]
#
# bikes_details_df = pd.read_csv('csvs/bikes_details.csv')
# bikes_details_list = bikes_details_df['company_name'].to_list()
#
# cars_details_df = pd.read_csv('csvs/cars_details.csv')
# cars_details_list = cars_details_df['company_name'].to_list()
#
# details_df = pd.concat([bikes_details_df, cars_details_df], axis=0)
# details_df.rename(columns={
#     'model_link': 'src_link',
#     'title': 'sub_company',
#     'model_img': 'img',
#     'model_name': 'model'
# }, inplace=True)
#
# details_df = details_df[['company_name', 'sub_company', 'img', 'model', 'src_link']]
# details_dict = details_df.to_dict('records')
# for row in details_dict:
#     row['model'] = row['model'].replace(f"{row['company_name']} ", '')
#
# details_df = pd.DataFrame(details_dict)
# merged_df = pd.merge(details_df, company_df, on='sub_company', how='left')
# merged_df.rename(columns={'id': 'company_id'}, inplace=True)
# print(merged_df.columns)
# merged_df = merged_df[['company_id', 'img', 'model', 'src_link']]
# merged_df.to_csv('csvs/details.csv', index=False)
# print(merged_df.columns.values)

#
# bikes_variant_details_df = pd.read_csv('csvs/bikes_variant_details.csv')
# bikes_variant_details_list = bikes_variant_details_df['company_name'].to_list()
#
# cars_variant_details_df = pd.read_csv('csvs/cars_variant_details.csv')
# cars_variant_details_list = cars_variant_details_df['company_name'].to_list()
#
# variant_details_df = pd.concat([bikes_variant_details_df, cars_variant_details_df], axis=0)
#
# details_dict = variant_details_df.to_dict('records')
# for row in details_dict:
#     row['model_name'] = row['model_name'].replace(f"{row['company_name']} ", '')
#     row['variant_name'] = row['variant_name'].replace(f"{row['company_name']} ", '')
#
# variant_details_df = pd.DataFrame(details_dict)
# variant_details_df = variant_details_df[[ 'variant_name', 'variant_link', 'model_name', 'variant_info',
#                                          'variant_fuel_type', 'price']]
# variant_details_df.rename(columns={
#     'variant_name': 'name',
#     'variant_link': 'src_link',
#     'variant_info': 'info',
#     'variant_fuel_type': 'fuel_type',
# }, inplace=True)
# variant_details_df.to_csv('csvs/variants.csv', index=False)
# print(variant_details_df.columns.values)
