with
stg as (

    select * from {{ref('stg_raw__soccer_matches')}}
    --where result != ''

),

splited as (

    select
        round,
        match_id,
        date_time,
        split_part(teams,' x ', 1) as home_team,
	    split_part(teams,' x ', 2) as away_team,
	    cast( split_part(result,' x ', 1) as int ) as home_goals,
	    cast( split_part(result,' x ', 2) as int ) as away_goals

    from stg

),

add_stats as (

    select
        *,
        case
            when home_goals > away_goals then 'W'
            when home_goals = away_goals then 'D'
            when home_goals < away_goals then 'L'
            else null
        end as home_result,
        case
            when home_goals > away_goals then 3
            when home_goals = away_goals then 1
            when home_goals < away_goals then 0
            else null
        end as home_points,
        home_goals - away_goals as home_goal_difference,
        case
            when away_goals > home_goals then 'W'
            when away_goals = home_goals then 'D'
            when away_goals < home_goals then 'L'
            else null
        end as away_result,
        case
            when away_goals > home_goals then 3
            when away_goals = home_goals then 1
            when away_goals < home_goals then 0
            else null
        end as away_points,
        away_goals - home_goals as away_goal_difference,
        concat(home_team, ' ', home_goals, ' x ', away_goals, ' ', away_team) as label

    from splited

),

home_info as (

    select
        round as round,
        match_id,
        date_time as date_time,
        'H' as home_or_away,
        home_team as team,
        home_goals as goals,
        home_result as result,
        home_goal_difference as goal_difference,
        home_points as points,
        label as label

    from add_stats

),

away_info as (

    select
        round as round,
        match_id,
        date_time as date_time,
        'A' as home_or_away,
        away_team as team,
        away_goals as goals,
        away_result as result,
        away_goal_difference as goal_difference,
        away_points as points,
        label as label

    from add_stats

),

pivoted as (

    select * from home_info
    union all
    select * from away_info

),

final as (

    select * from pivoted

)

select * from final
