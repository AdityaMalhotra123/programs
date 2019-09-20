#include <cs50.h>
#include <stdio.h>
#include <math.h>


int main(void)
{
    float amount;
    do
    {
        printf("O hai! How much change is owed?\n");
        amount = get_float();
    }
    while(amount < 0);
    
    amount *= 100;
    amount = (int) round(amount);
    int coins = 0;
    
    while(amount >= 25)
    {
        coins += 1;
        amount -= 25;
    }
    while(amount >= 10)
    {
        coins += 1;
        amount -= 10;
    }
    while(amount >= 5)
    {
        coins += 1;
        amount -= 5;
    }
    while(amount >= 1)
    {
        coins += 1;
        amount -= 1;
    }
    printf("%i\n", coins);
    
}