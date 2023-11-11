with
soccer_matches_pivoted as (

    select * from {{ref('int_soccer_matches_pivoted')}}

)

select * from soccer_matches_pivoted
