{{ config(unique_key='msisdn') }}

with parsed as (SELECT cast(key as String), cast(value as String), topic, partition, offset, timestamp, timestampType, _commit_timestamp, _commit_version, _change_type
FROM {{ delta_table_changes(source('default','bronze')) }})

select
    get_json_object(value, "$.uid") as uid,
    get_json_object(value, "$.msisdn_key") as msisdn,
    get_json_object(value, "$.subscriber_type") as subscriber_type,
    get_json_object(value, "$.customer_type") as customer_type,
    get_json_object(value, "$.last_activity_date") as last_activity_date,
    get_json_object(value, "$.status") as status,
    get_json_object(value, "$.dola") as dola,
    get_json_object(value, "$.smartphone_ind") as smartphone_ind,
    get_json_object(value, "$.loyalty_id") as loyalty_id,
    get_json_object(value, "$.loyalty_points_earned") as loyalty_points_earned,
    get_json_object(value, "$.loyalty_points_redeemed") as loyalty_points_redeemed,
    get_json_object(value, "$.loyalty_points_balance") as loyalty_points_balance,
    get_json_object(value, "$.preffered_language") as preffered_language,
    get_json_object(value, "$.gender") as gender,
    get_json_object(value, "$.consumer_address") as consumer_address,
    get_json_object(value, "$.subscriber_birthday") as subscriber_birthday,
    get_json_object(value, "$.dob") as dob,
    get_json_object(value, "$.age") as age,
    get_json_object(value, "$.active_data") as active_data,
    _commit_timestamp as commit_timestamp,
    _commit_version as commit_version
from parsed
where {{ delta_commits_per_run() }}