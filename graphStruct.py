from random import choice, randint, random
from typing import AnyStr
from math import sqrt
import logging
global logger

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)


def genUniqueId(num: int) -> AnyStr:
    uid = ""
    for _ in range(0, num):
        uid += choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890_')
    return uid


class node():
    def __init__(self, nid):
        self.x = 0
        self.y = 0
        self.id = nid
        self.links = []
        self.Fx = 0
        self.Fy = 0
        self.pin = False
        self.pinX = False
        self.pinY = False

    def linkToNode(self, eid):
        if eid == self.id:
            return None
        if eid in self.links:
            return eid
        self.links.append(eid)
        return eid


class graph():
    def __init__(self):
        self.nodeList = dict()

    def createNode(self, nid: AnyStr = ""):
        if nid == "":
            nid = genUniqueId(8)
        if nid not in self.nodeList.keys():
            self.nodeList[nid] = node(nid)
        return nid

    def getNode(self, nid):
        return self.nodeList[nid]

    def linkNode(self, sid, eid):
        sNode = self.getNode(sid)
        eNode = self.getNode(eid)
        sNode.linkToNode(eid)
        eNode.linkToNode(sid)

    def linkP2PNode(self, sids, eids):
        for sid, eid in zip(sids, eids):
            self.linkNode(sid, eid)

    def linkMeshNode(self, sids, eids):
        for sid in sids:
            for eid in eids:
                self.linkNode(sid, eid)

    def isLinked(self, sid, nid) -> bool:
        sNode = self.getNode(sid)
        if nid in sNode.links:
            return True
        return False


class frAutoLayout():
    def __init__(self, G: graph):
        self.G = G
        self.maxIter = 100
        self.idealDis = 10
        self.kCor = 0.2
        self.xCor = 0.2
        self.mCor = 0.1

    def calcDistance(self, sid, eid):
        sObj = self.G.getNode(sid)
        eObj = self.G.getNode(eid)
        d = sqrt((sObj.x - eObj.x)**2 + (sObj.y - eObj.y)**2)
        return d

    def randAssignNodes(self):
        maxL = sqrt(len(self.G.nodeList) * self.idealDis)
        for nObj in self.G.nodeList.values():
            nObj.x = maxL*random()
            nObj.y = maxL*random()
        # Rand Pin one Node
        randPinIdx = randint(0, len(self.G.nodeList)-1)
        #pinObj = list(self.G.nodeList.values())[randPinIdx]
        pinObj = self.G.nodeList['0']
        pinObj.x = maxL / 2.0
        pinObj.y = maxL / 2.0
        pinObj.pin = True
        pass

    def calcRepulsion(self, sid, eid):
        sObj = self.G.getNode(sid)
        eObj = self.G.getNode(eid)
        d = max(self.calcDistance(sid, eid), 0.01)
        ms = len(sObj.links)
        me = len(eObj.links)
        F = self.xCor * ms * me / d / d
        Fx = - F * (eObj.x - sObj.x) / d
        Fy = - F * (eObj.y - sObj.y) / d
        return Fx, Fy

    def calcGrativation(self, sid, eid):
        sObj = self.G.getNode(sid)
        eObj = self.G.getNode(eid)
        d = max(self.calcDistance(sid, eid), 0.01)
        linked = self.G.isLinked(sid, eid)
        if not linked:
            return 0, 0
        deltaD = d - self.idealDis
        if deltaD != 0:
            F = self.kCor * deltaD
        else:
            F = 0
        Fx = F * (eObj.x - sObj.y) / d
        Fy = F * (eObj.y - sObj.x) / d
        return Fx, Fy

    def moveWithForce(self):
        for sid in self.G.nodeList.keys():
            sObj = self.G.getNode(sid)
            if not sObj.pin:                
                m = len(sObj.links)
                dx = (sObj.Fx / m) ** 2 * self.mCor
                dy = (sObj.Fy / m) ** 2 * self.mCor
                if False:
                    if dx < 0.1:
                        sObj.pinX = True
                    if dy < 0.1:
                        sObj.pinX = True
                    if not sObj.pinX:
                        sObj.x += dx
                    if not sObj.pinY:
                        sObj.y += dy
                else:
                    sObj.x += dx
                    sObj.y += dy
                if sObj.Fx < 0.01 and sObj.Fy < 0.01:
                    sObj.pinX = True
                    sObj.pinX = True
                    sObj.pin =  sObj.pinX and sObj.pinY
                logger.info("id={} x={} y={} Fx={} Fy={} dx={} dy={}".format(sid, sObj.x, sObj.y, sObj.Fx, sObj.Fy, dx, dy))
            else:
                logger.info("id={} x={} y={} Fx={} Fy={} dx={} dy={}".format(sid, sObj.x, sObj.y, sObj.Fx, sObj.Fy, 0, 0))


    def updateForce(self):
        for sid in self.G.nodeList.keys():
            sObj = self.G.getNode(sid)
            sObj.Fx = 0
            sObj.Fy = 0
            for eid in self.G.nodeList.keys():
                if sid == eid:
                    continue
                Fpx,Fpy = self.calcRepulsion(sid, eid)
                Fgx,Fgy = self.calcGrativation(sid, eid)
                sObj.Fx += Fpx+Fgx
                sObj.Fy += Fpy+Fgy

    def autoLayout(self):
        self.randAssignNodes()
        for iter in range(0, self.maxIter):
            logger.info(">>>> Print {} Iteration".format(iter))
            self.updateForce()
            self.moveWithForce()
            logger.info(">>>> {}'s Iteration Finished\n".format(iter))       


if __name__ == "__main__":
    global G, V, layer
    G = graph()
    V = []
    for i in range(0,4):
        V.append(G.createNode(str(i)))
    G.linkMeshNode(V[0:1], V[1:4])
    # G.linkP2PNode(V[0:2], V[2:4])
    # G.linkMeshNode(V[0:2], V[4:8])
    # G.linkMeshNode(V[2:4], V[8:12])
    layer = frAutoLayout(G)
    layer.autoLayout()
