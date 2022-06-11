# from django.test import TestCase

# Create your tests here.
# import random
# password = "1869"
# attempt = 0
# while True:
#     p = ""
#     for i in range(4):
#         rand_int = random.randint(1,9)
#         p += str(rand_int)
#         print(p)
#     attempt += 1
#     if p == password :
#         print(attempt , "urinis hda topildi parol =", p )
#         break
#     else:
#         print("oxshamadi", attempt)

# import random
# password = "18699886"
#print( len(password))


# attempt=0
# p=''
# index=1
# for i in range(1000000):
#     #print(attempt)
  
#     while True:
#         r=str(random.randint(0, 9))
#         if attempt > (len(password)-1):
#             break
        
#         elif password[attempt]==r:
#             p+=r
#             attempt+=1
#             index+=1
# print(p)
            

# Program to generate a random number between 0 and 9

# importing the random module
import random

print(random.randint(0,9))