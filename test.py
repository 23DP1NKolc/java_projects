import time
countdown_time= 60
while countdown_time >0:
    print('\033[F\033[K', end='')
    print(countdown_time)
    time.sleep(1)
    countdown_time -=1


    

