import datetime

def Send403Hour(ip_client_address):

    http = []
    http.append('HTTP/1.1 200 OK\n')
    http.append('Content-Type: text/html\n')
    http.append('Connection: close\n')
    http.append('\r\n')

    f = open("BlockList/Hour.txt",'r+')

    for hour in f:
        now = datetime.datetime.now()
        splitted_time = hour.split(' ')
        print(splitted_time[0])
        ip_add = splitted_time[0] ==  ip_client_address
        in_minutes = (now.minute >= int(splitted_time[1].split(':')[1]))
        in_seconds = (now.second >= int(splitted_time[1].split(':')[2]))
        in_hour = (now.hour == int(splitted_time[1].split(':')[0]))
        #if its in the exact hour
        start_hour = (in_hour and in_minutes and in_seconds)
        # if its in the middle of start hour and end hour
        middle_in_hour = (now.hour > int(splitted_time[1].split(':')[0]))
        middle_in_last_hour = (now.hour < int(splitted_time[2].split(':')[0]))
        middle_hour = (middle_in_hour and middle_in_last_hour)
        # if its in the last hour
        last_in_hour = (now.hour == int(splitted_time[2].split(':')[0]))
        last_in_minutes = (now.minute <= int(splitted_time[2].split(':')[1]))
        last_in_seconds = (now.second <= int(splitted_time[2].split(':')[2]))
        last_hour = (last_in_hour and last_in_minutes and last_in_seconds)
        
        if ip_add and (start_hour or middle_hour or last_hour):
            with open("HTML/403hour.html",'r+') as g:
                for line in g:
                    http.append(line+'\n')
            f.close()
            return http
    f.close()
    return "OK"