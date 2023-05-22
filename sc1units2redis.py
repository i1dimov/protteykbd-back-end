import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

r.set('ProtossAirUnits', 'Observer,Shuttle,Scout,Carrier,Carrier\'sInterceptor,Arbiter,Corsair')

print(r.get('ProtossAirUnits'))