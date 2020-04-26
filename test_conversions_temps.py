import datetime
import time
from pytz import timezone
# https://gist.github.com/YannBouyeron/1083709633f78e6804602a7ac6ae4bfa



heures=['00','06','12','18']
t=time.localtime()
utc=time.gmtime()
decalage=t[3]-utc[3]
print ('Decalage',decalage )


print ('utc',utc[3])

heure_grib=heures[ ((utc[3]+19)//6)%4]

print ('heure_grib',heure_grib)











a=13

b=str(a//10)+str(a%10)
print('b',b)





instant=time.time()
print()
print (' Instant en  s ',instant)

format1=time.strftime(" %d %b %Y %H:%M:%S ", time.gmtime(instant))
format2=time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(instant))

format3=time.strftime("%d-%m-%YT%H-%M-%S", time.gmtime(time.time()))
print()
print('\tFormatage 1 gmt: ',format1)
print('\tFormatage 1 local: ',format2)
print('\tFormatage 3: ',format3)

print()
t=time.localtime()
print('localtime en s : ',t)


an=t[0]
print('an',an)
mois=t[1]
print('mois',mois)
jour=t[2]
print('jour',jour)

heure=t[3]
print('heure',heure)
mn=t[4]
print('mn',mn)
sec=t[5]
print('sec',sec)

# A l'inverse

tg=time.gmtime()
heureg=tg[3]
print (' heuregmt', heureg)




t1 = time.strftime("%A %d %B %Y %H:%M:%S")
print('t1 :',t1)

time_en_s  = time.mktime((2020, 3, 29, 12, 0, 0, 0, 0, 0))

print ('time en s  pour 29 3 12 h:', time_en_s)
formate=time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(time_en_s))

print('le meme formate :',formate)

#debut du jour courant en s
t=time.localtime()
debut_jour_local=time.mktime((t[0], t[1], t[2], 0, 0, 0, 0, 0, 0))
print('\nDebut journee en s ',debut_jour_local)
formate=time.strftime(" %d %b %Y %H:%M:%S ", time.localtime(debut_jour_local))


utc=time.gmtime()
print('Decalage horaire en h',t[3]-utc[3])



print('le meme formate :',formate)

formate=time.strftime(" %d %b %Y %H:%M:%S ", time.gmtime(debut_jour_local))
print('le meme formate en UTC :',formate)

# toutes les previsions sont connues a 11 h (gfs 6z) - 17 h (12) -23h (18h)  et 5h (00)  UTC
# soit debut du jour +5*3600 modulo 6*3600

" grib valide a l'heure gmtime"



t=time.localtime()

debut_jour=time.mktime((t[0], t[1], t[2], 0, 0, 0, 0, 0, 0))


t1=time.time()
ecart=t1-debut_jour

print ('ecart',ecart/3600)
if ecart<5*3600:
    print ('gfs18')
    heure_grib=18
elif ecart<11*3600:
    print('gfs00')
    heure_grib ='00'
elif ecart < 17 * 3600:
    print('gfs06')
    heure_grib = '06'
elif ecart < 23 * 3600:
    print('gfs12')
    heure_grib = '12'
else :
    print('gfs18')
    heure_grib = '18'



a=12


heures=['06','12','18','00']
print('b',heures[((a+12)%24)//6])
print()

# tutc=time.gmtime()
# tgmt=time.gmtime()
# heuregmt=tg[3]




# on met le grib a jour aux heures suivantes en UTC
heures=['06','12','18','24']
t=time.localtime()
utc=time.gmtime()
decalage=t[3]-utc[3]
heure_grib=heures[((t[3]+decalage+11)%24)//6]
date2grib=str(t[2]//10)+str(t[2]%10)+'-'+str(t[1]//10) + str(t[1]%10)+'-'+str(t[0])+'T'+heure_grib+'-00-00'




str(a//10)+str(a%10)



print(decalage)
print('heure dernier grib disponible',heure_grib)
print(date2grib)









# heures=['06','12','18','00']
# heure_grib=heures[((t[3]+12)%24)//6]
#
#
#
#
print('Decalage horaire',t[3]-utc[3])

