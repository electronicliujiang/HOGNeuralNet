import numpy as np

class NN:
    def __init__(self, hl=147, hlt='ReLU', lr=1, it=9000):
        np.random.seed(13)
        n = [0, hl, 0]
        self.cache = {
            "n": n,
            "hlt": hlt,
            "olt": 'sig',
            "lr": lr,
            'it': it
        }

    def train(self, tf, tl):
        self.populate(tf, tl)
        for i in range(self.cache["it"]):
            self.forward()
            c = self.loss()
            self.backward()

            if i % 1000 == 0:
                print("Cost at", i, c)

    def populate(self, tf, tl):
        A0 = np.array(tf).T
        Y = np.array(tl).T

        n = self.cache["n"]
        n[0] = A0.shape[0]
        n[2] = Y.shape[0]
        m = A0.shape[1]

        c = 0.001

        self.cache["A0"] = A0
        self.cache["Y"] = Y
        self.cache["n"] = n
        self.cache["m"] = m
        self.cache["W1"] = c * np.random.randn(n[1], n[0])
        self.cache["b1"] = c * np.random.randn(n[1], 1)
        self.cache["W2"] = c * np.random.randn(n[2], n[1])
        self.cache["b2"] = c * np.random.randn(n[2], 1)


    def forward(self):
        self.cache["Z1"] = np.dot(self.cache["W1"], self.cache["A0"]) + self.cache["b1"]
        self.cache["A1"] = self.activation(self.cache["Z1"], self.cache["hlt"])
        self.cache["Z2"] = np.dot(self.cache["W2"], self.cache["A1"]) + self.cache["b2"]
        self.cache["A2"] = self.activation(self.cache["Z2"], self.cache["olt"])

    def activation(self, Z, atype):
        A = np.zeros_like(Z)
        if atype == "lReLU":
            A = np.maximum(0.01 * Z, Z)
        elif atype == "ReLU":
            A = np.maximum(0, Z)
        elif atype == "sig":
            A = 1 / (1 + np.exp(-Z))
        elif atype == "tanh":
            A = (np.exp(Z) - np.exp(-Z)) / (np.exp(Z) + np.exp(-Z))
        return A

    def derivative(self, A, atype):
        dZ = np.array(A)
        if atype == "lReLU":
            dZ[dZ > 0] = 1
            dZ[dZ <= 0] = 0
        elif atype == "ReLU":
            dZ[dZ > 0] = 1
            dZ[dZ <= 0] = 0.01
        elif atype == "sig":
            dZ = np.dot(A, (1-A))
        elif atype == "tanh":
            dZ = 1 - np.square(A)
        return dZ

    def loss(self):
        Y = self.cache["Y"]
        A2 = self.cache["A2"]
        m = self.cache["m"]

        loss = np.add(np.multiply(Y, np.log(A2)), np.multiply((1-Y), np.log((1-A2))))
        cost = (-1/m) * np.sum(loss)
        cost = np.squeeze(cost)

        return cost

    def backward(self):
        m = self.cache["m"]

        self.cache["dZ2"] = np.subtract(self.cache["A2"], self.cache["Y"])
        self.cache["dW2"] = (1/m) * np.dot(self.cache["dZ2"], self.cache["A1"].T)
        self.cache["db2"] = (1/m) * np.sum(self.cache["dZ2"], axis=1, keepdims=True)
        self.cache["dZ1"] = np.dot(self.cache["W2"].T, self.cache["dZ2"]) * self.derivative(self.cache["A1"], self.cache["hlt"])
        self.cache["dW1"] = (1/m) * np.dot(self.cache["dZ1"], self.cache["A0"].T)
        self.cache["db1"] = (1/m) * np.sum(self.cache["dZ2"], axis=1, keepdims=True)

        self.update()

    def update(self):
        self.cache["dW1"] = np.subtract(self.cache["dW1"], (self.cache["lr"] * self.cache["dW1"]))
        self.cache["db1"] = np.subtract(self.cache["db1"], (self.cache["lr"] * self.cache["db1"]))
        self.cache["dW2"] = np.subtract(self.cache["dW2"], (self.cache["lr"] * self.cache["dW2"]))
        self.cache["db2"] = np.subtract(self.cache["db2"], (self.cache["lr"] * self.cache["db2"]))