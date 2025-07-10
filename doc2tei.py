from docx import Document
import lxml.etree
import lxml.builder
import argparse
import os
import glob
import sys
import re

def myread(myfilename):                 ## Read lines from docx file
    document = Document(myfilename)     ## then store them in a list
    listofpars = document.paragraphs
    masterlist=[]
    pagecount = 1
    linecount = 0
    isnewline = False
    masterind = 0
    for parindex in range(len(listofpars)):
        linecount +=1
        isnewline = True
        #print("para num: ", parindex)
        for runindex in range(len(listofpars[parindex].runs)):
            if listofpars[parindex].runs[runindex]._r.getchildren():
                if 'w:br' in listofpars[parindex].runs[runindex]._element.xml and 'type="page"' in listofpars[parindex].runs[runindex]._element.xml:
                    pagecount+=1
                    linecount=1
                elif '\n' in listofpars[parindex].runs[runindex].text:
                    linecount+=1
                    isnewline=True
            #print("P", pagecount, "Line", linecount, repr(listofpars[parindex].runs[runindex].text), listofpars[parindex].runs[runindex].bold)

            isbreak = "yes"
            if isnewline and masterind>0:
                if len(masterlist[masterind-1]["text"])>1:
                    if masterlist[masterind-1]["text"][-1] == "-" or masterlist[masterind-1]["text"][-2:] == "- ":
                        isbreak = "no"

            isbold = False
            isstrike = False
            isunderline = False
            isitalic = False
            if listofpars[parindex].runs[runindex].bold:
                isbold = True
            if listofpars[parindex].runs[runindex].font.strike:
                isstrike = True
            if listofpars[parindex].runs[runindex].font.underline:
                isunderline = True
            if listofpars[parindex].runs[runindex].italic:
                isitalic = True
                
            #note_match = re.search(r""
            
            #masterlist.append([pagecount,parindex,linecount,listofpars[parindex].runs[runindex].text.replace("\n",""), tag])
            curdict = {
                "page":pagecount,
                "para":parindex,
                "line":linecount,
                "text":listofpars[parindex].runs[runindex].text.replace("\n",""),
                "isbreak":isbreak,
                "bold":isbold,
                "strikethrough":isstrike,
                "italic":isitalic,
                "underline":isunderline
            }
            masterlist.append(curdict)
            masterind+=1
            isnewline=False
    
    '''        
    for index in range(len(masterlist)-1):
        #print("item",index,"is",masterlist[index])
        tempindex = index
        while(True):
            if masterlist[tempindex]["line"]!=masterlist[tempindex+1]["line"]:
                if masterlist[tempindex]["text"][-1] == "-" or masterlist[tempindex]["text"][-2:] == "- ":
                    masterlist[index]["isbreak"] = "no"
                else:
                    masterlist[index]["isbreak"] = "yes"
                break
            tempindex+=1
    masterlist[-1]["isbreak"]="yes"
    
    for index in range(len(masterlist)):
        print("item",index,"is",masterlist[index])
    '''
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
    
    E = lxml.builder.ElementMaker(namespace=ns, nsmap={None: "http://www.tei-c.org/ns/1.0"})
    ET = lxml.etree
    the_doc =   E.TEI(
                    E.teiHeader(
                        E.fileDesc(
                            E.titleStmt(
                                E.title("Philosophische Versuche: a digital edition"),
                                E.author("Tetens, Johannes Nikolaus (1736-1807)"),
                                E.respStmt(
                                    E.resp("Transcribed by"),
                                    E.name("John Hymers")
                                ),
                                E.respStmt(
                                    E.resp("Encoded by"),
                                    E.name("Michael Zahorec"),
                                    E.name("Micah Summers"),
                                    E.name("Courtney Fugate")
                                )
                            ),
                            E.publicationStmt(
                                E.publisher("The Tetens Project"),
                                E.pubPlace("Tallahassee, FL"),
                                E.address(
                                    E.addrLine("Department of Philosophy"),
                                    E.addrLine("Dodd Hall"),
                                    E.addrLine("Florida State University"),
                                    E.addrLine("Tallahassee, FL 32306")
                                )
                            ),
                            E.sourceDesc(
                                E.bibl("The first half of Teten's Philosophische Versuche")        
                            )
                        )
                    ),
                    E.text(
                        E.body(
                        )
                    )
                )
    
    #myxml =  ET.tostring(the_doc, pretty_print=False)
    #print(myxml)
    #return myxml
    
    return the_doc


def popuxml(myxml,masterlist):      ## populate xml with source data
    
    #E = lxml.builder.ElementMaker()
    etree = lxml.etree
    #tree = etree.fromstring(basicxml)
    #cnav = tree.find(".//body")
    #count=0
    
    body = myxml.xpath('//tei:text//tei:body', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})[0]
    
    
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
    i = 0
    while i < len(masterlist):
        item = masterlist[i]
        #print(item)
        
        if item["strikethrough"] and i+1 < len(masterlist):
            next_item = masterlist[i+1]
            if next_item["underline"]:
                if 'curelem' in locals():
                    curelem.tail = curtext
                    curtext = ""
                choice = etree.SubElement(p, "choice")
                sic = etree.SubElement(choice, "sic")
                sic.text = item["text"]
                corr = etree.SubElement(choice, "corr")
                corr.text = next_item["text"]
                curelem = choice
                i += 2
                prevpara = next_item["para"]
                prevline = next_item["line"]
                prevpage = next_item["page"]
                continue
        
        
        if item["page"]!=prevpage:
            if prevpara != -1:
                body.append(p)              # close current <p> before ending page
            pbe = etree.Element("pb")           
            pbe.set("n",str(item["page"]) )
            body.append(pbe)
            p = etree.Element("p")          # start new <p> for next page
            prevline = -1
            curtext = ""
            
        if item["para"]!=prevpara:
            if prevpara != -1:
                body.append(p)
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
            curelem.set("break",item["isbreak"])
         

         
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
        i += 1    
            
            
            
    xmlstr = etree.tostring(myxml)
    return xmlstr


def writexml(myxml,filename):         ## write xml structure to file
    f = open(filename, "wb")
    f.write(myxml)
    f.close()

def writetxt(masterlist, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        for index in range(len(masterlist)):
            f.write( "run "+str(index)+": "+str(masterlist[index])+"\n" )
    
def getfiles(indir, searchpattern):
    return glob.glob(os.path.join(indir, searchpattern))

def main():
    print("starting program...\n")
    parser = argparse.ArgumentParser(
        description = "converts a whole folder of docx files into TEI xml files (by the way, you should probably be using a virtual environment, if you aren't already using one)",
        usage="\nYou need to provide input and output directories.\nRun the program as follows.\npython doc2tei.py --inputdir exampleinputfolder --outputdir exampleoutputfolder\n\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--inputdir', type=str, help='Input file directory', required=True)
    parser.add_argument('--outputdir', type=str, help='Output file directory', required=True)
    args = parser.parse_args()

    if not args.inputdir or not args.outputdir:
        parser.print_help()
        sys.exit("\nError: you need to provide input and output directories. Run the program as follows (by the way, you should probably be using a virtual environment):\npython doc2tei.py --inputdir exampleinputfolder --outputdir exampleoutputfolder ")

    files = getfiles(args.inputdir, "*.docx")

    if files:
        for curfile in files:
            print("About to work on: ", curfile)
            masterlist = myread(curfile)
            #printdict(dictofpars)
            #dictoflists = splitlines(dictofpars)
            #printdict(dictoflists)
            basicxml = genxml()
            populatedxml = popuxml(basicxml,masterlist)
            writetxt(masterlist,   os.path.join(args.outputdir, os.path.basename(curfile)+ ".txt" ) )
            writexml(populatedxml, os.path.join(args.outputdir, os.path.basename(curfile)+ ".xml" ) )
    print("\nending program...")

if __name__ == '__main__':
    main()
