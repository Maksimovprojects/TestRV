# TestRV
I divided task on 7 independent test cases.
Each test case is isolated and does not rely on each other.
As the environment, you have to install: python, selenium, terminal, or IDE, unit test is enough to run tests.
I didn't use any 'fixtures' to simplify running, used simple construction without wrapping into try/except/finally, without handling Exceptions



1. Check that the AMEX banner is displayed at the top of the page.
There are a few approaches to do that:
 - find the coordinate of the web element(banner) by using the 'location' of the AMEX banner.
The position on the top of the page is related by 'y' value. So, the position by height is based on the 'y' value. I implemented an 'if' statement to make sure that the location of the AMEX banner won't be changed
 -  As I said before, we have a few approaches to do define that, the second approach is using xPath, to define location related to subsequent elements(ancestors). But I chose the first approach, because the structure of the page may be changed, that is the sequence of elements on the page could be also changed. 
That is one of the benefits of xPath, to be able to traverse up the DOM tree to parent elements. 

2. Check that the Login button directs to the member login page.
In this case, we have to switch between two tabs and catch 'title' and 'current_url' one of the tab, after that comparing the actual and expected result

3. Check that 'card images' are displayed beside the 'form'.
Not clear definition of the word 'beside'. 'Beside' on the page or 'beside' in  DOM document tree? 
 - if in test the word 'beside' means nearness element to each other by location on the page, I'll use 'location' by 'Y-axis of each element 'card images' and "form",  then compare values 'Y' of by location attribute. 
 -  if in test the word 'beside' means element 'card images' next to "form" by DOM tree, I'll use ancestor approach (element1 / element2 ...) by using CSS
selectors bounded by absolute path('form > aside > img'). If the structure of the DOM tree will be changed, the error will be caused, and test fall. Implemented that solution


4. Check that FAQ section accordion tabs expand.
I check expected conditions is element clickable, after that, I handle all elements(3) by for loop and click on them: expand/collapse


5. Check that the footer is displayed.
I scrolled to the end of the page, find the 'footer' locator, and check by using the 'expected conditions' 'wrapper' method. 


6. Enter test data into form:
I find locators of required fields and fill them by using the 'send_keys' method, by using 'Select' class from 'Webdriver' library I choose 'New York' value assign it to variable 'select' by visible text, but there is another way to do it by using indexing of value.
To make assertions I have to retrieve value from each attribute by using get_property("value") and comparing it with passed data into fields.


7. Click “View my Card Offers” and expect the results page to be visible.
You won't be able to interact with the element “View my Card Offers” button until you fill all required fields. So test case 6 is a precondition for test case 7.
I also could pull out 'filling fields' as a 'fixture' method and invoke it before the two last test cases
