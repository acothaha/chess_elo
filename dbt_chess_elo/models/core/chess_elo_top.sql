{{ config(materialized="table") }}


with chess_player as (
    select *
    from {{ ref('stg_chess_players') }}
)

select
    chess_player.id, 
    chess_player.player_name, 
    chess_player.ranking, 
    chess_player.rating, 
    chess_player.play_as, 
    chess_player.opponent, 
    chess_player.opponent_rating, 
    chess_player.result, 
    chess_player.move, 
    chess_player.site, 
    chess_player.date,
    chess_player.rn
from chess_player
