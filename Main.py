from ServerProxy import ServerProxy
import os

def main():

    print("Proxy Project for Computer Network class")

    #Create directory
    directory_name = "CacheProxy"
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
        print("Directory" , directory_name ,  "Created ")
    else:    
        print("Directory" , directory_name ,  "already exists")
    
    # ServerProxy(HOST='192.168.0.2',PORT=1030)
    ServerProxy(HOST='127.0.0.1',PORT=1030)


if __name__ == '__main__':
    main()