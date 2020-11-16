def remove_brackets(list1):
    """Remove brackets from text"""
    return str(list1).replace('[','').replace(']','')

def remove_quotations1(list1):
    return list1.strip('\"')

def remove_quotations2(list1):
    return list1.strip('\'')