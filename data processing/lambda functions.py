from sympy import isprime,prime
from functools import reduce
from math import pow
import re

oldlist = [1,2,3,4,5,6,7,8,9,10]
wordlist = ["one","two","three","four","five","six","seven","eight","nine","ten"]
newlist = []

def search(str): #lambda function that searches for substring in list of string
	return lambda x:str.find(x)!=-1 

'''
#Map functions
newlist = list(map(lambda x:x+1 ,oldlist)) #returns x+1
newlist = list(map(lambda x:pow(x,2),oldlist)) #returns the corresponding square of integers
newlist = list(map(lambda x:prime(x),oldlist)) #returns the corresponding prime by position e.g. 2,3,5...29
newlist = list(map(isprime,oldlist)) #returns boolean list (true,false) of whether element is prime
newlist = list(map(str.upper,wordlist)) #returns fully capitalize words from wordlist
newlist = list(map(lambda x:x[:1],wordlist)) #returns first letter of words from wordlist

#Filter functions
newlist = list(filter(lambda x:not(x%3),oldlist)) #returns integers divisible by 3
newlist = list(filter(lambda x:isprime(x),oldlist)) #returns only prime integers
newlist = list(filter(lambda x:x>3,oldlist)) #returns integers greater than 3
newlist = list(filter(lambda x:search(x)("e"),wordlist)) #lambda function that searches "e" substring in string, returning only those that do
newlist = list(filter(str.isupper,wordlist)) #returns only capitalized words in list

#Reduce functions
output = reduce(lambda x,y:x+y,oldlist) #adds all integers in list
'''
newlist = list(filter(lambda x:search(x)("e"),wordlist))
print(newlist)
