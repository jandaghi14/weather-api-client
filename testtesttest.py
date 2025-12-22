from datetime import datetime , timedelta

import time


# now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
# print(now)
# time.sleep(2)
# b = datetime.strptime(now,"%d/%m/%Y, %H:%M:%S")

# after = datetime.now()

# print(after - b)
# if after - b >= timedelta(seconds=2):
#     print("aaa")
# else:
#     print("bbb")

# print(b)

def test():
    print("a")

def testzzz():
    for i in range(3):
        try:
            a = int(input())
            a=a-1
            return test()
        except Exception as e:
            print("rr")

testzzz()
