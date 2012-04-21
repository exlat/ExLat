################################################################################
# Copyright 2012 ExLat Team                                                    #
#                                                                              #
# This file is part of ExLat.                                                  #
#                                                                              #
# ExLat is free software: you can redistribute it and/or modify it             #
# under the terms of the GNU General Public License as published by            #
# the Free Software Foundation, either version 3 of the License, or at         #
# your option) any later version.                                              #
#                                                                              #
# ExLat is distributed in the hope that it will be useful, but                 #
# WITHOUT ANY WARRANTY; without even the implied warranty of                   #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with ExLat.  If not, see <http://www.gnu.org/licenses/>.               #
################################################################################

#!/usr/bin/env python
import sys
import exchange as E
import datetime
def getListofDictionary(List, EventName):
  """Get a list of dictionaries. Each dictionary
     corresponds to a record of a single event
     with EventName as SUMMARY. Empty list will be
     returned if EventName is not found.
     Testing
  """
  EventCount = List.count(EventName)
  
  End = 0

  # Iterate through all the records with SUMMARY = EventName
  for I in range(0, EventCount):
    Dict = {}

    # Get the start and end indices of a single record
    EventIndex = List.index(EventName, End)
    Start = EventIndex - (List[EventIndex:0:-1].index('BEGIN'))
    End = List.index('END', EventIndex)
    KeyIndex = Start + 1
    newlist=List[Start:End]
    for Entry in List[Start:End:2]:
      # FIXIT: If the event in the calender is not part of a series of events
      # the dates strings are different. That is if the event is planned as an
      # extra event
      flag=0
      if Entry == 'RRULE':
         index=newlist.index('RRULE')
         EventsList = repeat(newlist,index)
         flag=1
         break
    if flag == 0:
       EventsList = dictionary(List,Start,End,KeyIndex)
  return EventsList


def repeat(newlist,index):
   """generating startdate and enddate for repeating events"""
   temp = newlist[index+1]
   values=temp.split(';')
   freq=values[0].split('=')
   cnt=values[1].split('=')
   count=[]
   count.append(cnt[1])
   c=map(int,count)
   cnt=c[0]
   start=newlist.index('BEGIN')
   end=newlist.index('OPAQUE')
   keyindex=start+1
   arr = []
   arr2 = []
   i=0 
   for entry in newlist[start:end:2]:
      if entry == 'DTSTART;TZID=Asia/Calcutta':
         s=datetime.datetime.strptime(newlist[keyindex],"%Y%m%dT%H%M%S")
         arr.append(s.strftime('%Y'))
         arr.append(s.strftime('%m'))
         arr.append(s.strftime('%d'))
         arr.append(s.strftime('%H'))
         arr.append(s.strftime('%M'))
         arr.append(s.strftime('%S'))   
      if entry == 'DTEND;TZID=Asia/Calcutta':
         s=datetime.datetime.strptime(newlist[keyindex],"%Y%m%dT%H%M%S")
         arr2.append(s.strftime('%Y'))
         arr2.append(s.strftime('%m'))
         arr2.append(s.strftime('%d'))
         arr2.append(s.strftime('%H'))
         arr2.append(s.strftime('%M'))
         arr2.append(s.strftime('%S'))
      if entry == 'DESCRIPTION':
         topic = newlist[keyindex]

      keyindex += 2
   intarr=map(int,arr)
   inityear=intarr[0]
   initmonth=intarr[1]
   initday=intarr[2]
   inithour=intarr[3]
   initminut=intarr[4]
   intarr2=map(int,arr2)
   finyear=intarr2[0]
   finmonth=intarr2[1]
   finday=intarr2[2]
   finhour=intarr2[3]
   finminut=intarr2[4]

   if freq[1] == 'MONTHLY':
      while i < cnt :
            Dict={} 
            Dict['Start Date'] = '%i' %inityear+'-'+'%i' %initmonth+'-'+'%i' %initday+' at '+'%i' %inithour+':'+'%i' %initminut
            Dict['End Date'] = '%i' %finyear+'-'+'%i' %finmonth+'-'+'%i' %finday+' at '+'%i' %finhour+':'+'%i' %finminut
            Dict['Topic'] = topic
            EventsList.append(Dict)       
            initmonth += 1
            finmonth += 1
            i += 1
            if initmonth > 12:
               initmonth=1
               inityear += 1
            if finmonth > 12:
               finmonth=1
               finyear += 1
   return EventsList 
         




def dictionary(List,Start,End,KeyIndex):
   """dictionary when event is not repeating"""
   Dict={}
   for Entry in List[Start:End:2]:
      if Entry == 'DTSTART':
        s=datetime.datetime.strptime(List[KeyIndex],"%Y%m%dT%H%M%SZ")
        Dict['Start Date'] = s.strftime('%Y-%m-%d-%H:%M')
      if Entry == 'DTEND':
        Dict['End Date'] = s.strftime('%Y-%m-%d-%H:%M')
      if Entry == 'DESCRIPTION':
        Dict['Topic'] = List[KeyIndex]
      KeyIndex += 2
   EventsList.append(Dict)

   return EventsList
EventsList = []
if len(sys.argv) != 3:
  print "Usage: ./gcalread.py <.ics file> <SUMMARY String>"
  sys.exit(1)

ICSFile = sys.argv[1]
SummaryString = sys.argv[2]
F = open(ICSFile)
Content = F.read()
NewContent = Content.replace('\r\n', ':')
List = NewContent.split(':')
ListOfDict = getListofDictionary(List, SummaryString)
TableList = ListOfDict
print TableList

Obj = E.ExportToLatex()
TableString = Obj.createLatexTable(TableList)
Obj.createOutputString(TableString)
Obj.createLatexFile()

#Clearing Memory
del Obj
