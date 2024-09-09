select * from formations f 

update formations set name = 'DEV (DLOG; DA)' where id = 118

delete from formations where id = 119

select formation_id,name from files where formation_id in(118,119)

update files set formation_id = 118 where formation_id = 119