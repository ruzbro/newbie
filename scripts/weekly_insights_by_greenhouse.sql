-- Calculate potential revenue by crop based on the formula:
-- estimated week revenue = total kg harvested * price per kg
-- (note that there are various price categories based on customer)
with q1 as (
  select 
    cs.primary_resource_tag as resource_tag, cs.crop_name, 
    -- TO_CHAR(cc.harvest_date::date, 'Mon-DD Dy') as harvest_date,
    cc.harvest_week_num,
    TO_CHAR(cc.harvest_date::date, 'YYYY-IW') as harvest_yyyy_iw,
    TO_CHAR(cc.harvest_date::date, 'Mon-DD Dy')||'-w'||RIGHT(cc.harvest_week_num::text, 2) as harvest_week,
    cs.current_weekly_harvest_kg * "price_b2b_B" as b2b_b_target_revenue,
    cs.current_weekly_harvest_kg * "price_hotel_B" as hotel_b_target_revenue,
    ROUND(cc.kg_harvested * "price_b2b_B") as b2b_b_harvest_revenue,
    ROUND(cc.kg_harvested * "price_hotel_B") as hotel_b_harvest_revenue,
    cs.current_weekly_harvest_kg as target_kg, 
    cc.kg_harvested,
    ROUND(((cc.kg_harvested - cs.current_weekly_harvest_kg) / cs.current_weekly_harvest_kg)::numeric * 100, 2) as pct_of_target_kg,
    cs.unit_weight_target_g as target_unit_g, 
    ROUND((cc.kg_harvested * 1000.0)::numeric / NULLIF(cc.units_harvested, 0), 2) as harvest_unit_g,
    ROUND(((ROUND((cc.kg_harvested * 1000.0)::numeric / NULLIF(cc.units_harvested, 0), 2) - cs.unit_weight_target_g) / 
      cs.unit_weight_target_g)::numeric * 100, 2) as pct_of_target_unit_g
  from crop_stats as cs
  join crop_calendar as cc on cs.crop_id = cc.crop_id
  where (cs.primary_resource_tag = $1 or $1 = 'all' or $1 = '')
    and (NOT (cs.crop_id = ANY($2)))
    -- primary_resource_tag = 'GH2'
    and cc.kg_harvested is not null
),
q2 as (
  select *, 
  TO_CHAR((CURRENT_TIMESTAMP AT TIME ZONE 'UTC' + INTERVAL '8 hours'), 
          'YYYY-IW') as current_week
  from q1
)
select *
from q2
where harvest_yyyy_iw <= current_week
order by crop_name, harvest_week_num