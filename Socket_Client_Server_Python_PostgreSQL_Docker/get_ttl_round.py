def round_ttl(ttl):
	'''Расчет ttl'''
	res=round(ttl/60)
	if res<4:
		return res+3
	else: return 4