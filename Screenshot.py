import pyautogui, time, datetime
time.sleep(2)
t = 0
print(t)
count = 0
while count < 15:
    if pyautogui.pixel(8,475)[0] == 222:
        if t == 0: t = datetime.datetime.now()
        time.sleep(1)
        count += 1

print((datetime.datetime.now()-t)/15)






