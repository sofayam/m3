# TBD Pull out all the stops on Pmw to create some nice input dialogs

import tkSimpleDialog
import Dialog as TinyDialog
import Pmw
import string

def complain(ctext):
    d = TinyDialog.Dialog(title="Warning", text=ctext, bitmap='warning', default=0, strings=("OK",))

def askString(parent, title, prompt,pos='centerscreenfirst'):
    d = Pmw.PromptDialog(parent=parent, title=title,
                         #label_text=prompt,
                         buttons=('OK', 'Cancel'),
                         defaultbutton='OK')
    d.withdraw()
    res = d.activate(geometry=pos)
    if res == 'Cancel':
        return None
    else:
        return d.get()

def askQuestion(question, alts):
    d = Pmw.MessageDialog(title='?', message_text=question, buttons=alts)
    d.withdraw()
    res = d.activate()
    return res

def askActNamePortName(p,pos,ports):
    d = Pmw.Dialog(p,
                   buttons=('OK', 'Cancel'),
                   defaultbutton='OK')
    n = Pmw.EntryField(d.interior(), labelpos='w', label_text="Activity Name")
    p = Pmw.ComboBox(d.interior(), labelpos='w', label_text='Port Name', scrolledlist_items=ports)
    p.selectitem(0)
    v = Pmw.RadioSelect(d.interior(), labelpos='w', label_text="Visibility")
    v.pack()
    v.add('Internal'); v.add('External')
    v.invoke('External')
    n.pack()
    p.pack()
    d.withdraw()
    n.component("entry").focus_set() 
    res = d.activate(geometry=pos)
    if res == 'OK':
        if n.get():
            return {'name': n.get(), 'port': p.get(), 'visibility': v.getcurselection()}
    return None

def askProcNamePortName(p,pos,ports):
    d = Pmw.Dialog(p,
                   buttons=('OK', 'Cancel'),
                   defaultbutton='OK')
    n = Pmw.EntryField(d.interior(), labelpos='w', label_text="Procedure Name")
    p = Pmw.ComboBox(d.interior(), labelpos='w', label_text='Port Name', scrolledlist_items=ports)
    p.selectitem(0)
    v = Pmw.RadioSelect(d.interior(), labelpos='w', label_text="Visibility")
    v.pack()
    v.add('Internal'); v.add('External')
    v.invoke('External')
    n.pack()
    p.pack()
    d.withdraw()
    n.component("entry").focus_set() 
    res = d.activate(geometry=pos)
    if res == 'OK':
        if n.get():
            return {'name': n.get(), 'port': p.get(), 'visibility': v.getcurselection()}
    return None


def askMessage(p, pos, ports):
    d = Pmw.Dialog(p,
                   buttons=('OK', 'Cancel'),
                   defaultbutton='OK')
    n = Pmw.EntryField(d.interior(), labelpos='w', label_text="Message Name")
    p = Pmw.ComboBox(d.interior(), labelpos='w', label_text='Port Name', scrolledlist_items=ports)
    p.selectitem(0)
    dir = Pmw.RadioSelect(d.interior(), labelpos='w', label_text="Direction")
    dir.pack()
    dir.add('INCOMING'); dir.add('OUTGOING')
    dir.invoke('INCOMING')
    tim = Pmw.RadioSelect(d.interior(), labelpos='w', label_text="Timing")
    tim.pack()
    tim.add('SYNCHRONOUS'); tim.add('ASYNCHRONOUS')
    tim.invoke('ASYNCHRONOUS')
    n.pack()
    p.pack()
    d.withdraw()
    n.component("entry").focus_set() 
    res = d.activate(geometry=pos)
    if res == 'OK':
        if n.get():
            return {'name': n.get(), 'port': p.get(),
                    'dir': dir.getcurselection(), 'tim': tim.getcurselection()}
    return None
    

def askData(p,pos):
    d = Pmw.Dialog(p,
                   buttons=('OK', 'Cancel'),
                   defaultbutton='OK')
    n = Pmw.EntryField(d.interior(), labelpos='w', label_text="Datastore name")
    t = Pmw.EntryField(d.interior(), labelpos='w', label_text="Type", value="INTEGER")
    n.pack()
    t.pack()
    d.withdraw()
    n.component("entry").focus_set() 
    res = d.activate(geometry=pos)
    if res == 'OK':
        if n.get() and t.get():
            return {'name': n.get(), 'type': t.get()}
    return None
    
def askState(p,pos):
    retval = askString(p,"Give State name","State Name",pos)
    name = retval
    return {'name': name}

def askTransition(parent,pos,ports):
    d = Pmw.Dialog(parent,
                   buttons=('OK', 'Cancel'),
                   defaultbutton='OK')
    n = Pmw.EntryField(d.interior(), labelpos='w', label_text="Transition Name")
    p = Pmw.ComboBox(d.interior(), labelpos='w', label_text='Port Name', scrolledlist_items=ports)
    v = Pmw.RadioSelect(d.interior(), labelpos='w', label_text="Visibility")
    v.pack()
    v.add('Internal'); v.add('External')
    v.invoke('External')
    n.pack()
    p.pack()
    p.selectitem(0)
    d.withdraw()
    n.component("entry").focus_set() 
    res = d.activate(geometry=pos)
    if res == 'OK':
        if n.get():
            return {'name': n.get(),  'visibility': v.getcurselection(), 'port': p.get(), 'tim': "ASYNCHRONOUS"}
    return None

def askTrigger(p,pos):
    d = Pmw.Dialog(p,
                   buttons=('OK', 'Cancel'),
                   defaultbutton='OK')
    n = Pmw.EntryField(d.interior(), labelpos='w', label_text="Trigger name")
    e = Pmw.EntryField(d.interior(), labelpos='w', label_text="Expression", value="TRUE")
    n.pack()
    e.pack()
    d.withdraw()
    n.component("entry").focus_set() 
    res = d.activate(geometry=pos)
    if res == 'OK':
        if n.get() and e.get():
            return {'name': n.get(), 'expr': e.get()}
    return None

def askTimer(p,pos):
    dial = Pmw.Dialog(p,
                   buttons=('OK', 'Cancel'),
                   defaultbutton='OK')
    n = Pmw.EntryField(dial.interior(), labelpos='w', label_text="Timer Name")
    p = Pmw.ComboBox(dial.interior(), scrolledlist_items=['ONESHOT','PERIODIC'])
    v = Pmw.ComboBox(dial.interior(), scrolledlist_items=['FIXED','CHANGEABLE'])
    d = Pmw.EntryField(dial.interior(), labelpos='w',
                       label_text="Delay", value="10", validate = {'validator': 'integer'})
    s = Pmw.ComboBox(dial.interior(), scrolledlist_items=[
        'ps','ns','us','ms','s','min','hour','day','year'])
    p.selectitem(0)
    v.selectitem(0)
    s.selectitem(0)
    n.pack(); p.pack(); v.pack(); d.pack(); s.pack()
    dial.withdraw()
    n.component("entry").focus_set() 
    res = dial.activate(geometry=pos)
    if res == 'OK':
        if n.get() == "": return None
        else:
            return {'name': n.get(), 'variability': v.get(),
                    'periodicity': p.get(), 'delay': d.get(), 'scale': s.get()}
    else:
        return None

def askChild(p,pos):
    d = Pmw.Dialog(p,
                   buttons=('OK', 'Cancel'),
                   defaultbutton='OK')
    n = Pmw.EntryField(d.interior(), labelpos='w', label_text="Child name")
    t = Pmw.EntryField(d.interior(), labelpos='w', label_text="Capsule name")
    n.pack()
    t.pack()
    d.withdraw()
    n.component("entry").focus_set() 
    res = d.activate(geometry=pos)

    if res == 'OK':
        if n.get() and t.get():
            return {'childname': n.get(), 'capsulename': t.get()}
    return None
    
def askPort(p,pos):
    retval = askString(p,"Give Port name","Port Name",pos)
    if retval:
        return {'name': retval}
    return None

def askNote(p, pos='centerscreenfirst', text=""):
    d = Pmw.Dialog(p,
                   buttons=('OK', 'Cancel'))
    t = Pmw.ScrolledText(d.interior())
    t.insert('end',text)
    t.pack()
    d.withdraw()
    #t.component("entry").focus_set() 
    res = d.activate(geometry=pos)
    if res == 'OK':
        text = t.get()
        # snip off the trailing carriage return
        if text[-1] == "\n":
            text = text[:-1]
        return {'text': text }
    return None
    

def chooseMessage(p,messageNames, pos='centerscreenfirst'):
    d = Pmw.Dialog(p,
                   buttons=(('OK',)),
                   defaultbutton='OK')
    m = Pmw.ComboBox(d.interior(), labelpos='w', label_text='Message Name', scrolledlist_items=messageNames)
    m.selectitem(0)
    m.pack()
    d.withdraw()
    m.component("entry").focus_set() 
    res = d.activate(geometry=pos)
    return {'message': m.get()}

def askOptions(p, optDict):
    def addSwitch(d, name,val):
        res = Pmw.RadioSelect(d.interior(), labelpos='w', label_text=name)
        res.pack()
        res.add('ON')
        res.add('OFF')
        if val:
            res.invoke('ON')
        else:
            res.invoke('OFF')            
        return res
    def readSwitch(switch):
        return switch.getcurselection() == 'ON'
    d = Pmw.Dialog(p,
                   buttons=('OK','Cancel'),
                   defaultbutton='OK')
    switchDict = {}
    for key, val in optDict.items():        
        switchDict[key] = addSwitch(d,key,val)
    d.withdraw()
    res = d.activate()
    if res == 'OK':
        resDict = {}
        for key, switch in switchDict.items():
            resDict[key] = readSwitch(switch)
        return resDict
    else:
        return None
    

    
    
