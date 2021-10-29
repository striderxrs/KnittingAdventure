
**Prologue - Wollplatz webscraper**


Given the problem, first step after reading related materials and trying out some sample scripting examples
was to look at the website  - 'www.wollplatz.de' in detail to observe what information is available readily
(the website layout, inspect element and page source)


**Initial try:**
 
Used Selenium webdriver to open up an automated window of chrome browser to send a search query, observing
how the url changed w.r.t the query.

Then modified the search term to match the url format. The idea was to save a list of search terms in a file
then access them through a loop, changing the URL each time the loop runs to indicate to our next product.

Progress is slow and cumbersome because of the extra browser windows opening and closing every-time the code is executed.
Decided to go for another approach with requests instead.


**Second Try:**

Switched the URL maker idea out in favor of a csv file containing the url's of required products.

Using requests, able to eliminate the browser window problem, figured that the table information was gettable by using soup.find() on a div class 3 levels above the table itself.

To Format the text data: used the index to identify position of required values and extract them into a list.

Called the csv function to write to a file the information that was retrieved.

Called the csv file in a loop to append information to the output file.

Possible grievance: The information related to delivery time was'nt readily available unless I have an account and an address locally in DE 
and even in that case I did'nt find that information until I placed an order. 
This is unlike Amazon which provides an option to insert your postcode and estimates delivery times. 


**Database:**

Initially tried to use MS Access, turned out to be a bit not too friendly. Switched to sqlite3 for ease of use.

**What can be improved:**

- The file containing urls to be parsed being actual text terms and requiring a text to address format substitution.
- Adding another website to the mix to compare prices and sort by price for a given product. Scaling at the moment can be done by writing 
another module to the tune of the next website and calling the subroutine through the main for loop.
- Support for browser view of csv file or an output file that is compatible with browser for easy access.
- Adding more test cases and exceptions to be caught, right now only timeout is being caught.
- In addition to this, a login prompt which automatically logs in the user account to purchase(requires relevant information)
- Writing GUI/UX elements for ease of use. 

 
**Some References used:**

https://ieeexplore.ieee.org/abstract/document/8821809

https://www.sqlitetutorial.net/

https://stackoverflow.com/

https://www.sqlite.org/docs.html

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

https://docs.python-requests.org/en/latest/

https://www.selenium.dev/documentation/

and of course, youtube tutorials.
