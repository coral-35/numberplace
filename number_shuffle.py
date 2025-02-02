import random

for n in range(1,10):
    # 1～9の重複のない並び替えを生成
    numbers = list(range(9))
    random_i = random.sample(numbers, 2) 
    print(random_i)