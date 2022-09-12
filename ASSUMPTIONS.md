# List of Assumptions
*Write your assumptions here*

1). If user has access to the internet he/she can run this program.

2). If user does not have an account with CryptoWatch they can still access the API.

3). If user uses the API for a multiple amount of times without using an account the API will deny access to get data for an x amount of hours.

4). The csv file can only be created using Python 3.6.5. (this was noticed as when using Python 3.9 as the interpreter for a test, csv file wasn't being created. This issue was resolved when reverting back to the original interpreter used in the beginning which was Python 3.6.5)