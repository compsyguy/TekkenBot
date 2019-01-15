from urllib.request import urlopen
import bs4 as BeautifulSoup
import re



def parse_character(character:str):
    """ Retrieve soup from URL Frame Data of single Character"""
    html = urlopen('http://rbnorway.org/t7-frame-data/'+character+'-t7-frames/').read()
    soup = BeautifulSoup.BeautifulSoup(html,'lxml')

    return soup

def commands_name(soup:BeautifulSoup):
    """ Parse URL and search for commands name """
    commands=[]
    zoom=soup.find('div',attrs={"entry clearfix"})
    zoom=zoom.find_all('td')
    j=0
    for i in zoom:
        if j%8==0 : #8xN matrix, we jump each column to get only command line column for each line
            cmd=str(zoom[j])
            cmd=cmd.replace("<td>",'')
            cmd=cmd.replace("</td>",'')
            if cmd == "<b>Command</b>":
                commands.append("################") #slice the list in moves and basic moves
            else :
                if len(cmd)>1: #ignore 1, 2,...
                    commands.append(cmd)
        j=j+1
    return commands
