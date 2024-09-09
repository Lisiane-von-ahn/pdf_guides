select * from formations 

update formations set name= 'DATA (DATA_IA ; DATA_S)' where id = 114

delete from formations where id = 116

select formation_id, name from files where formation_id in (114,116)

update files set formation_id= 114 where formation_id = 116