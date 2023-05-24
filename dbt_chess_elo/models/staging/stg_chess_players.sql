ate-- stg_chess_player.sql

{{ config(materialized="view") }}


with chess_elo as 
(
  select *,
  count(rating) over (order by ranking, rn) as _grp
  from {{ source('staging','players') }}
)

select
    concat(rn, "-", lower(regexp_replace(player_name, '[^A-ZÀ-Ö]', ''))) as id,
    cast(player_name as string) as player_name,
    cast(ranking as smallint) as ranking,
    cast(first_value(rating) over (partition by _grp order by ranking, rn) as integer) as rating,
    cast(play_as as string) as play_as,
    cast(opponent as string) as opponent,
    cast(opponent_rating as integer) as opponent_rating,
    cast(result as string) as result,
    cast(move as smallint) as move,
    cast(ECO as string) as ECO,
    cast(site as string) as site,
    -- {{ year_handler('year') }} as year,
    cast(date as DATE) as date,
    cast(rn as integer) as rn,
    
from chess_elo
ORDER BY ranking, rn desc
