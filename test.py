import HiveClient as hc

hcon = hc('10.141.212.26', 'pcb', '10000' )
res = hcon.query("select * from spi LIMIT 10")
print(res)