# coding=utf-8
def deleteReoccurringCharacters(string):
    seenCharacters = set()
    outputString = ''
    for char in string:
        if char not in seenCharacters:
            seenCharacters.add(char)
            outputString += char
    return outputString


"""Because of the way a set works in memory, it has a lookup time complexity of 0(1)"""

"""This means we can use it to check whether or not we have already visited a character"""

"""Time Complexity
Iterating through the entire input string has a time complexity of O(n), since there are n characters in the string itself.

For each of those characters, we have to check whether or not we have seen the… However, 
since a HashSet has a lookup time of O(1), 
our time complexity is not impacted.

Leaving us with a final time complexity of O(n)."""

"""Space Complexity
Worst case scenario, we get a string with all unique characters. For example, “abcdef”.

In that case, we would store all n elements in our string and our set.

However, we’re also limited to size of the english alphabet.

This is a good chance to ask our interviewer what type of characters count as unique in the string (uppercase / lowercase / numbers / symbols).

Assuming that the initial string will contain lowercase letters from the alphabet, since the alphabet is finite, 
our set and output string can never be bigger than 26 characters.

Leaving us with a worst case scenario space complexity of O(1)."""


print(deleteReoccurringCharacters('aaAA'))


"""In python, a dictionary can only hold a single value for a given key. However, if you use a relevant data type for that value, you should be able to save multiple values for a single key.

Option 1: Use a tuple to represent the value of the key.

var my_dict = {
	"my_key": (value_1, value_2, value_3)
};
print (my_dict["my_key"][0]) // This will print value_1
print (my_dict["my_key"][1]) // This will print value_2

Option 2: Use a list (array) to represent the value of the key.

var my_dict = {
	"my_key": [value_1, value_2, value_3]
};

print (my_dict["my_key"][0]) // This will print value_1
print (my_dict["my_key"][1]) // This will print value_2
Option 3: Use another dictionary to represent the value of the key.

var my_dict = {
	"my_key": {
		"key_1": value_1, 
		"key_2": value_2
	}
};
print (my_dict["my_key"]["key_1"]) // This will print value_1
print (my_dict["my_key"]["key_2"]) // This will print value_2
Hope this helps !!"""
