from sklearn.linear_model import LinearRegression


def linearReg(ages_train, net_worths_train):

    reg = LinearRegression()
    reg.fit(ages_train, net_worths_train)

    return reg
