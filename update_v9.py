from pathlib import Path
import base64

ROOT = Path(__file__).parent
CANDLE = ROOT / 'birthday-site' / 'dist' / 'candle-real.png'

# Back row then front row, distributed over the clear top of the cake.
POSITIONS = [
    (24, 73), (30, 76), (37, 78), (44, 79), (51, 79),
    (58, 78), (65, 76), (72, 73), (78, 69),
    (18, 54), (25, 59), (32, 63), (39, 65), (46, 66),
    (53, 66), (60, 65), (67, 63), (74, 59), (81, 54),
]
COLORS = [0, 28, 62, 110, 158, 192, 225, 270, 302,
          325, 14, 48, 90, 145, 182, 240, 282, 338, 55]

def css(candle_src: str) -> str:
    out = f'''
/* Nineteen individually interactive photographic wax candles. */
.scene[data-scene="5"] .candles{{position:absolute;left:50%;right:auto;top:0;bottom:auto;width:min(90%,510px);height:100%;display:block;margin:0;transform:translateX(-50%);pointer-events:none}}
.scene[data-scene="5"] .candle,.scene[data-scene="5"] .candle:nth-child(2),.scene[data-scene="5"] .candle:nth-child(3),.scene[data-scene="5"] .candle.grand{{position:absolute;display:block;width:clamp(19px,3vw,27px);height:clamp(55px,9vh,75px);margin:0;padding:0;border:0;background:none;box-shadow:none;filter:none;pointer-events:auto;transform:none}}
.scene[data-scene="5"] .candle:hover{{transform:translateY(-3px)}}
.scene[data-scene="5"] .candle .wax,.scene[data-scene="5"] .candle.grand .wax{{position:absolute;left:0;bottom:0;width:100%;height:100%;border:0;border-radius:0;box-shadow:none;background:transparent url("{candle_src}") center center / auto 100% no-repeat}}
.scene[data-scene="5"] .candle .wax:before,.scene[data-scene="5"] .candle .wax-shine,.scene[data-scene="5"] .candle .wax-drip,.scene[data-scene="5"] .candle .wick{{display:none}}
.scene[data-scene="5"] .candle:after{{content:'';position:absolute;z-index:5;left:50%;bottom:0;width:11px;height:4px;transform:translate(-50%,45%);border-radius:50%;background:#fff1dc;box-shadow:0 1px 3px #8e685d99;pointer-events:none}}
.scene[data-scene="5"] .candle .flame,.scene[data-scene="5"] .candle.small .flame,.scene[data-scene="5"] .candle.grand .flame{{left:50%;bottom:94%;width:11px;height:21px;filter:drop-shadow(0 0 7px #ffbc57) drop-shadow(0 0 13px #ffab4c)}}
.scene[data-scene="5"] .candle .flame:before{{background:radial-gradient(ellipse at 50% 70%,#fffef1 0 16%,#ffe39c 36%,#ffad55 68%,transparent 91%);border-radius:70% 70% 60% 60%;transform:rotate(0)}}
.scene[data-scene="5"] .candle .flame i{{left:4px;bottom:2px;width:3px;height:9px;background:#fffdf1;filter:blur(1px)}}
.scene[data-scene="5"] .candle .candle-halo{{left:-10px;top:-22px;width:48px;height:52px}}
@media(max-width:650px){{.scene[data-scene="5"] .candles{{width:min(94%,380px)}}.scene[data-scene="5"] .candle,.scene[data-scene="5"] .candle:nth-child(2),.scene[data-scene="5"] .candle:nth-child(3),.scene[data-scene="5"] .candle.grand{{width:19px;height:55px}}}}
'''
    for i, ((x, bottom), color) in enumerate(zip(POSITIONS, COLORS)):
        out += f'.scene[data-scene="5"] .candle[data-candle="{i}"]{{left:{x}%;bottom:{bottom}%;z-index:{3 if i<9 else 4}}}.scene[data-scene="5"] .candle[data-candle="{i}"] .wax{{filter:hue-rotate({color}deg)}}\n'
    return out

def update(source: str, candle_src: str) -> str:
    assert source.count('class="candles"') == 1
    assert source.count('data-candle="') == 19
    return source.replace('</style>', css(candle_src) + '</style>', 1)

site = ROOT / 'birthday-site' / 'dist' / 'index.html'
site.write_text(update(site.read_text(encoding='utf-8'), 'candle-real.png'), encoding='utf-8')
old = ROOT / '旷野生日网站_v8_含完整祝福.html'
new = ROOT / '旷野生日网站_v9_写实蜡烛.html'
uri = 'data:image/png;base64,' + base64.b64encode(CANDLE.read_bytes()).decode('ascii')
new.write_text(update(old.read_text(encoding='utf-8'), uri), encoding='utf-8')
print(site)
print(new)
