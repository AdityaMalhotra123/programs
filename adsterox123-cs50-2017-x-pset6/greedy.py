while True:
    amount = float(input("How much change is owed "))
    if (amount >= 0):
        break


amount = amount * 100;
amount = round(amount, 0);
coins = 0;

while amount >= 25:

    coins = coins + 1;
    amount = amount - 25;

while amount >= 10:

    coins = coins + 1;
    amount = amount - 10;

while amount >= 5:

    coins = coins + 1;
    amount = amount - 5;

while amount >= 1:

    coins = coins + 1;
    amount = amount - 1;

print(coins)