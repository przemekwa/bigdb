CREATE TABLE HOUSE(
   LINK           TEXT    NOT NULL,
   SITE            TEXT     NOT NULL,
   NICK        TEXT     NOT NULL,
   AGE         INT     NOT NULL,
   PRICE         INT     NOT NULL,
   WEIGHT         INT     NOT NULL,
   HEIGHT         INT     NOT NULL
)


-- Query

select max(link), price, weight, height,age from house where site='Poznań' group by price, weight, height,age

select * from (select max(link), price,  height,age from house where site='Poznań' group by price,  height,age);

-- grouop by age
select age, count(*) from (select max(link), price,  height,age from house where site='Poznań' group by price,  height,age) group by age order by age;