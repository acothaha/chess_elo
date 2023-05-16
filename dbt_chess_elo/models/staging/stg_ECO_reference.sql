-- stg_ECO_reference.sql

{{ config(materialized="view") }}

select *,
from {{ source('staging','ECO_reference') }}


