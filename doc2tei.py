from docx import Document
import lxml.etree
import lxml.builder


def myread(myfilename):                 ## Read lines from docx file
    document = Document(myfilename)     ## then store them in a list
    listofpars = document.paragraphs
    masterlist=[]
    pagecount = 1
    linecount = 0
    for parindex in range(len(listofpars)):
        linecount +=1
        #print("para num: ", parindex)
        for runindex in range(len(listofpars[parindex].runs)):
            if listofpars[parindex].runs[runindex]._r.getchildren():
                if 'w:br' in listofpars[parindex].runs[runindex]._element.xml and 'type="page"' in listofpars[parindex].runs[runindex]._element.xml:
                    pagecount+=1
                    linecount=1
                elif '\n' in listofpars[parindex].runs[runindex].text:
                    linecount+=1
            #print("P", pagecount, "Line", linecount, repr(listofpars[parindex].runs[runindex].text), listofpars[parindex].runs[runindex].bold)
            
            bold = False
            if listofpars[parindex].runs[runindex].bold:
                bold = True
            
            #masterlist.append([pagecount,parindex,linecount,listofpars[parindex].runs[runindex].text.replace("\n",""), tag])
            curdict = {
                "page":pagecount,
                "para":parindex,
                "line":linecount,
                "text":listofpars[parindex].runs[runindex].text.replace("\n",""),
                "bold":bold
            }
            masterlist.append(curdict)
            
    #for current in masterlist:
    #    print(current)
    
    return masterlist
    

def printdict(mydict):                  ## Loop print dictionary contents
    for x in range(len(mydict)):
        print("\n paragraph",x,"is")
        print(mydict[x])


def splitlines(mydict):                 ## Split dict contents by line and
    dictoflists = {}                    ## create new dict of lists of lines
    for x in range(len(mydict)):
        dictoflists[x] = mydict[x].splitlines()
    return dictoflists


def genxml():                   ## generate xml structure
    #E = lxml.builder.ElementMaker(namespace="http://www.tei-c.org/ns/1.0")
    
    
    ns = "http://www.tei-c.org/ns/1.0"
    
    E = lxml.builder.ElementMaker()
    ET = lxml.etree
    the_doc = E.TEI(
                    E.teiHeader(
                        E.fileDesc(
                            E.titleStmt(
                                E.title(

                                ),
                                E.respStmt(
                                    E.resp('we can put some info here'

                                    ),
                                    E.name('the name of the text goes here'

                                    )
                                ),
                                E.publicationStmt(

                                ),
                                E.sourceDesc(
                                    E.p('insert some source desciption here'

                                    )
                                )
                            )
                        )
                    ),
                    E.text(
                        E.body(
                            E.p()
                        )
                    )
              )
    
    myxml =  ET.tostring(the_doc, pretty_print=False)
    print(myxml)
    return myxml


def popuxml(basicxml,masterlist):      ## populate xml with source data
    E = lxml.builder.ElementMaker()
    etree = lxml.etree
    tree = etree.fromstring(basicxml)
    cnav = tree.find(".//body")
    count=0
    
    '''
    #print(dictoflists)
    for x in range(len(dictoflists)):
        #print(dictoflists[x])
        #print("\n")
        for y in range(len(dictoflists[x])):
            count+=1
            curel = ET.Element("p", linenum=str(count), paragraph=str(x+1), pagenum="??")
            curel.text = dictoflists[x][y]
            cnav.append(curel)
    '''


    '''
    prevpara = prevline = prevpage = -1
    curtext = ""
    for item in masterlist:
        print(item)
        
        if item["page"]!=prevpage:              # make a new pb element (I *think* this only works properly
            pbe = etree.Element("pb")           # if pb does not occur inside a <p> element)
            pbe.set("n",str(item["page"]) )
            cnav.append(pbe)
            
        if item["para"]!=prevpara:
            if prevpara != -1:
                cnav.append(p)
            p = etree.Element("p")
                           
        if item["bold"]==True:
            if item["line"]==prevline:
                
            else:
            
        #elif item["strike"]:
        #elif item["note"]:
        
        else:
            if item["line"]==prevline:
                curtext+=item["text"]
            else:
                curtext+=item["text"]
                lbe = etree.SubElement(p, "lb", n=str(item["line"]))
                lbe.set("break","yes")
                lbe.tail = curtext
                curtext = ""
                
                
        
        prevpara = item["para"]
        prevline = item["line"]
        prevpage = item["page"]
    ''' 
    
    prevpara = prevline = prevpage = -1
    curtext = ""
    for item in masterlist:
        #print(item)
        
        #if item["page"]!=prevpage:              # make a new pb element (I *think* this only works properly
        #    pbe = etree.Element("pb")           # if pb does not occur inside a <p> element)
        #    pbe.set("n",str(item["page"]) )
        #    cnav.append(pbe)                   THIS NEEDS FIXED!!!!!!!!!!!
            
        if item["para"]!=prevpara:
            if prevpara != -1:
                cnav.append(p)
            p = etree.Element("p")
            prevline = -1
        
        isbreak=True
        if 'curelem' in locals():
            if len(curtext)>1:
                if (curtext[-1] == "-") or (curtext[-2:-1] == "- "):
                    #print("dash ends",curtext)
                    isbreak=False
            
        if item["line"]!=prevline:
            isbreak=True
            if 'curelem' in locals():
                curelem.tail = curtext
                curtext = ""
            curelem = etree.SubElement(p, "lb", n=str(item["line"]))
         
        if item["bold"]==True:
            if 'curelem' in locals():
                curelem.tail = curtext
                curtext = ""
            curelem = etree.SubElement(p, "emph", rend="bold")
            curelem.text = item["text"]
        else:
            curtext+=item["text"]

            
        #elif item["strike"]:
        #elif item["note"]:
        
        prevpara = item["para"]
        prevline = item["line"]
        prevpage = item["page"]       
            
            
            
            
    myxml = etree.tostring(tree)
    return myxml


def writexml(myxml,myfilename):         ## write xml structure to file
    f = open(myfilename, "wb")
    f.write(myxml)
    f.close()


def main():
    print("starting program...\n")
    masterlist = myread('/home/michael/Downloads/11_PV_Vorrede_pres (1).docx')
    #printdict(dictofpars)
    #dictoflists = splitlines(dictofpars)
    #printdict(dictoflists)
    basicxml = genxml()
    populatedxml = popuxml(basicxml,masterlist)
    writexml(populatedxml,'/home/michael/Downloads/testxml04.xml')
    print("\nending program...")

if __name__ == '__main__':
    main()
