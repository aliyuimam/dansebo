(function(){
  'use strict';
  var WA='2349078265699';
  var still=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s,r){return (r||document).querySelector(s)}
  function $$(s,r){return [].slice.call((r||document).querySelectorAll(s))}

  /* ---------- Header ---------- */
  var top=$('.top'),menuBtn=$('#menuBtn'),nav=$('#nav'),hasHero=!!$('.hero');
  function onScroll(){
    var y=window.scrollY||0;
    top.classList.toggle('scrolled',y>8);
    if(hasHero)top.classList.toggle('over',y<40);
  }
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  menuBtn.addEventListener('click',function(){
    var o=nav.classList.toggle('open');menuBtn.setAttribute('aria-expanded',o);top.classList.toggle('menu-open',o);
  });
  nav.addEventListener('click',function(e){if(e.target.closest('a')){nav.classList.remove('open');top.classList.remove('menu-open');menuBtn.setAttribute('aria-expanded','false')}});

  /* ---------- Home hero slider ---------- */
  var hero=$('.hero');
  if(hero){
    var slides=$$('.hero-slide',hero),bars=$('.hero-bars',hero),cap=$('.hero-cap span',hero),num=$('.hero-cap b',hero),cur=0,t=null,DUR=6000;
    hero.style.setProperty('--dur',DUR/1000+'s');
    slides.forEach(function(s,i){
      var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Show slide '+(i+1)+': '+s.dataset.cap);b.innerHTML='<i></i>';
      b.addEventListener('click',function(){show(i);play()});bars.appendChild(b);
    });
    var btns=[].slice.call(bars.children);
    function show(i){
      cur=(i+slides.length)%slides.length;
      slides.forEach(function(s,k){s.classList.toggle('on',k===cur);s.setAttribute('aria-hidden',k!==cur)});
      btns.forEach(function(b,k){b.classList.remove('run');b.classList.toggle('done',k<cur);b.setAttribute('aria-current',k===cur)});
      cap.textContent=slides[cur].dataset.cap;num.textContent=String(cur+1).padStart(2,'0')+' / '+String(slides.length).padStart(2,'0');
      var nx=slides[(cur+1)%slides.length].querySelector('img');if(nx&&nx.loading==='lazy')nx.loading='eager';
    }
    function play(){
      clearTimeout(t);if(still)return;
      var b=btns[cur];void b.offsetWidth;b.classList.add('run');
      t=setTimeout(function(){show(cur+1);play()},DUR);
    }
    function pause(){clearTimeout(t);btns.forEach(function(b){b.classList.remove('run')})}
    $('.h-prev',hero).addEventListener('click',function(){show(cur-1);play()});
    $('.h-next',hero).addEventListener('click',function(){show(cur+1);play()});
    var tx=null;
    hero.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
    hero.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50){show(cur+(dx<0?1:-1));play()}tx=null});
    document.addEventListener('visibilitychange',function(){document.hidden?pause():play()});
    show(0);play();
  }

  /* ---------- Lightbox ---------- */
  var LB=null;
  function lightbox(list,start){
    var i=start;
    if(!LB){
      LB=document.createElement('div');LB.className='lb';LB.hidden=true;LB.setAttribute('role','dialog');LB.setAttribute('aria-modal','true');LB.setAttribute('aria-label','Photo viewer');
      LB.innerHTML='<img alt=""><button class="lb-close" type="button" aria-label="Close"><svg><use href="#i-x"/></svg></button><button class="lb-prev flip" type="button" aria-label="Previous photo"><svg><use href="#i-arrow"/></svg></button><button class="lb-next" type="button" aria-label="Next photo"><svg><use href="#i-arrow"/></svg></button><div class="lb-cap"></div>';
      document.body.appendChild(LB);
    }
    var img=$('img',LB),capEl=$('.lb-cap',LB),last=document.activeElement;
    function draw(){var it=list[i];img.src=it.src;img.alt=it.alt;capEl.innerHTML='';var b=document.createElement('b');b.textContent=it.cap;var s=document.createElement('span');s.textContent=(i+1)+' / '+list.length;capEl.appendChild(b);capEl.appendChild(s)}
    function go(d){i=(i+d+list.length)%list.length;draw()}
    function close(){LB.hidden=true;document.removeEventListener('keydown',key);document.body.style.overflow='';if(last)last.focus()}
    function key(e){if(e.key==='Escape')close();else if(e.key==='ArrowRight')go(1);else if(e.key==='ArrowLeft')go(-1)}
    $('.lb-close',LB).onclick=function(e){e.stopPropagation();close()};$('.lb-prev',LB).onclick=function(e){e.stopPropagation();go(-1)};$('.lb-next',LB).onclick=function(e){e.stopPropagation();go(1)};
    LB.onclick=function(e){if(e.target===LB)close()};
    draw();LB.hidden=false;document.body.style.overflow='hidden';document.addEventListener('keydown',key);$('.lb-close',LB).focus();
  }

  /* ---------- Gallery slider ---------- */
  $$('.gs').forEach(function(gs){
    var items=$$('.gs-item',gs),thumbs=$('.gs-thumbs',gs),capB=$('.gs-cap b',gs),capS=$('.gs-cap span',gs),cur=0,timer=null;
    var list=items.map(function(it){var m=$('.main',it);return {src:m.getAttribute('src'),alt:m.alt,cap:it.dataset.cap}});
    items.forEach(function(it,i){
      var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Show '+it.dataset.cap);
      var im=document.createElement('img');im.src=list[i].src;im.alt='';im.loading='lazy';b.appendChild(im);
      b.addEventListener('click',function(){show(i);stop()});thumbs.appendChild(b);
    });
    var tb=[].slice.call(thumbs.children);
    function show(i){
      cur=(i+items.length)%items.length;
      items.forEach(function(it,k){
        var on=k===cur;it.classList.toggle('on',on);it.setAttribute('aria-hidden',!on);
        if(on||k===(cur+1)%items.length){$$('img[data-src]',it).forEach(function(im){im.src=im.dataset.src;im.removeAttribute('data-src')})}
      });
      tb.forEach(function(b,k){b.setAttribute('aria-current',k===cur)});
      capB.textContent=items[cur].dataset.cap;capS.textContent=(cur+1)+' / '+items.length;
      var b=tb[cur];if(b&&thumbs.scrollWidth>thumbs.clientWidth){thumbs.scrollTo({left:b.offsetLeft-thumbs.clientWidth/2+b.clientWidth/2,behavior:still?'auto':'smooth'})}
    }
    function auto(){if(still||gs.dataset.auto!=='1')return;stop();timer=setInterval(function(){show(cur+1)},5000)}
    function stop(){clearInterval(timer);timer=null}
    $('.g-prev',gs).addEventListener('click',function(){show(cur-1);stop()});
    $('.g-next',gs).addEventListener('click',function(){show(cur+1);stop()});
    $('.gs-zoom',gs).addEventListener('click',function(){stop();lightbox(list,cur)});
    $('.gs-stage',gs).addEventListener('keydown',function(e){if(e.key==='ArrowRight'){show(cur+1);stop()}if(e.key==='ArrowLeft'){show(cur-1);stop()}});
    var tx=null,st=$('.gs-stage',gs);
    st.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
    st.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>40){show(cur+(dx<0?1:-1));stop()}tx=null});
    gs.addEventListener('mouseenter',stop);
    show(0);auto();
  });

  /* ---------- Gallery grid + filters ---------- */
  var grid=$('.masonry');
  if(grid){
    var cells=$$('button',grid);
    function visible(){return cells.filter(function(c){return !c.hidden})}
    cells.forEach(function(c){c.addEventListener('click',function(){
      var v=visible();lightbox(v.map(function(x){var im=$('img',x);return {src:im.getAttribute('src'),alt:im.alt,cap:x.dataset.cap}}),v.indexOf(c));
    })});
    $$('.filters button').forEach(function(f){f.addEventListener('click',function(){
      $$('.filters button').forEach(function(x){x.setAttribute('aria-pressed',x===f)});
      var k=f.dataset.f;cells.forEach(function(c){c.hidden=!(k==='all'||c.dataset.tag===k)});
    })});
  }

  /* ---------- Lightbox groups (e.g. certificates) ---------- */
  var groups={};
  $$('[data-lb]').forEach(function(b){(groups[b.dataset.lb]=groups[b.dataset.lb]||[]).push(b)});
  Object.keys(groups).forEach(function(k){var g=groups[k];g.forEach(function(b,i){b.addEventListener('click',function(){
    lightbox(g.map(function(x){var im=$('img',x);return {src:x.dataset.src||im.getAttribute('src'),alt:im.alt,cap:x.dataset.cap}}),i);
  })})});

  /* ---------- Courses ---------- */
  var dlg=$('#courseDlg'),data=window.DS_COURSES||null;
  if(dlg&&data){
    var form=$('#enrolForm',dlg),msg=$('#payMsg',dlg),active=null;
    function naira(n){return '₦'+n.toLocaleString('en-NG')}
    function fill(c){
      active=c;
      $('#dTitle',dlg).textContent=c.title;
      $('#dLevel',dlg).textContent=c.level;
      $('#dSummary',dlg).textContent=c.summary;
      $('#dFor',dlg).textContent=c.forWhom;
      $('#dOutcome',dlg).textContent=c.outcome;
      $('#dDur',dlg).textContent=c.duration;
      $('#dMode',dlg).textContent=c.mode;
      $('#dCert',dlg).textContent='Certificate';
      var ul=$('#dModules',dlg);ul.innerHTML='';c.modules.forEach(function(m){var li=document.createElement('li');li.textContent=m;ul.appendChild(li)});
      $('#dFee',dlg).textContent=naira(c.fee);
      $('#dForm',dlg).textContent=naira(data.formFee);
      $('#dTotal',dlg).textContent=naira(c.fee+data.formFee);
      form.reset();msg.hidden=true;$$('.field',form).forEach(function(f){f.classList.remove('invalid');var e=$('.err',f);if(e)e.remove()});
      var on=$('input[name="mode"][value="'+(c.mode==='Virtual'?'Virtual':'Physical')+'"]',form);if(on)on.checked=true;
    }
    function open(id,push){
      var c=data.courses.filter(function(x){return x.id===id})[0];if(!c)return;
      fill(c);if(!dlg.open){dlg.showModal();document.documentElement.style.overflow='hidden'}dlg.scrollTop=0;var m=$('.dlg',dlg);if(m)m.scrollTop=0;
      if(push){try{history.replaceState(null,'','#'+id)}catch(e){}}
    }
    function close(){dlg.close()}
    dlg.addEventListener('close',function(){document.documentElement.style.overflow='';try{history.replaceState(null,'',location.pathname)}catch(e){}});
    dlg.addEventListener('click',function(e){if(e.target===dlg)close()});
    $('.dlg-close',dlg).addEventListener('click',close);
    $$('[data-course]').forEach(function(b){b.addEventListener('click',function(){open(b.dataset.course,true)})});
    if(location.hash){open(location.hash.slice(1),false)}

    function setErr(input,text){
      var f=input.closest('.field');f.classList.add('invalid');
      var e=$('.err',f);if(!e){e=document.createElement('span');e.className='err';f.appendChild(e)}e.textContent=text;
    }
    function clearErr(input){var f=input.closest('.field');f.classList.remove('invalid');var e=$('.err',f);if(e)e.remove()}
    $$('input',form).forEach(function(i){i.addEventListener('input',function(){clearErr(i)})});
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var ok=true,n=form.elements.ename,em=form.elements.eemail,ph=form.elements.ephone;
      if(!n.value.trim()){setErr(n,'Enter your full name.');ok=false}
      if(!/^\S+@\S+\.\S+$/.test(em.value.trim())){setErr(em,'Enter a valid email, for example name@example.com.');ok=false}
      if(ph.value.replace(/\D/g,'').length<7){setErr(ph,'Enter a phone number we can reach you on.');ok=false}
      if(!ok){var first=$('.invalid input',form);if(first)first.focus();return}
      var payload={course:active.id,courseTitle:active.title,courseFee:active.fee,formFee:data.formFee,amount:active.fee+data.formFee,
        name:n.value.trim(),email:em.value.trim(),phone:ph.value.trim(),mode:(form.querySelector('input[name="mode"]:checked')||{}).value};
      window.DanSebo.proceedToPayment(payload,msg);
    });
  }

  /* Payment hook: replace this with the Paystack (or other) checkout when ready.
     It receives the enrolment details and the amount in naira. */
  window.DanSebo={
    paymentUrl:null, // e.g. 'https://paystack.com/pay/your-page' or your backend endpoint
    proceedToPayment:function(p,msgEl){
      if(this.paymentUrl){location.href=this.paymentUrl;return}
      msgEl.hidden=false;
      msgEl.textContent='Thank you, '+p.name.split(' ')[0]+'. Online payment is coming soon. Our team will contact you on '+p.phone+' to complete your registration for '+p.courseTitle+'.';
    }
  };

  /* ---------- Contact form ---------- */
  var cf=$('#contactForm');
  if(cf){
    var subj=cf.elements.csubject,waBtn=$('#cfWa'),ok=$('#cfOk');
    var map={printing:'Printing & Production',branding:'Branding & Creative Design',ict:'ICT & Digital Solutions',training:'Training & Mentorship',partnership:'Partnership',quote:'Request a quote'};
    var h=location.hash.slice(1);if(map[h]){for(var i=0;i<subj.options.length;i++){if(subj.options[i].text===map[h])subj.selectedIndex=i}}
    function text(){
      var g=function(k){return cf.elements[k].value.trim()};
      return 'Hello DanSebo,\n\nSubject: '+subj.value+'\nName: '+g('cname')+(g('cemail')?'\nEmail: '+g('cemail'):'')+(g('cphone')?'\nPhone: '+g('cphone'):'')+(g('corg')?'\nOrganisation: '+g('corg'):'')+'\n\n'+g('cmsg');
    }
    function valid(){
      var good=true;
      [['cname','Enter your name.'],['cmsg','Tell us a little about what you need.']].forEach(function(r){
        var el=cf.elements[r[0]];if(!el.value.trim()){setErr2(el,r[1]);good=false}
      });
      var em=cf.elements.cemail;if(em.value.trim()&&!/^\S+@\S+\.\S+$/.test(em.value.trim())){setErr2(em,'Check the email address.');good=false}
      if(!good){var f=$('.invalid input, .invalid textarea',cf);if(f)f.focus()}
      return good;
    }
    function setErr2(input,t){var f=input.closest('.field');f.classList.add('invalid');var e=$('.err',f);if(!e){e=document.createElement('span');e.className='err';f.appendChild(e)}e.textContent=t}
    $$('input,textarea',cf).forEach(function(i){i.addEventListener('input',function(){var f=i.closest('.field');f.classList.remove('invalid');var e=$('.err',f);if(e)e.remove()})});
    waBtn.addEventListener('click',function(e){
      if(!valid()){e.preventDefault();return}
      waBtn.href='https://wa.me/'+WA+'?text='+encodeURIComponent(text());
      ok.hidden=false;
    });
    cf.addEventListener('submit',function(e){e.preventDefault();waBtn.click()});
  }

  /* ---------- Copy buttons ---------- */
  $$('[data-copy]').forEach(function(b){b.addEventListener('click',function(){
    var v=b.dataset.copy,lbl=b.textContent;
    function done(t){b.textContent=t;setTimeout(function(){b.textContent=lbl},1500)}
    try{navigator.clipboard.writeText(v).then(function(){done('Copied')},function(){done('Copy failed')})}catch(e){done('Copy failed')}
  })});

  var yr=$('#yr');if(yr)yr.textContent=new Date().getFullYear();
})();
