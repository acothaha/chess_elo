{{ config(materialized="table") }}


with chess_player as (
    select *
    from {{ ref('stg_chess_players') }}
),

ECO_referece as (
    select *
    from {{ ref('stg_ECO_reference') }}
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
    ECO_referece.name,
    ECO_referece.opening_moves,
    chess_player.site, 
    chess_player.year,
    chess_player.rn
from chess_player
    LEFT JOIN ECO_referece ON chess_player.ECO = ECO_referece.eco_code
