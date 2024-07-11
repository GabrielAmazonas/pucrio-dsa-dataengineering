from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import pandas as pd
from io import BytesIO
from minio import Minio

# MinIO credentials and endpoint
# Define MinIO credentials and endpoint
access_key = 'minioroot'
secret_key = 'miniopassword'
minio_endpoint = 'filestorage:9000'  # Replace with your MinIO server endpoint
minio_bucket_name = 'olympicweightliftingbucket'
object_name = 'athlete_events.parquet'

# Initialize MinIO client
client = Minio(minio_endpoint,
               access_key=access_key,
               secret_key=secret_key,
               secure=False)  # Change to True if MinIO is using HTTPS

# Function to read Parquet file from MinIO into pandas DataFrame
def read_parquet_from_minio(client, bucket_name, object_name):
    try:
        # Download object into memory
        object_data = client.get_object(bucket_name, object_name)
        parquet_bytes = object_data.read()

        # Read Parquet data using pandas and pyarrow
        buffer = BytesIO(parquet_bytes)
        df = pd.read_parquet(buffer, engine='pyarrow')

        return df

    except Exception as err:
        print(f"Error: {err}")
        return None


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    df = read_parquet_from_minio(client, minio_bucket_name, object_name)


    # Create athlete_df
    athlete_df = df[['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Team']].drop_duplicates().reset_index(drop=True)
    athlete_df['athlete_id'] = athlete_df.index + 1  # Adding athlete_id as primary key
    team_df = df[['Team', 'NOC', 'Sport']].drop_duplicates().reset_index(drop=True)
    team_df['team_id'] = team_df.index + 1  # Adding team_id as primary key

    # Create games_df
    games_df = df[['Games', 'Year', 'Season', 'City']].drop_duplicates().reset_index(drop=True)
    games_df['games_id'] = games_df.index + 1  # Adding games_id as primary key

    # Create event_df
    event_df = df[['Event']].drop_duplicates().reset_index(drop=True)
    event_df['event_id'] = event_df.index + 1  # Adding event_id as primary key

    # Create medal_df
    medal_df = df[['ID', 'Games', 'Event', 'Medal']].copy()
    medal_df = medal_df.merge(athlete_df[['ID', 'athlete_id']], left_on='ID', right_on='ID', how='left')
    medal_df = medal_df.merge(games_df[['Games', 'games_id']], left_on='Games', right_on='Games', how='left')
    medal_df = medal_df.merge(event_df[['Event', 'event_id']], left_on='Event', right_on='Event', how='left')
    medal_df = medal_df[['ID', 'Games', 'Event', 'Medal', 'athlete_id', 'games_id', 'event_id']]

    print(medal_df.info())

    tables = [
        {'table_name': 'athlete', 'df': athlete_df},
        {'table_name': 'team', 'df': team_df},
        {'table_name': 'games', 'df': games_df},
        {'table_name': 'event', 'df': event_df},
        {'table_name': 'medal', 'df': medal_df}
    ]

    schema_name = 'weightlifting_olympians'  # Specify the name of the schema to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
       

        for table in tables:
            loader.export(
                table['df'],
                schema_name,
                table['table_name'],
                index=False,  # Specifies whether to include index in exported table
                if_exists='replace',  # Specify resolution policy if table name already exists
            )

        loader.execute("""
            ALTER TABLE weightlifting_olympians.athlete ADD CONSTRAINT fk_athlete_team FOREIGN KEY (team_id) REFERENCES weightlifting_olympians.team(team_id);
        """)


        loader.execute("""
            ALTER TABLE weightlifting_olympians.medal ADD CONSTRAINT fk_medal_athlete FOREIGN KEY (athlete_id) REFERENCES weightlifting_olympians.athlete(athlete_id);
            ALTER TABLE weightlifting_olympians.medal ADD CONSTRAINT fk_medal_event FOREIGN KEY (event_id) REFERENCES weightlifting_olympians."event"(event_id);
            ALTER TABLE weightlifting_olympians.medal ADD CONSTRAINT fk_medal_games FOREIGN KEY (games_id) REFERENCES weightlifting_olympians.games(games_id);
        """)
        

    return df