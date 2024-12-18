from docx import Document
import lxml.etree
import lxml.builder


def myread(myfilename):                 ## Read paragraphs from docx file
    document = Document(myfilename)     ## then store them in a dictionary
    listofpars = document.paragraphs
    mydict = {}
    
    '''
    for para in range(len(listofpars)):
        print(para)
        print(listofpars[para].text)
        print("\n")
        mydict[para] = listofpars[para].text
    ''' 
        
        
    
    
    for para in range(len(listofpars)):
        mydict[para] = ""
        for run in listofpars[para].runs:
            if run.bold:
                mydict[para] += "<hi rend=\"bold\">" + run.text + "</hi>"    
            else:
                #print(run.text)
                #print("just printed")
                mydict[para] += run.text 
        
    return mydict
    

def printdict(mydict):                  ## Loop print dictionary contents
    for x in range(len(mydict)):
        print("\n paragraph",x,"is")
        print(mydict[x])


def splitlines(mydict):                 ## Split dict contents by line and
    dictoflists = {}                    ## create new dict of lists of lines
    for x in range(len(mydict)):
        dictoflists[x] = mydict[x].splitlines()
    return dictoflists


def genxml(listdict):                   ## generate xml structure
    #E = lxml.builder.ElementMaker(namespace="http://www.tei-c.org/ns/1.0")
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
    myxml =  ET.tostring(the_doc, pretty_print=True)
    return myxml


def popuxml(basicxml,dictoflists):      ## populate xml with source data
    E = lxml.builder.ElementMaker()
    ET = lxml.etree
    tree = ET.fromstring(basicxml)
    cnav = tree.find(".//body")
    count=0
    #print(dictoflists)
    for x in range(len(dictoflists)):
        #print(dictoflists[x])
        #print("\n")
        for y in range(len(dictoflists[x])):
            count+=1
            curel = ET.Element("p", linenum=str(count), paragraph=str(x+1), pagenum="??")
            curel.text = dictoflists[x][y]
            cnav.append(curel)
    myxml = ET.tostring(tree)
    return myxml


def writexml(myxml,myfilename):         ## write xml structure to file
    f = open(myfilename, "wb")
    f.write(myxml)
    f.close()


def main():
    print("starting program...\n")
    dictofpars = myread('/home/michael/Downloads/11_PV_Vorrede_pres (1).docx')
    #printdict(dictofpars)
    dictoflists = splitlines(dictofpars)
    #printdict(dictoflists)
    basixml = genxml(dictoflists)
    populatedxml = popuxml(basixml,dictoflists)
    writexml(populatedxml,'/home/michael/Downloads/testxml03.xml')
    print("\nending program...")

if __name__ == '__main__':
    main()
