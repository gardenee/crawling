create table store (
    store_no number not null
    ,menu_2nd_cate_no number not null
    ,store_name varchar2(50) not null
    ,store_x number(38) not null
    ,store_y number(38) not null
    ,store_road_address varchar2(500)
    ,store_old_address varchar2(500)
    ,store_opening_hours varchar2(500)
    ,stroe_visit_count number
)
