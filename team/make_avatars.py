import hashlib, math

# Film palette: gold, green, coral cations/anions; cyan and violet from the VAN film
PAL = {
    'gold':  ('#fff4d6', '#d9b77a', '#6b5023'),
    'green': ('#e6fff0', '#5fc58f', '#1d5a3c'),
    'coral': ('#ffe1d6', '#e0745a', '#6b2a1c'),
    'cyan':  ('#e0fbff', '#4fc6d4', '#16545c'),
    'violet':('#ece6ff', '#8c7be6', '#382c75'),
    'blue':  ('#e4efff', '#86aee6', '#2a4670'),
}
SCHEMES = [('gold','green','coral'), ('cyan','violet','coral'), ('green','gold','blue'),
           ('violet','cyan','gold'), ('blue','gold','coral'), ('gold','cyan','violet')]

def defs():
    g = []
    for k, (hi, mid, lo) in PAL.items():
        g.append(f'<radialGradient id="at-{k}" cx="35%" cy="32%" r="70%"><stop offset="0" stop-color="{hi}"/>'
                 f'<stop offset=".45" stop-color="{mid}"/><stop offset="1" stop-color="{lo}"/></radialGradient>'
                 f'<radialGradient id="gl-{k}"><stop offset="0" stop-color="{mid}" stop-opacity=".55"/>'
                 f'<stop offset="1" stop-color="{mid}" stop-opacity="0"/></radialGradient>')
    g.append('<radialGradient id="av-bg" cx="50%" cy="35%" r="75%"><stop offset="0" stop-color="#1c2638"/>'
             '<stop offset="1" stop-color="#080b12"/></radialGradient>')
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
            + ''.join(g) + '</defs></svg>')

def inside(x, y, P):
    # head-and-shoulders profile, facing +x when P['dir']=1
    d = P['dir']; cx = 48
    def ell(ex, ey, rx, ry): return ((x-ex)/rx)**2 + ((y-ey)/ry)**2 <= 1
    hx, hy = cx + d*P['hoff'], P['hy']
    head = ell(hx, hy, P['hrx'], P['hry'])
    back = ell(hx - d*P['hrx']*.35, hy - 2, P['hrx']*.9, P['hry']*.95)
    hair = P['hair'] and ell(hx - d*5, hy - P['hry']*.45, P['hrx']*1.05, P['hry']*.65)
    nose = ell(hx + d*(P['hrx']+1), hy + 1, 5.5, 5)
    chin = ell(hx + d*(P['hrx']*.5), hy + P['hry']*.6, 9, 8)
    neck = (abs(x - (hx - d*3)) <= P['nw']) and hy + 6 <= y <= 92
    sh = ell(cx - d*3, 122, P['srx'], 48)
    return head or back or hair or nose or chin or neck or sh

def avatar(name, size=72):
    h = hashlib.sha256(name.encode()).digest()
    P = dict(dir=1 if h[0] % 2 else -1, hoff=3 + h[1] % 4, hy=39 + h[2] % 3,
             hrx=16 + h[3] % 3, hry=20 + h[4] % 3, hair=h[5] % 3 != 0, nw=9 + h[6] % 3,
             srx=46 + h[7] % 5)
    A, B, C = SCHEMES[h[8] % len(SCHEMES)]
    hexa = h[9] % 2 == 0
    sp = 5.6
    pts = []
    rows = int(96 / (sp * (0.866 if hexa else 1))) + 2
    for r in range(rows):
        y = 4 + r * sp * (0.866 if hexa else 1)
        off = (sp / 2 if (hexa and r % 2) else 0) + (h[10] % 3)
        for c in range(-1, 20):
            x = off + c * sp
            if 0 < x < 96 and 0 < y < 96 and inside(x, y, P):
                pts.append((x, y, r, c))
    # vacancies
    vac = {(h[11 + i] * 7 + i) % max(len(pts), 1) for i in range(4)}
    out = [f'<svg class="av" viewBox="0 0 96 96" width="{size}" height="{size}" aria-hidden="true">',
           '<rect width="96" height="96" fill="url(#av-bg)"/>']
    # faint stars
    for i in range(7):
        sx = (h[i] * 37 + h[i + 7]) % 96; sy = (h[i + 14] * 53 + h[i]) % 96
        out.append(f'<circle cx="{sx}" cy="{sy}" r=".45" fill="#c9d6ec" opacity=".35"/>')
    # bonds to near neighbours
    bonds = []
    for i, (x1, y1, *_) in enumerate(pts):
        for x2, y2, *_ in pts[i + 1:]:
            dd = math.hypot(x1 - x2, y1 - y2)
            if dd < sp * 1.05:
                bonds.append(f'M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}')
    out.append(f'<path d="{"".join(bonds)}" stroke="#b9c8e2" stroke-opacity=".22" stroke-width=".45" fill="none"/>')
    for k, (x, y, r, c) in enumerate(pts):
        if k in vac:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.8" fill="none" stroke="#86aee6" stroke-opacity=".7" stroke-width=".6" stroke-dasharray="1 1"/>')
            continue
        sel = (r + c) % 3 if not hexa else (r * 2 + c) % 3
        col, rad = [(A, 2.2), (B, 1.95), (C, 1.3)][sel]
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad*2.1:.1f}" fill="url(#gl-{col})"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="url(#at-{col})"/>')
    out.append('</svg>')
    return ''.join(out)

if __name__ == '__main__':
    import sys
    names = sys.argv[1:]
    html = '<html><body style="background:#f5f6f7;display:flex;gap:16px;flex-wrap:wrap;padding:20px">' + defs()
    for n in names:
        html += f'<div style="font:12px sans-serif">{avatar(n, 160)}<br>{n}</div>'
    open('/tmp/claude-0/-home-claude/90dd8236-d84d-552d-b831-082433b5249e/scratchpad/av_preview.html', 'w').write(html + '</body></html>')
