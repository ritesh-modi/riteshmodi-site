/* ritesh 👋 — shared site behaviour. Every block is guarded, so pages only run what they have. */
(function(){
  "use strict";
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;

  /* ---------- theme toggle ---------- */
  var tgl = document.getElementById('tgl');
  function sysDark(){ return matchMedia('(prefers-color-scheme: dark)').matches; }
  function isDark(){ var t=root.getAttribute('data-theme'); return t ? t==='dark' : sysDark(); }
  function paint(){ if(tgl) tgl.textContent = isDark() ? '☀️' : '🌙'; }
  paint();
  if(tgl) tgl.addEventListener('click', function(){ root.setAttribute('data-theme', isDark()?'light':'dark'); paint(); if(window.__remakeBlobs) window.__remakeBlobs(); });

  /* ---------- waving hand ---------- */
  function wave(el){ if(reduce||!el) return; el.animate([
    {transform:'rotate(0)'},{transform:'rotate(16deg)'},{transform:'rotate(-8deg)'},
    {transform:'rotate(14deg)'},{transform:'rotate(-4deg)'},{transform:'rotate(0)'}
  ],{duration:1200,easing:'ease-in-out'}); }
  var heroWave = document.getElementById('wave');
  if(heroWave) setTimeout(function(){ wave(heroWave); }, 400);
  var brand = document.querySelector('.brand');
  if(brand){ brand.addEventListener('mouseenter', function(){ wave(brand.querySelector('.wv')); }); }

  /* ---------- rotating word (hero) ---------- */
  var rot = document.getElementById('rot');
  if(rot && !reduce){
    var words=['obvious','less scary','click','fun','yours'], ri=0;
    setInterval(function(){ ri=(ri+1)%words.length;
      rot.style.transition='opacity .25s,transform .25s'; rot.style.opacity='0'; rot.style.transform='translateY(6px)';
      setTimeout(function(){ rot.textContent=words[ri]; rot.style.opacity='1'; rot.style.transform='none'; },250);
    },2100);
  }

  /* ---------- card 3D tilt ---------- */
  if(!reduce){
    document.querySelectorAll('.card').forEach(function(c){
      c.addEventListener('mousemove', function(e){
        var r=c.getBoundingClientRect(), px=(e.clientX-r.left)/r.width-.5, py=(e.clientY-r.top)/r.height-.5;
        c.style.transform='perspective(800px) rotateY('+(px*9)+'deg) rotateX('+(-py*9)+'deg) translateY(-6px)';
      });
      c.addEventListener('mouseleave', function(){ c.style.transform=''; });
    });
  }

  /* ---------- filters (explorables page) ---------- */
  var filters = document.getElementById('filters');
  if(filters){
    var cards=[].slice.call(document.querySelectorAll('#grid .card')), count=document.getElementById('count');
    filters.querySelectorAll('.chip').forEach(function(c){
      c.addEventListener('click', function(){
        filters.querySelectorAll('.chip').forEach(function(x){x.classList.remove('on');}); c.classList.add('on');
        var f=c.getAttribute('data-f'), n=0;
        cards.forEach(function(card){
          var show = f==='all' || (' '+card.getAttribute('data-cat')+' ').indexOf(' '+f+' ')>=0;
          card.classList.toggle('hide', !show); if(show) n++;
        });
        if(count) count.textContent = n+' explorable'+(n===1?'':'s');
      });
    });
  }

  /* ---------- ambient blobs (hero) ---------- */
  var cv = document.getElementById('blobs');
  if(cv){
    var ctx=cv.getContext('2d'), W,H,dpr,blobs=[], mx=.5,my=.4;
    function palette(){ var s=getComputedStyle(root);
      return ['--coral','--grape','--teal','--sun','--sky','--pink'].map(function(v){return s.getPropertyValue(v).trim();}); }
    function resize(){ dpr=Math.min(2,devicePixelRatio||1); W=cv.clientWidth; H=cv.clientHeight; cv.width=W*dpr; cv.height=H*dpr; ctx.setTransform(dpr,0,0,dpr,0,0); }
    function make(){ var cols=palette(); blobs=[];
      for(var i=0;i<6;i++){ blobs.push({ x:Math.random()*W, y:Math.random()*H*.9,
        r:Math.min(W,H)*(0.22+Math.random()*0.18), c:cols[i%cols.length],
        dx:(Math.random()-.5)*0.16, dy:(Math.random()-.5)*0.16, px:Math.random()*40-20, py:Math.random()*40-20 }); } }
    window.__remakeBlobs=function(){ make(); if(reduce) draw(); };
    function hex2rgb(h){ h=h.replace('#',''); if(h.length===3)h=h.split('').map(function(c){return c+c;}).join(''); var n=parseInt(h,16); return [(n>>16)&255,(n>>8)&255,n&255]; }
    function draw(){
      ctx.clearRect(0,0,W,H);
      blobs.forEach(function(b){
        if(!reduce){ b.x+=b.dx; b.y+=b.dy;
          if(b.x<-b.r) b.x=W+b.r; if(b.x>W+b.r) b.x=-b.r; if(b.y<-b.r) b.y=H+b.r; if(b.y>H+b.r) b.y=-b.r; }
        var ox=(mx-.5)*b.px, oy=(my-.5)*b.py;
        var rgb=hex2rgb(b.c), g=ctx.createRadialGradient(b.x+ox,b.y+oy,0,b.x+ox,b.y+oy,b.r);
        g.addColorStop(0,'rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+','+(isDark()?0.5:0.42)+')');
        g.addColorStop(1,'rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',0)');
        ctx.fillStyle=g; ctx.beginPath(); ctx.arc(b.x+ox,b.y+oy,b.r,0,7); ctx.fill();
      });
      if(!reduce) requestAnimationFrame(draw);
    }
    resize(); make(); ctx.filter='blur(10px)'; draw();
    addEventListener('resize', function(){ resize(); make(); });
    addEventListener('mousemove', function(e){ mx=e.clientX/innerWidth; my=e.clientY/innerHeight; });
  }
})();
