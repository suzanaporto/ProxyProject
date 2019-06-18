def Send403Message (request_page):
    
    http = []
    http.append('HTTP/1.1 200 OK\n')
    http.append('Content-Type: text/html\n')
    http.append('Connection: close\n')
    http.append('\r\n')

    f = open("BlockList/Domains.txt",'r+')

    for page in f:
        if page.strip() == request_page.strip():
            with open("HTML/403.html",'r+') as g:
                for line in g:
                    http.append(line+'\n')
            f.close()
            return http
    f.close()
    return "OK"