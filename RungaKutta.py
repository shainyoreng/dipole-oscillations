#implementing the RUnge-Kutta-Nystrom method as is shown in the paper
# https://www.sciencedirect.com/science/article/pii/089812219190209M
# The Six-stage seventh-order Lobatto IIIA RKN data from
# https://www.sciencedirect.com/science/article/pii/S0377042723004776

from math import sqrt

class RKN2f4:
	N = 3
	def c(k):
		return [(5-3*sqrt(3))/24,(3+sqrt(3))/12,(1+sqrt(3))/24][k]
	def cdot(k):
		return [(3-2*sqrt(3))/12,1/2,(3+2*sqrt(3))/12][k]
	def alpha(k):
		return [(3+sqrt(3))/6,(3-sqrt(3))/6,(3+sqrt(3))/6][k]
	def gamma(k,l):
		return [[             0, 		  0, 0],
				[(2-sqrt(3))/12, 		  0, 0],
				[ 			   0, sqrt(3)/6, 0]][k][l]

class RKN6f7:
	N = 6
	def cdot(k):
		return [0.033333333333333333333333, 0.189237478148923490158306, 0.277429188517743176508360, 0.277429188517743176508360, 0.189237478148923490158306, 0.033333333333333333333333][k]
	def c(k):
		return [0.033333333333333333333333, 0.167007309146871573763622, 0.178280368337326917338981, 0.099148820180416259169378, 0.022230169002051916394684, 0][k]
	def alpha(k):
		return [0, 0.117472338035267653574498, 0.357384241759677451842924, 0.642615758240322548157075, 0.882527661964732346425501, 1][k]
	def gamma(k, l):
		return [
			[0, 0, 0, 0, 0, 0],
			[0.006899875101736095721792, 0, 0, 0, 0, 0],
			[-0.008649348384522627811526, 0.072511096513592418131778, 0, 0, 0, 0],
			[0.104494022647602567335994, -0.023548725703754618489262, 0.125532209425544389630595, 0, 0, 0],
			[-0.206831187509496682807197, 0.515997648211865580182855, -0.023154349324445859897361, 0.103415425688545404668997, 0, 0],
			[0.837331614754864935733926, -1.126061983315861349122818, 0.805147761593905739861816, -0.055588841946761896205889, 0.039171448913852569732965, 0]
		][k][l]



def approximation_increment(f,g,x0,y0,dx0,dy0,dt,ORD):
	F = []
	G = []
	def f_k(f,g,x0,y0,dx0,dy0,dt,k):
		if k<len(F):
			return F[k]
		if k==0:
			return f(x0,y0)
		else:
			return f(x0+dx0*ORD.alpha(k)*dt+dt*dt*sum([ORD.gamma(k,i)*f_k(f,g,x0,y0,dx0,dy0,dt,i) for i in range(k)]),
					y0+dy0*ORD.alpha(k)*dt+dt*dt*sum([ORD.gamma(k,i)*g_k(f,g,x0,y0,dx0,dy0,dt,i) for i in range(k)]))
	def g_k(f,g,x0,y0,dx0,dy0,dt,k):
		if k<len(G):
			return G[k]
		if k==0:
			return g(x0,y0)
		else:
			return g(x0+dx0*ORD.alpha(k)*dt+dt*dt*sum([ORD.gamma(k,i)*f_k(f,g,x0,y0,dx0,dy0,dt,i) for i in range(k)]),
					y0+dy0*ORD.alpha(k)*dt+dt*dt*sum([ORD.gamma(k,i)*g_k(f,g,x0,y0,dx0,dy0,dt,i) for i in range(k)]))

	for i in range(ORD.N):
		F.append(f_k(f,g,x0,y0,dx0,dy0,dt,i))
		G.append(g_k(f,g,x0,y0,dx0,dy0,dt,i))
	
	x = x0 + dx0*dt + dt*dt*sum([ORD.c(i)*F[i] for i in range(ORD.N)])
	y = y0 + dy0*dt + dt*dt*sum([ORD.c(i)*G[i] for i in range(ORD.N)])
	dx = dx0 + dt*sum([ORD.cdot(i)*F[i] for i in range(ORD.N)])
	dy = dy0 + dt*sum([ORD.cdot(i)*G[i] for i in range(ORD.N)])

	return x,y,dx,dy

def approximation_increment_RNK6f7(f,g,x0,y0,dx0,dy0,dt):
	return approximation_increment(f,g,x0,y0,dx0,dy0,dt,RKN6f7)