/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    int first = 0;
    int last = n - 1;
    for (int a = 0; a < n; a++)
    {
        int mid = (first + last)/2;
        if (values[mid] == value)
        {
            return true;
        }
        else if (values[mid] < value)
        {
            first = mid + 1;
        }
        else if (values[mid] > value)
        {
            last = mid - 1;
        }
        if (first > last)
        {
            return false;
        }
    }
    
    // TODO: implement a searching algorithm
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    for (int b = 0; b < (n - 1); b++)
    {
        for (int c = 0; c < n - b - 1; c++)
        {
            if (values[c] > values[c + 1])
            {
                int swap = values[c];
                values[c] = values[c + 1];
                values[c + 1] = swap;
            }
        }
    }
    // TODO: implement an O(n^2) sorting algorithm
    return;
}
