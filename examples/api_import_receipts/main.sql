select
	cs.cashnum as cash_id,
	cp.numberfield as check_id,
	to_char(cs.shiftopen,'YYYY-MM-DD') as check_date,
	ch.item as ware,
	sum(case 
		when ch.precision < 1 then ch.qnty * ch.precision
		else ch.qnty / 1000
	end) as ware_amount
from ch_shift cs
left join ch_purchase cp on cp.id_shift = cs.id 
left join ch_position ch on cp.id = ch.id_purchase 
where 
	cp.datecommit >= current_timestamp - interval '5 minute'
	and cp.cashoperation = 0
group by 
	cs.cashnum,
	cs.shiftopen,
	cp.numberfield,
	ch.item