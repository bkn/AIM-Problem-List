# AIMPL

## Starting Daemons

Start CouchDB

$ make run-dummy
$ make run-proxy

$ open http://localhost:8888/pl/

To stop things:

$ make stop-proxy
$ make stop-dummy



## CouchDB URLs

This is a set of urls that can be easily accessed from the current implementation. 

    / 
    /pl/58afdcd0588ebaa30c246523b9b5ffab
    /pl/58afdcd0588ebaa30c246523b9b5ffab/sec/8  
    /pl/58afdcd0588ebaa30c246523b9b5ffab/sec/8/prob/4
 
    /pl/58afdcd0588ebaa30c246523b9b5ffab
    /_list/pl/pl_with_sections?
        startkey=["58afdcd0588ebaa30c246523b9b5ffab"]&
        endkey=["58afdcd0588ebaa30c246523b9b5ffab"%2C{}]&
        include_docs=true
  
    /pl/58afdcd0588ebaa30c246523b9b5ffab/sec/8  
    /_list/section/pl_full?
      startkey=["58afdcd0588ebaa30c246523b9b5ffab",8]&
      endkey=["58afdcd0588ebaa30c246523b9b5ffab",8,{}]&
      include_docs=true
    
    /pl/58afdcd0588ebaa30c246523b9b5ffab/sec/8/prob/4
    /_list/prob/pl_full?
      key=["58afdcd0588ebaa30c246523b9b5ffab",8,4]&
      include_docs=true


The problem when using a regular (human readable) field that is not the docid, in the view like this, is that 2 Problem Lists floating around out there could silently collide. In a scenario where problem lists are not identified (in the document) by their docids, but rather by view queries based on secondary attributes (eg: the human readable title), you can get many docs emitting on the same lookup key, rendering for users a silent remix of the 2 problem lists.

The most robust solution for Problem List identity is to use human-readable docids.

Here is the above, with human readable docids:

    / 
    /pl/edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2
    /pl/edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2/sec/8  
    /pl/edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2/sec/8/prob/4


    / 
    /_list/index/pls
    /aim-test/_design/aimpl/_list/index/pls
    
    /pl/edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2
    /_list/pl/pl_with_sections?
        startkey=["edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2"]&
        endkey=["edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2"%2C{}]&
        include_docs=true
        
    /pl/edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2/sec/8  
    /_list/section/pl_full?
      startkey=["edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2",8]&
      endkey=["edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2",8,{}]&
      include_docs=true
      
    /pl/edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2/sec/8/prob/4
    /aim-test/_design/aimpl/_list/section/pl_full?
      key=["edu.aim.pl-Braid-Groups-Clusters-and-Free-Probability-v2",8,4]&
      include_docs=true

Solution: Draft Mode

I've been aware from the beginning of the project that the workflow for Problem Lists is complex. I think a draft mode
