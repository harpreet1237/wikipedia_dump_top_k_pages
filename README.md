Entry Number : 2020MCB1237 (Course Project - Social Computing and Networks)
Name: Harpreet Singh
Drive Link: https://drive.google.com/drive/folders/1W9NGeKyOOWk_rc0pqCwXeUkJHj-MzEs0?usp=sharing 


Files used : 
1. python code page_rank.py         -execution of code                                                                              -attached with project.
2. node_id_value.txt                -required for storing line number of each page and its adjacencyList(22.37 million pages)       -drive link shared (https://drive.google.com/drive/folders/1W9NGeKyOOWk_rc0pqCwXeUkJHj-MzEs0?usp=sharing)
3. graph_adjacencyList.txt          -required for storing adjacencyList of each page (directed graph)                               -drive link shared
4. top_k_pages.txt                  -required to output top K most visited pages after required number of iterations of random Walk -attached with project.
5. enwiki-latest-pages-articles.xml.bz2 dump    -dump from which data was extracted                                                 -publicly available


EXECUTION PROCESS AND TESTING :
1.  There are two user-specific functions :makeGraph() and randomWalk(k,P,iterations) and one-program specific function (get_links(content,dictionary))
2.  First function i.e. makeGraph builds the graph in the following way:
    a.  It extracts the page-title and page-content using xml conversion of string inbetween <page> to </page> tags. From this XML tree, we fetch 
        page-titles and page-contents from which links are extracted carefully (using get_links() functions) by refining links and "[[]]" tags in some special cases.
    b.  In first iteration of bz2 file, it stores page-titles in it and in a dictionary to store only required pages.
    c.  In second iteration, it stores all links that are given under page.revision.text tag and are stored in string (in file named graph_adjacencyList.txt)
        and line numbers corresponding to page-titles are stored in file named "node_id_value.txt" consisting of 22.37 million pages. It is used while directly fetching adjacency list of given page-title.
3.  Second function i.e. randomWalk(k,P,iterations) where k is number of top K pages you want to see, P - probability of teleporting.
    a.  First, it fetches dictionary of page-titles and their corresponding line numbers in "graph_adjacencyList.txt" file to obtain adjacencyList of current Page.
    b.  Second, it creates visited list and map to store page-titles and visited count.
    c.  I am using linecache module to read line number of adjacencyList at exact line number provided by information stored in node_id_value.txt . 
    d.  a while loop is run upto number of iterations provided. and then dictionary is sorted in reverse order to obtain K top most visited pages.
    e.  We teleported when no directed edge was there or according to the probability provided to any visited node. 
    f.  Then dictionary is sorted on the basis of decreasing order, then printing top k most visited pages in file "top_k_pages.txt".
    NOTE : In adjacencyList, first node is page itself, therefore it is removed from the string first, then a random page-title is choosen.
4.  Building graph such a large number of pages using titles as string took so long and therefore to ease out with debugging process, these two functions were used one by one.
    it took nearly 6 hours to make Graph stored in file named "graph_adjacencyList.txt" of size 5.24GB. Then randomWalk was performed on various number of iterations to check any discrepencies.
    it took nearly 2.5 hours to run upto 100 million iterations on whole network of wikipedia pages. 
5. For the sake of checking correctness of code, I used a smaller version of dump available and run my code on that file.


OBSERVATIONS : 
I observed that some pages that list other pages for reference are more visited such as Living People, MediaWiki,etc
Some countries' pages are also among top visited pages because of obvious reasons, everypage have something related to country where it happens or is about.
Some news agencies,Bureaus,surveys,National Registers,etc also top because of references of various events that have wikipedia pages.
Some very big events has also got position among top 10 like, World War II,World War I, etc.
Some famous big cities such as New york cities,London,etc also got positions among top visited pages.
Some famous recent movie categories like term Anime has also got top position.
Some famous theories got position among top hundreds most visited pages like Isaac Newton's gravitation theory(260), Cannizzaro reaction(279),etc 
Most of top visited pages are countries (or very famous cities) (top 50).
Most of top visited pages below 100 (and before 500) are mostly famous cities/states/regions like Montreal,Tamil Nadu,Dublin,etc with a small chunk of famous political entities(United States House of Representatives), 
theories,diseases(COVID-19  on 334th position) and many many other things that are competitively famous like universities (Stanford University),Newspapers(The Times of India),etc.
