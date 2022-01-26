from datetime import datetime

class Currency:
    Code = ""
    Description = ""
    High = None
    Low = None
    VarBid = None
    Bid = None
    Ask = None
    LastUpdate = None

    def __init__(self, code, desc, high, low, varBid, bid, ask):
        self.Code = code
        self.LastUpdate = datetime.now().time()
        self.Description = desc
        self.High = high
        self.Low = low
        self.VarBid = varBid
        self.Bid = bid
        self.Ask = ask
        
