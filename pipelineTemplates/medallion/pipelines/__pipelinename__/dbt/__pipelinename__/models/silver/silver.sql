{{ config(unique_key='msisdn') }}

with parsed as (SELECT * FROM {{ delta_table_changes(source('default','bronze')) }})

select
    "uid" as uid,
    "msisdn_key" as msisdn,
    "subscriber_type" as subscriber_type,
    "customer_type" as customer_type,
    "last_activity_date" as last_activity_date,
    "status" as status,
    "dola" as dola,
    "smartphone_ind" as smartphone_ind,
    "loyalty_id" as loyalty_id,
    "loyalty_points_earned" as loyalty_points_earned,
    "loyalty_points_redeemed" as loyalty_points_redeemed,
    "loyalty_points_balance" as loyalty_points_balance,
    "preffered_language" as preffered_language,
    "gender" as gender,
    "consumer_address" as consumer_address,
    "subscriber_birthday" as subscriber_birthday,
    "dob" as dob,
    "age" as age,
    "active_data" as active_data,
    _commit_timestamp as commit_timestamp,
    _commit_version as commit_version
from parsed
where {{ delta_commits_per_run() }}
