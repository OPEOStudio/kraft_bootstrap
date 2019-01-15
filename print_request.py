import requests
import json

### PRINT THE REQUEST
# Script to print the request, to make sure that all the right request elements are being sent
# DOESN'T WORK FOR NOW

def print_r(string, url, data, headers, params):
	# Put headers, params back into dictionnary
	#print("headers: "+headers) ## Allowed me to test that headers is well a dict right now
	#headers_dict = json.loads(headers)
	#params_dict = json.loads(params)

	print("headers : "+str(headers))

	# Define the Request object
	request = requests.Request(string, url, data = data, headers = headers, params = params)

	print("request: "+str(request))

	# Prepare the request
	prepared = request.prepare()

	# Calls the printing step
	pretty_print_POST(prepared)


def pretty_print_POST(request):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print(" ")
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body,
    ))


