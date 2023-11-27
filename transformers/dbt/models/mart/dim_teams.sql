with
soccer_matches_pivoted as (

    select * from {{ref('int_soccer_matches_pivoted')}}

),

distinct_teams as (

    select distinct team from soccer_matches_pivoted

),

final as (

    select
        row_number() over(order by team asc) as team_id,
        team

    from distinct_teams

)

select * from final
