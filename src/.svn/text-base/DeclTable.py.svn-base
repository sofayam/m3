class DeclTable:
    def __init__(self):
        self.table = {}
    def add(self,category,name,node):
        if category not in self.table:
            self.table[category] = {}
        if name in self.table[category]:
            print  "**************decl tabulation name clash**************"
        self.table[category][name] = node
    def category(self,cat):
        if cat in self.table:
            return self.table[cat]
        else:
            return {}
