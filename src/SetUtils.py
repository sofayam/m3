import string
#
# A SnippetList is a subset of sparse set used for checking case statement ranges
# Subset because any "absorbing" will only be done by one snippet alone
# All work is done with integers (i.e. ord(..) values)
# I don't use sets here because the ranges could be huge - and all
# standard python solutions for set which I have found represent
# every member individually
#
def makeSnippet(first, last=None):
    if last!=None:
        if first == last:
            return ItemSnippet(first)
        elif first < last:
            return RangeSnippet(first,last)
        else:
            raise "bogus snippet %s %s" % (first,last)
    else:
        return ItemSnippet(first)

class RangeSnippet:
    def __init__(self,first,last):
        self.first = first
        self.last = last
    def absorbsItem(self,item):
        if (item < self.first) or (item > self.last):
            return False, None
        elif item == self.first:
            return True, [makeSnippet(self.first+1, self.last)]
        elif item == self.last:
            return True, [makeSnippet(self.first, self.last-1)]
        else:
            return True, [makeSnippet(self.first,item-1),makeSnippet(item+1,self.last)]
    def absorbsRange(self, first, last):
        if first < self.first or first > self.last: return False,None
        elif last < self.first or last > self.last: return False,None
        elif first == self.first and last == self.last: return True, None
        elif first == self.first:
            return True, [makeSnippet(last+1,self.last)]
        elif last == self.last:
            return True, [makeSnippet(last+1,self.last)]
        else: 
            return True, [makeSnippet(self.first,first-1),makeSnippet(last+1,self.last)]
        
        raise "too complicated"
    def image(self):
        return "[%s..%s]" % (self.first,self.last)
class ItemSnippet:
    def __init__(self,item):
        self.item = item
    def absorbsItem(self, item):
        return item == self.item, None
    def absorbsRange(self, first, last):
        return None,None
    def image(self):
        return "%s" % self.item
class SnippetList:
    def __init__(self,first,last):
        self.list = [RangeSnippet(first,last)]
    def deleteItem(self,item):
        #print "deleting item", item, "range", self.image()
        # find the snippet containing this item and either delete it (if it is an item) or cut it in two
        for snippet in self.list:
            res, splinters = snippet.absorbsItem(item)
            if res:
                self.list.remove(snippet)
                if splinters:
                    self.list += splinters
                return True
        return False
    def deleteRange(self,first,last):
        #print "deleting range", first, last, "range", self.image()
        if first > last:
            return False
        if first == last:
            return self.deleteItem(first)
        for snippet in self.list:
            res, splinters = snippet.absorbsRange(first,last)
            if res:
                self.list.remove(snippet)
                if splinters:
                    self.list += splinters
                return True
        return False
    def image(self):
        if not len(self.list) : return '[]'
        return string.join([snippet.image() for snippet in self.list], ",")
    def isEmpty(self):
        return self.list == []
    
def testMe():
    s = SnippetList(1,10)
    print s.image() #OK
    s.deleteRange(4,5)
    print s.image() #OK
    s.deleteItem(2)
    print s.image() #OK
    s.deleteRange(7,9)
    print s.image() #OK
    for i in [1,3,6,10]:
        s.deleteItem(i)
        print s.image() #OK     
    if s.isEmpty():
        print "passed" #OK
    else:
        print "failed" #OK
                
if __name__ == "__main__":
    testMe()
