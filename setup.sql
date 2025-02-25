//SQL used to set up data and coursework for https://learn.snowflake.com/en/courses/OD-ESS-DABW/

CREATE or replace TABLE "SMOOTHIES"."PUBLIC"."FRUIT_OPTIONS" (fruit_id VARCHAR, fruit_name VARCHAR); 

create or replace file format smoothies.public.two_headerrow_pct_delim
	TYPE=CSV
    SKIP_HEADER=2
    FIELD_DELIMITER='%'
    TRIM_SPACE=TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY='"'
    REPLACE_INVALID_CHARACTERS=TRUE
    DATE_FORMAT=AUTO
    TIME_FORMAT=AUTO
    TIMESTAMP_FORMAT=AUTO; 

SELECT $1, $2
	FROM '@smoothies.public.my_uploaded_files/fruits_available_for_smoothies.txt'
(FILE_FORMAT => smoothies.public.two_headerrow_pct_delim);

COPY INTO smoothies.public.fruit_options
from @smoothies.public.my_uploaded_files
files = ('fruits_available_for_smoothies.txt')
file_format = (format_name = smoothies.public.two_headerrow_pct_delim)
on_error = abort_statement
validation_mode = return_errors
purge = true;

COPY INTO smoothies.public.fruit_options
from (select $2, $1
FROM '@smoothies.public.my_uploaded_files/fruits_available_for_smoothies.txt')
file_format = (format_name = smoothies.public.two_headerrow_pct_delim)
on_error = abort_statement
purge = true;

select * from smoothies.public.fruit_options

COPY INTO "SMOOTHIES"."PUBLIC"."FRUIT_OPTIONS" 
FROM (SELECT $1, $2
	FROM '@smoothies.public.two_headerrow_pct_delim') 
FILES = ('2025-01-30T09:33:58.633Z/fruits_available_for_smoothies.txt') 
FILE_FORMAT = '"SMOOTHIES"."PUBLIC"."temp_file_format_2025-01-30T09:35:09.777Z"' 
ON_ERROR=ABORT_STATEMENT 
-- For more details, see: https://docs.snowflake.com/en/sql-reference/sql/copy-into-table

create table smoothies.public.orders (ingredients varchar(200))

alter table smoothies.public.orders add column name_on_order varchar(100);
alter table smoothies.public.orders add column order_filled boolean default false;

       update smoothies.public.orders
       set order_filled = true
       where name_on_order is null;


truncate SMOOTHIES.PUBLIC.ORDERS 

alter table SMOOTHIES.PUBLIC.ORDERS 
add column order_uid integer --adds the column
default smoothies.public.order_seq.nextval  --sets the value of the column to sequence
constraint order_uid unique enforced; --makes sure there is always a unique value in the column


create or replace table smoothies.public.orders (
       order_uid integer default smoothies.public.order_seq.nextval,
       order_filled boolean default false,
       name_on_order varchar(100),
       ingredients varchar(200),
       constraint order_uid unique (order_uid),
       order_ts timestamp_ltz default current_timestamp()
);

set mystery_bag = 'What is in here?';
select $mystery_bag;

set mystery_bag = 'This bag is empty!!';
select $mystery_bag;

create or replace function sum_mystery_bag_vars(var1 number, var2 number, var3 number) 
    returns number as 'select var1+var2+var3';

select sum_mystery_bag_vars(2, 4, 7);

select NEUTRALIZE_WHINING('do Re mE')

create function util_db.public.NEUTRALIZE_WHINING(input varchar)
    returns text as 'select initcap(input)'


select neutralize_whining('aBCD')

select * from smoothies.public.fruit_options limit 10
alter table smoothies.public.fruit_options add column search_on varchar
update smoothies.public.fruit_options set search_on='apple' where fruit_name='Apples';
update smoothies.public.fruit_options set search_on='blueberry' where fruit_name='Blueberries';
update smoothies.public.fruit_options set search_on='jack_fruit' where fruit_name='Jackfruit';
update smoothies.public.fruit_options set search_on='raspberry' where fruit_name='Raspberries';
update smoothies.public.fruit_options set search_on='strawberry' where fruit_name='Strawberries';
