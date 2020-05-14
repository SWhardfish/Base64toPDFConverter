import xmltodict
from base64 import b64decode

with open('output.xml') as fd:
    obj = xmltodict.parse(fd.read())

obj = obj['S:Envelope']['S:Body']['ns2:sampleResponse']['result']
root_elements = obj["Level1"] if type(obj["Level1"]) == list else [obj["Level1"]]
# Above step ensures that root_elements is always a list
# Is obj["Root"] a list already, then use obj["Root"], otherwise make single element list.

for element in root_elements:

    b64 = element["AttachedDocument"]
    name = element["numbers"]["id"]
    print(name +' - '+ b64)

    # Decode the Base64 string, making sure that it contains only valid characters
    bytes = b64decode(b64, validate=True)

    # Perform a basic validation to make sure that the result is a valid PDF file
    # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
    # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
    if bytes[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    # Write the PDF contents to a local file
    f = open(name + '.pdf', 'wb')
    f.write(bytes)
    f.close()