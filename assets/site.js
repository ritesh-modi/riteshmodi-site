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

  /* ---------- explorables: search, filter, sort ---------- */
  var filters = document.getElementById('filters');
  if(filters){
    var grid   = document.getElementById('grid'),
        cards  = [].slice.call(grid.querySelectorAll('.card')),
        count  = document.getElementById('count'),
        qbox   = document.getElementById('q'),
        sortEl = document.getElementById('sort'),
        order  = cards.slice();            // document order, used as the tiebreak within a day
    var topic = 'all', level = false;

    /* The placeholder quotes the collection size, so derive it rather than hard-coding a number
       that goes stale the next time a card is added. */
    if(qbox){
      qbox.placeholder = 'Search ' + cards.length + ' explorables…';
    }

    /* The inline data-q on each card covers titles, headings and bold terms, so the very first
       keystroke is instant. The complete word list of every explorable lives in a separate
       ~150KB file, fetched once on first search, because making everyone who merely browses
       download it would be a poor trade. Until it lands, search falls back to the inline index. */
    var FULL = null, fetching = false;
    function loadFullIndex(){
      if(FULL || fetching) return;
      fetching = true;
      fetch('/assets/search-index.json')
        .then(function(r){ return r.ok ? r.json() : null; })
        .then(function(j){ if(j){ FULL = j; apply(); } })
        .catch(function(){ /* stay on the inline index */ });
    }

    var empty = document.createElement('div');
    empty.className = 'empty hide';
    empty.textContent = 'Nothing matches that. Try a shorter word, or clear the filters.';
    grid.appendChild(empty);

    function matches(card){
      if(topic !== 'all' && card.getAttribute('data-topic') !== topic) return false;
      if(level && card.getAttribute('data-level') !== 'beginner') return false;
      /* Every word in the query must appear somewhere in the card's index. Matching word by
         word rather than as one string means "learning rate" works even though the index is
         stored alphabetically and those two words are nowhere near each other in it. */
      var q = (qbox && qbox.value || '').trim().toLowerCase();
      if(q){
        var hay = card.getAttribute('data-q') || '';
        if(FULL){ var extra = FULL[card.getAttribute('href')]; if(extra) hay += ' ' + extra; }
        var words = q.split(/\s+/);
        for(var i=0;i<words.length;i++){ if(hay.indexOf(words[i]) < 0) return false; }
      }
      return true;
    }

    var MONTHS = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December'];

    /* "2026-09-08" -> "September 2026". Returns '' for a card with no usable date so
       the caller can leave it ungrouped rather than invent a heading for it. */
    function monthOf(d){
      var p = (d || '').split('-');
      if(p.length < 2) return '';
      var m = MONTHS[(+p[1]) - 1];
      return m ? m + ' ' + p[0] : '';
    }

    function monthHeading(label){
      var h = document.createElement('div'), t = document.createElement('h2');
      h.className = 'mhead';
      t.textContent = label;
      h.appendChild(t);
      return h;
    }

    function apply(){
      var sort = sortEl ? sortEl.value : 'new',
          searching = !!(qbox && qbox.value.trim()),
          n = 0;

      /* A–Z has no timeline to draw, and a month heading over a filtered or searched
         subset claims a completeness the page no longer has. Both fall back to a plain
         run of cards. */
      var flat = searching || topic !== 'all' || level || sort === 'az';

      cards.forEach(function(c){
        var ok = matches(c);
        c.classList.toggle('hide', !ok);
        c.classList.remove('feat');
        if(ok) n++;
      });

      /* Headings are rebuilt every pass rather than hidden, because which months exist
         depends on what survived the filter. */
      [].slice.call(grid.querySelectorAll('.mhead')).forEach(function(h){ grid.removeChild(h); });

      var seq = order.slice();
      if(sort === 'old')     seq.sort(function(a,b){ return (a.getAttribute('data-date')||'zzz').localeCompare(b.getAttribute('data-date')||'zzz'); });
      else if(sort === 'az') seq.sort(function(a,b){ return (a.getAttribute('data-title')||'').localeCompare(b.getAttribute('data-title')||''); });
      else                   seq.sort(function(a,b){ return (b.getAttribute('data-date')||'').localeCompare(a.getAttribute('data-date')||''); });

      /* The newest piece leads at full width, but only in the unfiltered newest-first
         view. Featuring the top of a filtered subset would promote whatever the filter
         happened to leave first, which is a different and much weaker claim. */
      var lead = null;
      if(!flat && sort === 'new'){
        for(var i = 0; i < seq.length; i++){
          if(!seq[i].classList.contains('hide')){ lead = seq[i]; break; }
        }
      }
      if(lead) lead.classList.add('feat');

      var month = '';
      seq.forEach(function(c){
        if(c === lead || c.classList.contains('hide')){ grid.appendChild(c); return; }
        if(!flat){
          var m = monthOf(c.getAttribute('data-date'));
          if(m && m !== month){ month = m; grid.appendChild(monthHeading(m)); }
        }
        grid.appendChild(c);
      });
      grid.appendChild(empty);

      empty.classList.toggle('hide', n > 0);
      if(count) count.textContent = n + (n === 1 ? ' explorable' : ' explorables');
    }

    filters.querySelectorAll('.chip').forEach(function(c){
      c.addEventListener('click', function(){
        if(c.hasAttribute('data-l')){                       // beginner is an independent toggle
          level = !level; c.classList.toggle('on', level);
        } else {
          filters.querySelectorAll('.chip:not(.lvl)').forEach(function(x){ x.classList.remove('on'); });
          c.classList.add('on'); topic = c.getAttribute('data-f');
        }
        apply();
      });
    });
    if(qbox)   qbox.addEventListener('input', function(){ loadFullIndex(); apply(); });

    /* Accept ?q= so a search has a shareable URL. Without it the SearchAction in the
       home page's WebSite schema would name a target that does nothing, and Google
       treats a search box it cannot actually drive as a reason to drop the markup. */
    (function(){
      if(!qbox) return;
      var m = /[?&]q=([^&#]*)/.exec(location.search);
      if(!m) return;
      try { qbox.value = decodeURIComponent(m[1].replace(/\+/g, ' ')); } catch(e){ return; }
      loadFullIndex(); apply();
    })();
    if(sortEl) sortEl.addEventListener('change', apply);
    apply();
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
