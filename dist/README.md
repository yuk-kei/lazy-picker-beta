# Lazy Picker - Beta Release v2

## Overview of tasks completed

- [x] Order list can be inputted directly by user or via uploading file, paste list manually and enter order one by one.
- [x] Implement repetitive nearest neighbor (doing nearest neighbor for all nodes) for multiple access points
- [x] The timeout should no longer be hardcoded to 1 minute. It will be a specified by the user via a menu setting in seconds (can be decimal/fractions of a second - i.e. 1, 60, 0.25, etc)
- [x] Allow user to configure their start locations at any time
- [x] If database or input file not exit, the program would not crash and allow user to select file through file picker
- [x] If there is an issue with an invalid user input, such as character instead of numbers, the program should not crash
- [x] If there is an issue with calculating the route (say there is an item that doesn't exist), the program should not crash, but simply not doing anything
- [x] Allow user to export directions to a .txt file (and append multiple order directions)
- [x] Enhanced UI(loading scene and colored map)

## known bugs/errors

- Can not check whether the worker start location is conflicted with  shelves' locations
- Can not generate optimal path for branch-and-bound in multiple access points
- Can not set the destination