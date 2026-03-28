-- explain analyze
select * from quest;
select * from term_dict;

-- Случайное количество записей
with ids as (
    select distinct floor(random() * (select max(id) from quest) + 1)::int as target_id
    from generate_series(1, 20)
)
select q.* 
from quest q
join ids on q.id = ids.target_id
limit 5;

select 
random() * (select max(id) from quest) rnd_id,
floor(random() * (select max(id) from quest) + 1)
from generate_series(1, 20);