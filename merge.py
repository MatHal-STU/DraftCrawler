import pandas as pd
import os

folder_path = r'D:\Skola\VINF\DraftCrawler\wiki\big'
crawler_file = "D:\Skola\VINF\DraftCrawler\output.csv"
all_files = os.listdir(folder_path)

csv_files = [f for f in all_files if f.endswith('.csv')]
df_list = []
column_names = ["Overall", "Name", "Country", "Junior_Team", "Year"]
crawler_file_names = ["Name", "Team", "Round", "Overall", "Year", "Position", "Country", "Junior_Team"]
for csv in csv_files:
    file_path = os.path.join(folder_path, csv)
    try:
        df = pd.read_csv(file_path, names=column_names)
        df_list.append(df)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_path, sep='\t', encoding='utf-16')
            df_list.append(df)
        except Exception as e:
            print(f"Could not read file {csv} because of error: {e}")
    except Exception as e:
        print(f"Could not read file {csv} because of error: {e}")

big_df = pd.concat(df_list, ignore_index=True)
df = pd.read_csv(crawler_file, names=crawler_file_names)
df = df.drop_duplicates()
merged_df = pd.merge(df, big_df, on=["Overall", "Year"], how="left", suffixes=('_df', '_big_df'))
merged_df["Junior_Team_df"] = merged_df.apply(lambda row: row["Junior_Team_big_df"] if row["Junior_Team_df"] == "Unknown" else row["Junior_Team_df"], axis=1)
merged_df["Country_df"] = merged_df.apply(lambda row: row["Country_big_df"] if row["Country_df"] == "Unknown" else row["Country_df"], axis=1)
# print(df.loc[[159220]])
merged_df["Junior_Team_df"] = merged_df["Junior_Team_df"].fillna("Unknown")
merged_df["Country_df"] = merged_df["Country_df"].fillna("Unknown")

merged_df = merged_df.drop(columns=["Junior_Team_big_df","Name_big_df", 'Country_big_df'])
merged_df = merged_df.drop_duplicates()
merged_df["Country_df"] = merged_df["Country_df"].apply(lambda x: x.split('|')[-1] if '|' in str(x) else x)
merged_df.to_csv(os.path.join("./", 'output_merged.csv'), index=False, header=False)