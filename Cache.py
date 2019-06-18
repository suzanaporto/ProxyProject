import os

def cache_sites_write(request_page_name,bytes):
    g = open("CacheProxy/"+request_page_name+".txt","w+")
    g.write(bytes)
    g.close()

def cache_sites_open(request_page_name):
    lines = []
    for file in os.listdir("CacheProxy"):
        if file == request_page_name+".txt":
            f = open(request_page_name+".txt","r+")
            for line in f:
                lines.append(line)
            f.close()
            return lines
    return "NOT"