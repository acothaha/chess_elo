-- stg_chess_player.sql

{{ config(materialized="view") }}


with chess_elo as 
(
  select *,
  from {{ source('staging','players') }}
)

select
    cast(player_name as string) as player_name,
    cast(ranking as smallint) as ranking,
    cast(rating as integer) as rating,
    cast(play_as as string) as play_as,
    cast(opponent as string) as opponent,
    cast(opponent_rating as integer) as opponent_rating,
    cast(result as string) as result,
    cast(move as smallint) as move,
    cast(ECO as string) as ECO,
    cast(site as string) as site,
    cast(year as smallint) as year

from chess_elo