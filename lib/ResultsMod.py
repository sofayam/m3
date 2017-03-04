def Write(msg):
    import Global
    Global.results.putUserMessage(msg.val)

def WriteProtocol(msg):
    import Global
    Global.results.putUserMessageProtocol(msg.val)    
