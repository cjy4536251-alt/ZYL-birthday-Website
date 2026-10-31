from pathlib import Path
from urllib.parse import quote
import re

ROOT = Path(__file__).parent
SVG = (ROOT / "cake.svg").read_text(encoding="utf-8")
(ROOT / "birthday-site" / "dist" / "cake.svg").write_text(SVG, encoding="utf-8")

OLD_LETTER = ('<p>高一认识你的时候，我没想过，我们会一起走过这么多故事。</p>'
              '<p>我们也曾走散过，沉默过，幸好，故事没有停在那些遗憾里。再次和你说话的时候，我真的很开心。</p>'
              '<p>新的一岁，希望你能勇敢追逐喜欢的一切，不必总是赶路，也别忘了看看沿途的花。</p>'
              '<p>愿你自由，永远明亮。生日快乐呀！</p>'
              '<p class="signature">—— 一直祝福你的CJY</p>')
NEW_LETTER = ('<p>高一认识你的时候，我没想过，我们会一起走过这么多故事。</p>'
              '<p>我们也曾走散过，沉默过，幸好，故事没有停在那些遗憾里。再次和你说话的时候，我真的很开心。</p>'
              '<p>新的一岁，希望你能勇敢追逐喜欢的一切，不必总是赶路，也别忘了看看沿途的风景。</p>'
              '<p>十九岁的张燕玲，生日快乐！</p>'
              '<p class="signature">—— 一直祝福你的CJY</p>')

CSS = '''
/* A sparkling pause before the river carries us onward. */
.yay-overlay{position:absolute;inset:0;z-index:18;display:grid;place-items:center;pointer-events:none;opacity:0;visibility:hidden;background:radial-gradient(circle,#ffe3a939 0,#18342c66 38%,#102b2880 100%)}
.yay-overlay.show{visibility:visible;animation:yay-pause 2.25s ease-in-out forwards}
.yay-overlay span{position:relative;font-size:clamp(110px,22vw,240px);font-weight:900;line-height:1;color:#fff9e3;background:linear-gradient(130deg,#fffefa,#ffda83 36%,#ffffff 51%,#f7bd69 75%,#fff9e3);background-clip:text;-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 0 15px #fff2a8) drop-shadow(0 0 35px #ffcd80);animation:yay-shine 1.1s ease-in-out infinite alternate}
.yay-overlay span:before,.yay-overlay span:after{content:'✦';position:absolute;font-size:.28em;-webkit-text-fill-color:#fff8ce;filter:drop-shadow(0 0 10px #fff0a4);animation:yay-twinkle .7s ease-in-out infinite alternate}
.yay-overlay span:before{top:-.08em;left:-.34em}.yay-overlay span:after{right:-.4em;bottom:.02em;animation-delay:.25s}
@keyframes yay-pause{0%{opacity:0;transform:scale(.7)}18%{opacity:1;transform:scale(1.04)}55%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(1.16)}}
@keyframes yay-shine{to{filter:drop-shadow(0 0 22px #fff9c4) drop-shadow(0 0 55px #ffd68c)}}
@keyframes yay-twinkle{to{opacity:.35;transform:scale(.6) rotate(45deg)}}
.birthday-cake{position:absolute;z-index:1;left:0;right:0;bottom:0;width:100%;height:100%;object-fit:contain;object-position:center bottom;pointer-events:none;filter:drop-shadow(0 15px 20px #141b17a8)}
.scene[data-scene="5"] .candles{z-index:3;bottom:38%;gap:clamp(2px,.42vw,5px)}
.scene[data-scene="5"] .candle,.scene[data-scene="5"] .candle:nth-child(2),.scene[data-scene="5"] .candle:nth-child(3){height:calc(clamp(68px,10vh,96px) + var(--rise))}
.scene[data-scene="5"] .candle.grand{height:clamp(115px,17vh,150px)}
.scene[data-scene="5"] .candle-platter{display:none}
@media(max-width:650px){.scene[data-scene="5"] .candles{bottom:37%;gap:1px}.scene[data-scene="5"] .candle,.scene[data-scene="5"] .candle:nth-child(2),.scene[data-scene="5"] .candle:nth-child(3){height:calc(67px + var(--rise))}.scene[data-scene="5"] .candle.grand{height:112px}}
@media(prefers-reduced-motion:reduce){.yay-overlay.show{animation-duration:2.25s!important}.yay-overlay span,.yay-overlay span:before,.yay-overlay span:after{animation:none!important}}
'''

def replace_once(s, old, new, label):
    count = s.count(old)
    if count != 1:
        raise ValueError(f"{label}: expected once, found {count}")
    return s.replace(old, new, 1)

def update(s, cake_src):
    s = replace_once(s, '</style>', CSS + '</style>', 'style')
    s = replace_once(s, '<div class="plane-transition"', '<div class="yay-overlay" id="yayOverlay" aria-hidden="true"><span>耶</span></div><div class="plane-transition"', 'yay overlay')
    s = replace_once(s, '<div class="candle-scene"><div class="candle-glow"></div>', f'<div class="candle-scene"><div class="candle-glow"></div><img class="birthday-cake" src="{cake_src}" alt="奶油草莓生日蛋糕">', 'cake')
    s = replace_once(s, '<div class="panel letter" id="letter">' + OLD_LETTER, '<div class="panel letter" id="letter">' + NEW_LETTER, 'letter')
    s = replace_once(s, '<p class="body">愿你像旷野的风，自由而明亮。<br>愿你走向的每一个远方，都有花开。</p>', '', 'old final lead')
    s = replace_once(s, '一只蝴蝶：愿你永远有轻盈的心情。', '一只蝴蝶：愿ZYL如蝴蝶，破茧之后，志赴山海', 'butterfly')
    s = replace_once(s, '一封小信：谢谢你，出现在我的青春里。', '一封小信：谢谢你，出现在我的青春里。（好肉麻呀~~~）', 'envelope')
    s = s.replace('写给风的愿望', '写给自己的愿望')
    old = "if(stones.size===3){$('riverpanel').classList.add('complete');sparkle(innerWidth/2,innerHeight/2,24);setTimeout(()=>go(3),1500)}"
    new = "if(stones.size===3){$('riverpanel').classList.add('complete');sparkle(innerWidth/2,innerHeight/2,24);const yay=$('yayOverlay');yay.classList.remove('show');void yay.offsetWidth;yay.classList.add('show');setTimeout(()=>{go(3);setTimeout(()=>yay.classList.remove('show'),300)},1950)}"
    s = replace_once(s, old, new, 'stone completion')
    s = s.replace('音乐稍后会加入。', '点击出发后可播放音乐。')
    return s

site = ROOT / 'birthday-site' / 'dist' / 'index.html'
site.write_text(update(site.read_text(encoding='utf-8'), 'cake.svg'), encoding='utf-8')
single_old = ROOT / '旷野生日网站_v6_含音乐.html'
single_new = ROOT / '旷野生日网站_v7_含蛋糕.html'
cake_uri = 'data:image/svg+xml,' + quote(SVG, safe='')
single_new.write_text(update(single_old.read_text(encoding='utf-8'), cake_uri), encoding='utf-8')
print(site)
print(single_new)
