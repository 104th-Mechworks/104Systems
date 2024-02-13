# # # lst = [1,2,2,3,4,5,6,7,8,9]
# # # print(set(lst))
# # # print(max(set(lst), key=lst.count))
# # #
# # # # # insomnia passphrase: the debt that all men pay
# # #
# # # # convert 0b01000000000000000000 to decimal
# # # b = 549755813888
# # # print(bin(b))
# # # print(int(b))
# # # print(len('1000000000000000000000000000000000000000'))
# # from functools import cache
#
#
#
# # # def sieve_of_eratosthenes(limit):
# # #     primes = []
# # #     is_prime = [True] * (limit + 1)
# # #     is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime numbers
# # #
# # #     for number in range(2, int(limit**0.5) + 1):
# # #         if is_prime[number]:
# # #             primes.append(number)
# # #             for multiple in range(number * number, limit + 1, number):
# # #                 is_prime[multiple] = False
# # #
# # #     for number in range(int(limit**0.5) + 1, limit + 1):
# # #         if is_prime[number]:
# # #             primes.append(number)
# # #
# # #     return primes
# # #
# # #
# # # def prime_factor(number, primes):
# # #     for n in primes:
# # #         if number % n == 0:
# # #             new_number = num // n
# # #             print(n)
# # #             return new_number, n
# # #
# # #
# # # def remove_excess(primeslist: list, n):
# # #     primeslist.sort(reverse=True)
# # #     for p in primeslist:
# # #         if p > n:
# # #             primes.remove(p)
# # #     return primes
# # #
# # #
# # # num = int(input("enter a number"))
# # # pf = []
# # # primes = sieve_of_eratosthenes(num)
# # # primes.reverse()
# # # new_num, pfn = prime_factor(num, primes)
# # # pf.append(pfn)
# # # primes = remove_excess(primes, new_num)
# # #
# # #
# # # while new_num != 0:
# # #     new_num, pfn = prime_factor(num, primes)
# # #     primes = remove_excess(primes, new_num)
# # #     pf.append(pfn)
# # #     if new_num in primes:
# # #         pf.append(new_num)
# # #         break
# # #
# # # print(f"prime factor decomposition of {num} is: {pfn}")
#
# # def sieve_of_eratosthenes(limit):
# #     primes = []
# #     is_prime = [True] * (limit + 1)
# #     is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime numbers
#
# #     for number in range(2, int(limit**0.5) + 1):
# #         if is_prime[number]:
# #             primes.append(number)
# #             for multiple in range(number * number, limit + 1, number):
# #                 is_prime[multiple] = False
#
# #     for number in range(int(limit**0.5) + 1, limit + 1):
# #         if is_prime[number]:
# #             primes.append(number)
#
# #     return primes
#
#
# # def prime_factor(number, primes):
# #     for n in primes:
# #         if number % n == 0:
# #             new_number = number // n
# #             print(n)
# #             return new_number, n
# #     return None, None  # Return None if no prime factor is found
#
#
# # def remove_excess(primeslist: list, n):
# #     return [p for p in primeslist if p <= n]
#
#
# # num = int(input("enter a number: "))
# # pf = []
# # primes = sieve_of_eratosthenes(num)
# # primes.reverse()
#
# # while num != 0:
# #     new_num, pfn = prime_factor(num, primes)
# #     if new_num is None:
# #         break  # Break the loop if no prime factor is found
# #     primes = remove_excess(primes, new_num)
# #     pf.append(pfn)
# #     num = new_num
#
# # print(f"prime factor decomposition of {num} is: {pf}")
#
#
# text = input("enter a string: ")
#
#
#
#
#
# def check(text: str):
#     # check if all the characters are unique
#     unique = True
#     for i in text:
#         if text.count(i) > 1:
#             unique = False
#             break
#     if len(text) < 5 or len(text) > 7:
#         print("wrong length")
#         return False
#     if text.upper() != text:
#         print("all uppercase")
#         return False
#     if sum(text.encode("ascii")) > 600 or sum(text.encode("ascii")) < 350:
#         print(sum(text.encode("ascii")))
#         return False
#     if unique == False:
#         print("not unique")
#         return False
#     return True
#
#
# valid = False
# while valid == False:
#     valid = check(text)
#     if valid == False:
# #         text = input("enter a string: ")
# #     else:
# #         print("valid")
# #         break
# role = {
#     "anti_armour": 0b100000000,
#     "anti_armour_instructor": 0b1000000000,
#     "advanced_anti_armour": 0b10000000000,
#     "advanced_anti_armour_instructor": 0b100000000000,
#     "anti_armour_cadre": 0b1000000000000,
#     "advanced_marksman_instructor": 0b1000000000000000000,
#     "head_anti_armour_cadre": 0b10000000000000
# }
# s=0
# for v in role.values():
#     s += v
#
# from Bot.utils.kmcbitroles import RoleSwitcher
#
# rs = RoleSwitcher.decode(s)
#
# def kmcsort(elem):
#     keywords = [
#         ('Head Cadre', 5),
#         ('Cadre', 4),
#         ('Advanced Instructor', 3),
#         ('Instructor', 2),
#         ('Advanced', 1),
#     ]
#
#     matches = [(priority, keyword) for keyword, priority in keywords if keyword in elem]
#
#     if matches:
#         # Sort matches by keyword length in descending order
#         matches.sort(key=lambda x: len(x[1]), reverse=True)
#         return matches[0]
#
#     return (0, elem)
#
# def kmcsortlist(lst) -> list:
#     return list(reversed(sorted(lst, key=kmcsort)))
#
# print(rs)
# kmcsortlist(rs)
