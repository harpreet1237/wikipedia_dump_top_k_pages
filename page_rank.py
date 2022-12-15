#2020MCB1237
#Harpreet Singh
import bz2 as bz
import xml.etree.ElementTree as  et
import random as random 
import linecache as lc                                                      #importing important libraries required for different functionalities

filepath = "enwiki-latest-pages-articles.xml.bz2"


def get_links(content,page_dict):                                           #function that extracts links from content of the page
    content.replace("\n","")
    contents = content.split("[[")

    links = []
    for con in contents:
        if "]]" in con and page_dict.get(con.split("]]")[0]) != None:
            links.append(con.split("]]")[0].strip())                        #careful selection of links from content 

    return links


def makeGraph():                                                            #function to make a graph from links obtained so far
    graph_file = open("graph_adjacencyList.txt","w+",encoding="utf-8")
    node_file = open("node_id_value.txt","w+",encoding="utf-8")             #both page_id and page_title relationship is being saved on disk 
                                                                            #and adjacency list of graph made to be built in this function
    
    page_dict = {}                                                          #to store the line number where page_titles are stored


    inPage = False                                                          # flag for string of xml tree
    tre_string=""                                                           # to be used for parsing in XML tree 

    f = bz.open(filepath,"rb")                                              #bz2 file to be read

    for fin in f:                                                           #reading the bz2 function 
        
        finn = str(fin,"utf-8")                                             #encoding 
        if inPage:                                                          #if we are still reading a page then search for end tag
            if '</page>' in finn:                                           #if we get end tag then we parse string as xml tree 
                tre_string+=finn
                root = et.fromstring(tre_string)                            #conversion of string to xml tree
                content = root.find('revision').find('text').text
                if content is None:
                    tre_string = ""
                    inPage = False
                else:
                    if "Wikipedia:" not in root.find('title').text.strip():
                        page_dict[root.find('title').text.strip()] = 1          #marking presence of page of given title
                    
                    tre_string = ""                                             #we have read page now  and hence mark inPage as False
                    inPage = False
                 
            else:                                                 
                tre_string+=finn                                            #if do not find end tag then keep on adding string 
        else:
            if '<page>' in finn:                                            #if we are out of page and find starting tag then start adding content into string
                inPage = True
                tre_string = finn

    f.close()
 
    f = bz.open(filepath,"rb")                                              #bz2 file to be read again
    inPage = False                                                          #flag for string of xml tree
    tre_string=""   
    
    count = 0
    for fin in f:  
        
        finn = str(fin,"utf-8")  
        if inPage:               
            if '</page>' in finn:   
                tre_string+=finn
                root = et.fromstring(tre_string)                            #conversion of string to xml tree
                content = root.find('revision').find('text').text
                if content is None:
                    tre_string = ""                                         #we have read page now  and hence mark inPage as False
                    inPage = False
                else:
                    content = root.find('revision').find('text').text.strip()

                    

                    node_file.write(root.find('title').text.strip()+"*@*"+str(count)+"\n")      #storing the title_page and line number by inserting a unique marker
                    adj_list = get_links(content,page_dict)                                     #getting links from above function
                    adj_list.append(root.find('title').text.strip())                            #adding starting node as first member of list
                    for i in range(len(adj_list)):
                        adj_list[i] = adj_list[i].strip()
                    adj_list.reverse()

                    graph_str = ""                                          #storing the whole adjacency list as string
                    for ad in adj_list:
                        temp = ad
                        graph_str+=(temp.strip())+";.;"                     #adding a unique marker to avoid clash with splitting of strings    
                    
                    graph_str+="\n" 
                    count+=1         
                    graph_file.write(graph_str)                             #writing in a file that contain adjacency list as a form of string
                    

                    tre_string = ""                                         #we have read page now  and hence mark inPage as False
                    inPage = False
                 
            else:                                                 
                tre_string+=finn                                            #if do not find end tag then keep on adding string 
        else:
            if '<page>' in finn:                                            #if we are out of page and find starting tag then start adding content into string
                inPage = True
                tre_string = finn
    
    f.close()
    graph_file.close()                                                      #closing all important files
    node_file.close()

    

def randomWalk(k,P,iterations):                                             #function to perform random walk Given arguements : k- top k most visited pages and P : probability of teleporting  and iterations to be performed          
    vis = {}
    page_id = {}                                                            #3 dictionaries storing the line numbers after reading from the file 

    
    node_file = open("node_id_value.txt","r",encoding="utf-8")              #reading adjacency list and node_list containing id and strings

    page_list = []
    while True:
        line = node_file.readline()
        if not line:
            break  
        nodes = line.split("*@*")                                           #splitting on the basis of markers added 
        # print(type(nodes[1]))
        
        if nodes[1][:-1].isdigit() == True: 
            page_list.append(nodes[0])
            page_id[nodes[0]] = int(nodes[1][:-1])                          #id values assigned to required string(title_pages)

    count = 0

    vis_list = []
    current_page = random.choice(list(page_id))                             #randomly selecting a page
    print(current_page)
    vis[current_page] = 1                                                   #marking a page visited
    vis_list.append(current_page)
    
    while count < iterations:                                               #performing randomwalk
        count+=1

        if count%50000 == 0:                   
            print(f"{count} steps completed..")
        adj_list = lc.getline("graph_adjacencyList.txt",page_id[current_page],module_globals=None)      #fetching adjacency list directly from file
        adj_list = adj_list.split(";.;")[:-1]
        
        lenn = len(adj_list)
            
        if lenn > 0:                                                                                    #removing the first page(i.e. itself) 
            adj_list.reverse()
            adj_list.pop()
            adj_list.reverse()
            lenn-=1

        

        pr = random.random()                                                                           #probability of teleportation is decided by given probability
        if pr < P:
            current_page = random.choice(vis_list)                                                     #randomly choosing the visited nodes 
        else:
            if adj_list == None or lenn == 0:                                                          #randomly choosing other pages if no new page has edge from current_page
                if len(vis_list) <= 1:
                    current_page = random.choice(page_list)                                         
                else:
                    current_page = random.choice(vis_list)
            else:
                current_page = random.choice(adj_list)                                                  #randomly choosing neighbors of current page

        val = vis.get(current_page)                                                                     #checking if page is visited or not

        if val == None:
            vis[current_page] = 1
            vis_list.append(current_page)
        else:                                                                                           #if not visited then marked with 1 else increased visited count
            vis[current_page]+=1


    print("randomWalk Completed..")
    kTop_pages = list(sorted(vis.items(), key=lambda x:x[1], reverse=True))         #sorting the dictionary on the basis of number of visits 

    result = open("top_k_pages.txt","w",encoding="utf-8")

    print("dictionary sorted..")

    result.write(f"Top {k} visited pages on Wikipedia after {iterations} number of iterations: \n")

    for v in kTop_pages:                                                            #printing top K pages on wikipedia on text file
        if k == 0:
            break
        k-=1
        result.write(v[0]+" "+str(v[1])+"\n")                                       #printing the page name with number of times visited 

    result.close()

    print(count)                                                                    #printing total steps taken

# makeGraph()                                                                       #function to build graph from wikipedia dump

print("Graph built...\nRandomWalk Under way")                                          
randomWalk(1000,0.4,1e8)                                                            #randomWalk function called by user : k can be choosen similarly, 
                                                                                    #probability of teleportation and number of iterations can be choosen by user n
