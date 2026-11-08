import math, sys

def surface(u, v):
    z = 0.70*math.sin(1.15*u)*math.cos(0.85*v) + 0.20*math.sin(2.1*u + 0.7*v) - 0.10*u*v
    return (u, v, z)

def rot(p, elev, azim):
    x, y, z = p
    ca, sa = math.cos(azim), math.sin(azim)
    x, y = x*ca - y*sa, x*sa + y*ca          # yaw about z
    ce, se = math.cos(elev), math.sin(elev)
    y, z = y*ce - z*se, y*se + z*ce          # tilt about x
    return (x, y, z)

def build(W, H, n_u, n_v, steps, stroke, stroke_min, umin=-2.4, umax=2.4, vmin=-1.9, vmax=1.9,
          color="#16181d", elev=1.12, azim=0.50, margin=0.06, bg=None, opmin=0.28, opmax=0.95):
    lines = []
    def emit(points):
        pts = [rot(surface(u, v), elev, azim) for (u, v) in points]
        depth = sum(p[1] for p in pts)/len(pts)   # y after rotation: larger = farther
        lines.append((depth, [(p[0], p[2]) for p in pts]))
    for i in range(n_u+1):
        u = umin + (umax-umin)*i/n_u
        emit([(u, vmin + (vmax-vmin)*k/steps) for k in range(steps+1)])
    for j in range(n_v+1):
        v = vmin + (vmax-vmin)*j/n_v
        emit([(umin + (umax-umin)*k/steps, v) for k in range(steps+1)])
    xs = [x for _, pts in lines for x, _ in pts]; ys = [y for _, pts in lines for _, y in pts]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    sc = min(W*(1-2*margin)/(bx1-bx0), H*(1-2*margin)/(by1-by0))
    ox = W/2 - (bx0+bx1)/2*sc; oy = H/2 + (by0+by1)/2*sc
    lines.sort(key=lambda t: -t[0])
    dmin = min(l[0] for l in lines); dmax = max(l[0] for l in lines)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" fill="none" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="Wireframe drawing of a curved surface">']
    if bg: out.append(f'<rect width="{W}" height="{H}" fill="{bg}"/>')
    for depth, pts in lines:
        t = (depth - dmin)/(dmax - dmin + 1e-9)       # 0 near, 1 far
        op = opmax - (opmax-opmin)*t
        sw = stroke - (stroke-stroke_min)*t
        d = "M" + " L".join(f"{ox + x*sc:.1f} {oy - y*sc:.1f}" for x, y in pts)
        out.append(f'<path d="{d}" stroke="{color}" stroke-opacity="{op:.2f}" stroke-width="{sw:.2f}"/>')
    out.append('</svg>')
    return "\n".join(out)

if __name__ == "__main__":
    kind = sys.argv[1]
    if kind == "hero":
        print(build(760, 620, 22, 15, 44, 1.15, 0.5, margin=0.01))
    elif kind == "mark":
        print(build(64, 64, 5, 4, 20, 3.2, 2.4, umin=-2.0, umax=2.0, vmin=-1.6, vmax=1.6, margin=0.08, opmin=0.55))
    elif kind == "og":
        print(build(1200, 630, 26, 18, 44, 1.4, 0.6, color="#f7f5f0", margin=0.0, opmin=0.18, opmax=0.8))
