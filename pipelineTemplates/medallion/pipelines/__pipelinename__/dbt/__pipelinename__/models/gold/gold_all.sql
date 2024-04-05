{{ config( materialized='incremental', unique_key='msisdn', alias=var("alias-gold"),
    incremental_strategy='merge', file_format='delta', location_root=var("path-gold") ) }}

select
    msisdn,
    struct(uid as customerId) as customer360,
    struct(
        subscriber_type as customerSubCategory,
        customer_type as customerCategory,
        status) as customer,
    struct(
        last_activity_date as interActionDate,
        dola as interActionDate2)as partyInteraction,
    struct(smartphone_ind as resourceSpecification) as resource,
    struct(
        loyalty_id as id,
        loyalty_points_earned as actionType,
        loyalty_points_redeemed as actionAttribute,
        loyalty_points_balance as actionAttribute2
    ) as loyalty,
    struct(
        preffered_language as languageCode,
        preffered_language as isFavoriteLanguage,
        gender as gender,
        dob as birthDate
    ) as individual,
    struct(
        consumer_address as mediumCharacteristic,
        consumer_address as mediumType
    ) as contactMedium,
    subscriber_birthday as computed,
    age as computed2,
    struct(active_data as usageData) as usage,
    commit_timestamp
FROM {{ delta_table_changes(ref("silver")) }}