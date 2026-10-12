/* Share bar: one script, every page. Load it with <script src="/assets/share.js" defer></script>.
   It adds two things:
   - a fixed "Share" tab at the top right of every page, which opens a panel of share buttons;
   - the share block itself, rendered into <div id="share"> when the page has one (home,
     explorables listing), otherwise just above the page footer (every explorable).
   The share target is the page's canonical URL, so a shared explorable links to its own page. */
(function(){
  "use strict";
  var doc = document;

  var canonical = doc.querySelector('link[rel="canonical"]');
  var url = (canonical && canonical.href) || location.href.split('#')[0];
  var ogTitle = doc.querySelector('meta[property="og:title"]');
  var title = (ogTitle && ogTitle.content) || doc.title;
  var both = title + ' ' + url;
  function enc(s){ return encodeURIComponent(s); }

  /* Platforms with a public web share endpoint. Instagram and TikTok have none for links,
     so they are handled below by copying the link; on phones "More" reaches them too. */
  var networks = [
    { name: 'X',           href: 'https://x.com/intent/post?text=' + enc(title) + '&url=' + enc(url) },
    { name: 'LinkedIn',    href: 'https://www.linkedin.com/sharing/share-offsite/?url=' + enc(url) },
    { name: 'Reddit',      href: 'https://www.reddit.com/submit?url=' + enc(url) + '&title=' + enc(title) },
    { name: 'Facebook',    href: 'https://www.facebook.com/sharer/sharer.php?u=' + enc(url) },
    { name: 'WhatsApp',    href: 'https://wa.me/?text=' + enc(both) },
    { name: 'Threads',     href: 'https://www.threads.net/intent/post?text=' + enc(both) },
    { name: 'Bluesky',     href: 'https://bsky.app/intent/compose?text=' + enc(both) },
    { name: 'Hacker News', href: 'https://news.ycombinator.com/submitlink?u=' + enc(url) + '&t=' + enc(title) },
    { name: 'Email',       href: 'mailto:?subject=' + enc(title) + '&body=' + enc(title + '\n\n' + url) }
  ];

  /* ---------- styles: scoped, neutral, so they sit on any explorable palette ---------- */
  var css = [
    '.lp-share{max-width:680px;margin:0 auto;padding:clamp(40px,6vw,64px) 16px;font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;color:inherit;text-align:left}',
    '.lp-share h2{font:600 clamp(20px,3vw,26px)/1.25 system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:-.01em;margin:0 0 8px;color:inherit}',
    '.lp-share p{margin:0 0 18px;opacity:.8;font-size:15px}',
    '.lp-share ul,.lp-panel ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}',
    '.lp-pill{display:inline-flex;align-items:center;padding:9px 14px;border:1px solid rgba(127,127,127,.45);border-radius:999px;background:transparent;color:inherit;font:500 14px/1.2 system-ui,-apple-system,"Segoe UI",sans-serif;text-decoration:none;cursor:pointer;white-space:nowrap}',
    '.lp-pill:hover{background:rgba(127,127,127,.14)}',
    '.lp-pill:focus-visible,.lp-tab:focus-visible{outline:2px solid currentColor;outline-offset:2px}',
    '.lp-share .lp-status,.lp-panel .lp-status{min-height:1.5em;margin:12px 0 0;font-size:14px;opacity:.85}',
    '.lp-tab{position:fixed;top:12px;right:12px;z-index:2147483000;padding:8px 14px;border:1px solid rgba(127,127,127,.5);border-radius:999px;background:Canvas;color:CanvasText;font:600 13px/1.2 system-ui,-apple-system,"Segoe UI",sans-serif;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.12)}',
    '.lp-panel{position:fixed;top:52px;right:12px;z-index:2147483000;width:min(340px,calc(100vw - 24px));padding:16px;border:1px solid rgba(127,127,127,.4);border-radius:14px;background:Canvas;color:CanvasText;box-shadow:0 10px 30px rgba(0,0,0,.18);font:15px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif}',
    '.lp-panel[hidden]{display:none}',
    '.lp-panel .lp-lead{margin:0 0 12px;font-size:14px;opacity:.85}',
    '.lp-panel .lp-pill{font-size:13px;padding:7px 11px}'
  ].join('');
  if(!doc.getElementById('lp-share-css')){
    var style = doc.createElement('style');
    style.id = 'lp-share-css';
    style.textContent = css;
    doc.head.appendChild(style);
  }

  /* ---------- helpers ---------- */
  function copyLink(message, status){
    var done = function(){ status.textContent = message; };
    var fallback = function(){
      var ta = doc.createElement('textarea');
      ta.value = url;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      doc.body.appendChild(ta);
      ta.select();
      try { doc.execCommand('copy'); done(); }
      catch(e){ status.textContent = 'Copy failed. The link is ' + url; }
      doc.body.removeChild(ta);
    };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(url).then(done, fallback);
    } else { fallback(); }
  }

  function openWindow(href){
    window.open(href, '_blank', 'noopener,noreferrer,width=640,height=720');
  }

  /* Builds the button list. Used twice: in the bottom block and in the top-right panel. */
  function buildList(status){
    var list = doc.createElement('ul');

    function add(label, onClick, href){
      var li = doc.createElement('li');
      var el = doc.createElement(href ? 'a' : 'button');
      el.className = 'lp-pill';
      el.textContent = label;
      if(href){
        el.href = href;
        if(href.indexOf('mailto:') !== 0){ el.target = '_blank'; el.rel = 'noopener noreferrer'; }
      } else {
        el.type = 'button';
        el.addEventListener('click', onClick);
      }
      li.appendChild(el);
      list.appendChild(li);
    }

    networks.forEach(function(n){
      if(n.name === 'Email'){ add(n.name, null, n.href); }
      else { add(n.name, function(){ openWindow(n.href); }); }
    });
    add('Instagram', function(){ copyLink('Link copied. Paste it into your Instagram story, post or DM.', status); });
    add('TikTok',    function(){ copyLink('Link copied. Paste it into your TikTok caption or message.', status); });
    add('Copy link', function(){ copyLink('Link copied.', status); });
    if(navigator.share){
      add('More…', function(){
        navigator.share({ title: title, text: title, url: url }).catch(function(){});
      });
    }
    return list;
  }

  /* ---------- bottom block ---------- */
  var block = doc.createElement('aside');
  block.className = 'lp-share';
  block.setAttribute('aria-label', 'Share');

  var h = doc.createElement('h2');
  h.textContent = 'If this site and its content helped you, or made a concept clear, it is wise to share it with others.';
  block.appendChild(h);

  var p = doc.createElement('p');
  p.textContent = 'Pass it to the person who is stuck on the same thing. Pick the place they will see it.';
  block.appendChild(p);

  var blockStatus = doc.createElement('p');
  blockStatus.className = 'lp-status';
  blockStatus.setAttribute('role', 'status');
  block.appendChild(buildList(blockStatus));
  block.appendChild(blockStatus);

  var slot = doc.getElementById('share');
  if(slot){ slot.appendChild(block); }
  else {
    var footer = doc.querySelector('footer');
    if(footer && footer.parentNode){ footer.parentNode.insertBefore(block, footer); }
    else { doc.body.appendChild(block); }
  }

  /* ---------- top-right tab and panel ---------- */
  var tab = doc.createElement('button');
  tab.type = 'button';
  tab.className = 'lp-tab';
  tab.textContent = 'Share';
  tab.setAttribute('aria-expanded', 'false');
  tab.setAttribute('aria-controls', 'lp-panel');

  var panel = doc.createElement('div');
  panel.className = 'lp-panel';
  panel.id = 'lp-panel';
  panel.hidden = true;
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'Share this page');

  var lead = doc.createElement('p');
  lead.className = 'lp-lead';
  lead.textContent = 'Helped you, or made a concept click? Send it to someone who needs it.';
  panel.appendChild(lead);

  var panelStatus = doc.createElement('p');
  panelStatus.className = 'lp-status';
  panelStatus.setAttribute('role', 'status');
  panel.appendChild(buildList(panelStatus));
  panel.appendChild(panelStatus);

  function setOpen(open){
    panel.hidden = !open;
    tab.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  tab.addEventListener('click', function(){ setOpen(panel.hidden); });
  doc.addEventListener('keydown', function(e){ if(e.key === 'Escape' && !panel.hidden){ setOpen(false); tab.focus(); } });
  doc.addEventListener('click', function(e){
    if(!panel.hidden && !panel.contains(e.target) && e.target !== tab){ setOpen(false); }
  });

  doc.body.appendChild(tab);
  doc.body.appendChild(panel);
})();
