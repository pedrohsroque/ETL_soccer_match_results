with
source as 
(

    select
        lpad(
            round,
            2,
            '0'
        ) as round,
        concat(
            lpad(
                round,
                2,
                '0'
            ),
            '_',
            lpad(
                cast( row_number() over(partition by round) - 1 as text ),
                2,
                '0'
            )
         ) as match_id,
        to_timestamp(date_time, 'YYYY-MM-DD/THH24:MI') as date_time,
        teams,
        case
            when result = '' then null
            when result = 'None x None' then null
            else result
        end as result

    from {{ source( 'raw', 'campeonato_brasileiro_serie_a_2023' ) }}

)

select * from source
