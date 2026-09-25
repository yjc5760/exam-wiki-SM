import numpy as np, math
r=math.radians
def trial(H,g,phi,delta,theta,beta,mode="a",n=20001):
    """楔體試算。theta>0：牆背頂端往填土側傾（牆背俯壓填土）。"""
    ph,dl,th,bt=r(phi),r(delta),r(theta),r(beta)
    A=np.array([0,0.]); B=np.array([H*math.tan(th),H])
    dw=np.array([math.sin(th),math.cos(th)]); nw=np.array([math.cos(th),-math.sin(th)])
    s=1 if mode=="a" else -1
    pd=math.cos(dl)*nw+s*math.sin(dl)*dw
    best=None; rhos=np.linspace(r(1),r(89),n); Ps=[]
    for rho in rhos:
        df=np.array([math.cos(rho),math.sin(rho)]); nf=np.array([-math.sin(rho),math.cos(rho)])
        # C = t*df on surface: B + u*(cosb,sinb)
        M=np.array([df,-np.array([math.cos(bt),math.sin(bt)])]).T
        try: t,u=np.linalg.solve(M,B)
        except: Ps.append(np.nan); continue
        if t<=0 or u<0: Ps.append(np.nan); continue
        C=t*df
        area=0.5*abs(B[0]*C[1]-B[1]*C[0])
        W=g*area
        rd=math.cos(ph)*nf+s*math.sin(ph)*df
        Mm=np.array([pd,rd]).T
        P,R=np.linalg.solve(Mm,np.array([0,W]))
        Ps.append(P)
    Ps=np.array(Ps)
    i=np.nanargmax(Ps) if mode=="a" else np.nanargmin(Ps)
    return Ps[i]/(0.5*g*H*H), math.degrees(rhos[i]), rhos, Ps
def ka_c(phi,delta,theta,beta):
    ph,dl,th,bt=map(r,(phi,delta,theta,beta))
    num=math.cos(ph-th)**2
    den=math.cos(th)**2*math.cos(dl+th)*(1+math.sqrt(math.sin(dl+ph)*math.sin(ph-bt)/(math.cos(dl+th)*math.cos(th-bt))))**2
    return num/den
def kp_c(phi,delta,theta,beta):
    ph,dl,th,bt=map(r,(phi,delta,theta,beta))
    num=math.cos(ph+th)**2
    den=math.cos(th)**2*math.cos(dl-th)*(1-math.sqrt(math.sin(dl+ph)*math.sin(ph+bt)/(math.cos(dl-th)*math.cos(th-bt))))**2
    return num/den
def ka_rs(phi,beta):
    b,p=r(beta),r(phi); q=math.sqrt(math.cos(b)**2-math.cos(p)**2)
    return math.cos(b)*(math.cos(b)-q)/(math.cos(b)+q)
if __name__=="__main__":
    for (d,t,b) in [(0,0,0),(20,0,0),(0,0,15),(15,0,15),(20,10,0),(20,-10,0),(20,10,15)]:
        k,rho,_,_=trial(6,18,30,d,t,b)
        print("A d=%d t=%d b=%d trial=%.4f rho=%.2f closed=%.4f"%(d,t,b,k,rho,ka_c(30,d,t,b)), "closed(-t)=%.4f"%ka_c(30,d,-t,b))
    for (d,t,b) in [(0,0,0),(20,0,0),(10,0,0),(30,0,0)]:
        k,rho,_,_=trial(6,18,30,d,t,b,"p")
        print("P d=%d trial=%.4f closed=%.4f rho=%.2f"%(d,k,kp_c(30,d,t,b),rho))
    print("Rankine sloped 15:",ka_rs(30,15))
