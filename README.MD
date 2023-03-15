# What can be optimized?
1. This app is using Django and one of the main task of it is to extract characters from 3rd party API, which is an I/O operation. This is a perfect task for using asyncio and AioHttp framework. I did async calls in Django but support of it is limited. With average 10 calls performance optimization is twice - from 4s to 2 s. I also tried to do 82 requests for each character synchronously and asynchronously and time saving almost 6 times (from 17 sec to 3.7 sec)
2. For sake of simplicity here is used sqlite database which is not suitable for production - in production should be changed to postgres or mongodb as there is no relations support is needed and mongo will be faster in this case.
3. Also according to good coding style business logic should be moved out of views to prevent their extention.
4. This code should be revised for errors possible and add logging
5. Add code and formatting checkers like mypy, blake of flake8, isort etc. 
6. In normal situation files should never be saved in application - but moved to some files storage
