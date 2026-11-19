import os,base64,subprocess
from playwright.sync_api import sync_playwright
FPS=30
ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','png','-i','-','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart','-an','laser_annealing_HZO.mp4'],stdin=subprocess.PIPE)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--allow-file-access-from-files']); pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.goto('file://'+os.path.abspath('film.html')); pg.evaluate('window.ready')
    n=int(pg.evaluate('DUR')*FPS)
    for i in range(n):
        d=pg.evaluate(f'(render({i/FPS}),document.getElementById("c").toDataURL("image/png"))')
        ff.stdin.write(base64.b64decode(d.split(',')[1]))
    d=pg.evaluate('(render(4.2),document.getElementById("c").toDataURL("image/jpeg",0.85))')
    open('poster.jpg','wb').write(base64.b64decode(d.split(',')[1]))
    b.close()
ff.stdin.close(); ff.wait()
