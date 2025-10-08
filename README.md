#### SnipeIT API scraper for usernames and asset details


Monthly asset reviews getting you down? Spending hours trawling through Snipe to find assets and chase down users? Well no more. With this handy dandy little script you can pop your users usernames directly into an
excel sheet and have snipe pull everything you want about them!

if like me your users are firstname.lastname types, you can use this formula to automatically convert Full Name to username:

```
=LOWER(LEFT(B2,FIND(" ",B2)-1) & "." & RIGHT(B2,LEN(B2)-FIND(" ",B2)))
```
Stick that in A2-11, (Header should be Username in A1, Full name in B1) and then just copy/paste however many names you have to do each month into B2+ and watch it work.
(script is set up to do 10 at once as thats the monthly quota for me. Youll need to change this if you only want to do 1 or 2, but if its only 1 or 2 what are you doing here??)

Make sure you are CD'd into the folder your script and users.xlsx files are chilling and run via your preferred IDE. Should come back with a new excel with all the goodies you need.

Have fun with those extra couple hours in the day
