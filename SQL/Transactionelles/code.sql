update t set a=a+1;

update t set b=42 where a=1;
SELECT * from t where a=2;
update t set b=42 where a=2;

commit;
ROLLBACK;
SELECT * from t;
insert INTO t values(3,3);
delete from t where b=3;
SELECT * from t WHERE a=2;
ALTER TABLE t ADD PRIMARY KEY (a);

select * from t where b=1;
update t set b=10 where b=1;
