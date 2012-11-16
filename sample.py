# To use the Face API in your code, just import the generated code
# add your developer key (you can find it in your dashboard: http://www.mashape.com/account/index )
# and relax!
# This is a sample of the initialization of the client.. then call its methods!


from Face import Face

# basic instantiation. TODO Put your authentication keys here.
client = Face("1vgorh7zmjvdnjq2xjwqq6xnwm6xa4", "zhyjc7xytpu3rcwjy3akzzqiirb3ev")


api.detect(urls="http://www.lambdal.com/test2.jpg")

# A sample function call. These parameters are not properly filled in.
# See Face.py to find all function names and parameters.
response = client.detect(images='http://www.taipeitimes.com/images/2012/11/08/thumbs/P03-121108-1.jpg')

# now you can do something with the response.
print vars(response)
