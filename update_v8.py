from pathlib import Path
import base64
import re

ROOT = Path(__file__).parent
CAKE = ROOT / 'birthday-site' / 'dist' / 'cake-real.png'

CARD = r'''$('cardbtn').onclick=()=>{
  const canvas=document.createElement('canvas');canvas.width=1080;canvas.height=1440;
  const ctx=canvas.getContext('2d');const im=new Image();
  im.onload=()=>{
    const scale=Math.max(canvas.width/im.width,canvas.height/im.height),iw=im.width*scale,ih=im.height*scale;
    ctx.drawImage(im,(canvas.width-iw)/2,(canvas.height-ih)/2,iw,ih);
    const shade=ctx.createLinearGradient(0,0,0,1440);shade.addColorStop(0,'#122b2566');shade.addColorStop(1,'#0c211bbb');ctx.fillStyle=shade;ctx.fillRect(0,0,1080,1440);
    ctx.fillStyle='#fff9eeeF';ctx.shadowColor='#10251c99';ctx.shadowBlur=35;ctx.fillRect(68,252,944,1095);ctx.shadowBlur=0;
    ctx.strokeStyle='#d7b895';ctx.lineWidth=3;ctx.strokeRect(85,269,910,1061);
    ctx.fillStyle='#9d7456';ctx.textAlign='center';ctx.font='25px serif';ctx.fillText('A FIELD FOR YOU · 10.30',540,323);
    ctx.fillStyle='#354c3c';ctx.font='bold 51px serif';ctx.fillText('十九岁的张燕玲，生日快乐！',540,396);
    ctx.strokeStyle='#d9bd9a';ctx.beginPath();ctx.moveTo(240,432);ctx.lineTo(840,432);ctx.stroke();
    const paragraphs=[
      '高一认识你的时候，我没想过，我们会一起走过这么多故事。',
      '我们也曾走散过，沉默过，幸好，故事没有停在那些遗憾里。再次和你说话的时候，我真的很开心。',
      '新的一岁，希望你能勇敢追逐喜欢的一切，不必总是赶路，也别忘了看看沿途的风景。',
      '十九岁的张燕玲，生日快乐！'
    ];
    ctx.font='35px serif';ctx.fillStyle='#405544';ctx.textAlign='left';let y=495;
    for(const paragraph of paragraphs){
      let line='';
      for(const ch of Array.from(paragraph)){
        if(line&&ctx.measureText(line+ch).width>790){ctx.fillText(line,145,y);y+=62;line=ch}else line+=ch;
      }
      if(line){ctx.fillText(line,145,y);y+=62}y+=24;
    }
    ctx.font='30px serif';ctx.textAlign='right';ctx.fillStyle='#8a705c';ctx.fillText('—— 一直祝福你的CJY',920,Math.min(y+20,1280));
    const a=document.createElement('a');a.download='旷野生日纪念卡_含祝福.png';a.href=canvas.toDataURL('image/png');a.click();toast('纪念卡已保存');
  };
  im.onerror=()=>toast('纪念卡生成失败，请重试');im.src=IMAGE_DATA[6];
};'''

STYLE = '''
/* Real cake photography beneath the interactive candles. */
.scene[data-scene="5"] .birthday-cake{left:50%;right:auto;bottom:-30%;width:min(90%,510px);height:auto;max-height:none;object-fit:contain;transform:translateX(-50%);filter:drop-shadow(0 20px 22px #101b15aa)}
.scene[data-scene="5"] .candles{left:50%;right:auto;bottom:60%;width:min(76%,410px);transform:translateX(-50%);gap:clamp(1px,.3vw,3px)}
.scene[data-scene="5"] .candle,.scene[data-scene="5"] .candle:nth-child(2),.scene[data-scene="5"] .candle:nth-child(3){width:clamp(11px,1.7vw,18px);height:calc(clamp(61px,9vh,84px) + var(--rise))}
.scene[data-scene="5"] .candle.grand{width:clamp(30px,4.5vw,43px);height:clamp(102px,15vh,129px)}
@media(max-width:650px){.scene[data-scene="5"] .birthday-cake{width:min(94%,380px);bottom:-30%}.scene[data-scene="5"] .candles{width:92%;bottom:59%;gap:1px}.scene[data-scene="5"] .candle,.scene[data-scene="5"] .candle:nth-child(2),.scene[data-scene="5"] .candle:nth-child(3){width:clamp(10px,3vw,14px);height:calc(61px + var(--rise))}.scene[data-scene="5"] .candle.grand{width:32px;height:104px}}
'''

def update(source: str, cake_src: str) -> str:
    assert source.count('src="cake.svg"') == 1 or 'src="data:image/svg+xml,' in source
    source = re.sub(r'(<img class="birthday-cake" src=")[^"]+(" alt="奶油草莓生日蛋糕")',
                    lambda m: m.group(1) + cake_src + m.group(2), source, count=1)
    source = source.replace('</style>', STYLE + '</style>', 1)
    start = source.index("$('cardbtn').onclick=")
    end = source.index('\nfor(let i=0;i<24;i++)', start)
    source = source[:start] + CARD + source[end:]
    return source

site = ROOT / 'birthday-site' / 'dist' / 'index.html'
site.write_text(update(site.read_text(encoding='utf-8'), 'cake-real.png'), encoding='utf-8')
old = ROOT / '旷野生日网站_v7_含蛋糕.html'
new = ROOT / '旷野生日网站_v8_含完整祝福.html'
cake_uri = 'data:image/png;base64,' + base64.b64encode(CAKE.read_bytes()).decode('ascii')
new.write_text(update(old.read_text(encoding='utf-8'), cake_uri), encoding='utf-8')
print(site)
print(new)
