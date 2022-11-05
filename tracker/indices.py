market_indices = [
                    ["S&P 500","^GSPC"],
                    ["Dow Jones Industrial Average","^DJI"],
                    ["NASDAQ Composite","^IXIC"],
                    ["NYSE COMPOSITE (DJ)","^NYA"],
    ["NYSE AMEX COMPOSITE INDEX","^XAX"],
    ["Cboe UK 100","^BUK100P"],
    ["Russell 2000","^RUT"],
    ["Vix","^VIX"],
    ["FTSE 100","^FTSE"],
    ["DAX PERFORMANCE-INDEX","^GDAXI"],
    ["CAC 40","^FCHI"],
    ["ESTX 50 PR.EUR","^STOXX50E"],
    ["EURONEXT 100","^N100"],
    ["BEL 20","^BFX"],
    ["MOEX Russia Index","IMOEX.ME"],
    ["Nikkei 225","^N225"],
    ["HANG SENG INDEX","^HSI"],
    ["SSE Composite Index","000001.SS"],
    ["Shenzhen Component","399001.SZ"]]

selected_indices = [["S&P 500","^GSPC"],
                    ["Dow Jones Industrial Average","^DJI"],
                    ["NASDAQ Composite","^IXIC"],
                    ["NYSE COMPOSITE (DJ)","^NYA"]]

rest_indices=[    ["NYSE AMEX COMPOSITE INDEX","^XAX"],
    ["Cboe UK 100","^BUK100P"],
    ["Russell 2000","^RUT"],
    ["Vix","^VIX"],
    ["FTSE 100","^FTSE"],
    ["DAX PERFORMANCE-INDEX","^GDAXI"],
    ["CAC 40","^FCHI"],
    ["ESTX 50 PR.EUR","^STOXX50E"],
    ["EURONEXT 100","^N100"],
    ["BEL 20","^BFX"],
    ["MOEX Russia Index","IMOEX.ME"],
    ["Nikkei 225","^N225"],
    ["HANG SENG INDEX","^HSI"],
    ["SSE Composite Index","000001.SS"],
    ["Shenzhen Component","399001.SZ"]]

def get_market_indices():
    return market_indices

def get_selected_indices():
    return selected_indices
def get_rest_indices():
    return rest_indices

def add_selected_indices(token):
    if len(rest_indices) == 0:
        return False
    for i in range(len(rest_indices)):
        if rest_indices[i][1] == token:
            selected_indices.append([rest_indices[i][0],rest_indices[i][1]])
            rest_indices.pop(i)
            break
    return True

def reduce_selected_indices(token):
    if len(selected_indices) == 0:
        return False
    for i in range(len(selected_indices)):
        if selected_indices[i][1] == token:
            rest_indices.append([selected_indices[i][0],selected_indices[i][1]])
            selected_indices.pop(i)
            break
    return True
