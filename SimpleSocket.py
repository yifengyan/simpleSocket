#!/usr/bin/python

import socket, sys, ssl

#Required Constants for the program.
courseName = 'cs5700fall2016'
neuID = sys.argv[-1]
hostName = sys.argv[-2]

'''
This function will receive response data from the Connection() function and split it.
If BYE flag is found in the message it will print the Secret flag and exit,
otherwise it'll do all the arithmetic operations specified in the project requirements.  
'''
def getSolution(response):

    res=response.replace('\n', '').split(" ")
    firstNumber=res[2]
    if firstNumber == 'BYE':
        print res[1]
        exit()
    operator=res[3]
    secondNumber=res[4] 
    
    result=None
    if operator == '+':
        result = int(firstNumber)+int(secondNumber)
    elif operator == '-':
        result = int(firstNumber)-int(secondNumber)
    elif operator == '*':
        result = int(firstNumber)*int(secondNumber)
    elif operator == '/':
        result = int(firstNumber)/int(secondNumber)
    return result

'''
This function will establish the connection between the Client and the Server.
It'll create an SSL connection if -s is found in the command argument, otherwise a non-SSL one.
It'll update the port number if -p is found in the command argument, otherwise the default port number
will be used to establish the connection. 
If the port number is not equal to 27993 with TCP connection or is not equal to 27994 with SSL connection, it will print out an error and stop the program.
It'll also receive the response data from the Server and send it to getSolution() function  for further analysis.  
'''   
def connection():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sslExist=None
    portExist=None
    portNumber=27993
    try:
        portExist=sys.argv.index('-p')
    except:
        portExist=-1
    if portExist!=-1:
        portNumber=sys.argv[portExist+1]
    try:
        sslExist=sys.argv.index('-s')
    except:
        sslExist=-1
    if sslExist!=-1:
        soc = ssl.wrap_socket(soc)
        if portExist!=-1 and portNumber!=27994:
            print "Please input the right port number for the SSL connection. Execute again."
            exit()
        portNumber=27994
    else:
        if portExist!=-1 and portNumber!=27993:
            print "Please input the right port number for the TCP connection. Execute again."
            exit()
    portNum=int(portNumber)
    soc.connect((hostName, portNum))
    mySoc=soc
    mySoc.sendall(courseName + ' HELLO ' + neuID+ '\n')

    while True:
        response = mySoc.recv(1024)
        if response==None:
            print "Sever Not Responding. Execute again."
            break
        myResult = getSolution(response)
        mySoc.sendall(courseName+' '+str(myResult)+'\n')
    mySoc.close()
    
'''
This function checks the initial validity of the input.
'''    
def validate():
    if len(sys.argv)>6 or len(sys.argv)<2:
        print 'Incorrect input. Execute again.'
        exit()    
            
'''
This function calls the validate() function to validate the input and connection() function to establish the connection.
''' 
def main():
    validate()
    connection()
    
main()
