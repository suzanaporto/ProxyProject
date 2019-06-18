def Send403Word(request_msg):

    http = []
    http.append('HTTP/1.1 200 OK\n')
    http.append('Content-Type: text/html\n')
    http.append('Connection: close\n')
    http.append('\r\n')

    k = open("BlockList/Words.txt",'r+')

    for word in k:
        if word.strip() in request_msg.strip():
            with open("HTML/403word.html",'r+') as t:
                for line in t:
                    http.append(line+'\n')
            k.close()
            return http
    k.close()
    return "OK"