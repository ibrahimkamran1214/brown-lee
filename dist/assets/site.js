document.documentElement.classList.add('js');(function(){
var hdr=document.getElementById('top-bar'),nav=document.getElementById('site-nav'),mb=document.querySelector('.menu-btn');
var mq=window.matchMedia('(max-width:1120px)');
function closeDrops(except){document.querySelectorAll('.drop-btn[aria-expanded="true"]').forEach(function(b){if(b!==except){b.setAttribute('aria-expanded','false');var d=document.getElementById(b.getAttribute('aria-controls'));if(d)d.classList.remove('open');}});}
document.querySelectorAll('.drop-btn').forEach(function(b){
  var d=document.getElementById(b.getAttribute('aria-controls')),li=b.parentNode,t;
  function open(){closeDrops(b);b.setAttribute('aria-expanded','true');d.classList.add('open');}
  function close(){b.setAttribute('aria-expanded','false');d.classList.remove('open');}
  b.addEventListener('click',function(e){e.stopPropagation();b.getAttribute('aria-expanded')==='true'?close():open();});
  li.addEventListener('mouseenter',function(){if(!mq.matches){clearTimeout(t);open();}});
  li.addEventListener('mouseleave',function(){if(!mq.matches){t=setTimeout(close,180);}});
  li.addEventListener('focusout',function(e){if(!mq.matches&&!li.contains(e.relatedTarget))close();});
});
document.addEventListener('click',function(e){if(!e.target.closest('.has-drop'))closeDrops();});
function setNav(o){if(!nav||!mb)return;nav.classList.toggle('open',o);mb.setAttribute('aria-expanded',o?'true':'false');document.body.classList.toggle('nav-open',o);
  if(o&&hdr){document.documentElement.style.setProperty('--navtop',hdr.getBoundingClientRect().bottom+'px');var f=nav.querySelector('a,button');if(f)f.focus();}}
if(mb)mb.addEventListener('click',function(){setNav(!nav.classList.contains('open'));});
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){if(nav&&nav.classList.contains('open')){setNav(false);mb.focus();}closeDrops();}
  if(e.key==='Tab'&&nav&&nav.classList.contains('open')){var f=[mb].concat([].slice.call(nav.querySelectorAll('a,button'))).filter(function(x){return x.offsetParent!==null;});var i=f.indexOf(document.activeElement);
    if(e.shiftKey&&i<=0){e.preventDefault();f[f.length-1].focus();}else if(!e.shiftKey&&i===f.length-1){e.preventDefault();f[0].focus();}}
});
if(nav)nav.addEventListener('click',function(e){var a=e.target.closest('a');if(a&&mq.matches)setNav(false);});
mq.addEventListener&&mq.addEventListener('change',function(){setNav(false);closeDrops();});
var cand=document.querySelectorAll('.sec .h-sec,.sec .eyebrow,.card,.steps li,.vs-col,.proj li,.tile,.g-item,.split-media,.split-copy,.panel,.faq details,.quote-form,.qb-copy,.calc-teaser,.stats div');
if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
var k=0;cand.forEach(function(el){if(el.getBoundingClientRect().top>window.innerHeight){el.classList.add('reveal');el.style.transitionDelay=((k++%4)*70)+'ms';io.observe(el);}});
setTimeout(function(){document.querySelectorAll('.reveal:not(.in)').forEach(function(el){if(el.getBoundingClientRect().top<window.innerHeight)el.classList.add('in');});},2500);}
document.querySelectorAll('.stats dd').forEach(function(dd){var m=dd.textContent.match(/^(\D*)(\d+)(.*)$/);if(!m||matchMedia('(prefers-reduced-motion: reduce)').matches)return;var end=+m[2],st=null;function f(t){if(!st)st=t;var p=Math.min((t-st)/1200,1);dd.textContent=m[1]+Math.round(end*(1-Math.pow(1-p,3)))+m[3];if(p<1)requestAnimationFrame(f);}
var o=new IntersectionObserver(function(es){if(es[0].isIntersecting){requestAnimationFrame(f);o.disconnect();}});o.observe(dd);});
var onS=function(){if(hdr)hdr.classList.toggle('scrolled',window.scrollY>40);};window.addEventListener('scroll',onS,{passive:true});onS();
var d=document.getElementById('lightbox');
if(d&&d.showModal){var li=document.getElementById('lb-img'),lc=document.getElementById('lb-cap');
document.querySelectorAll('[data-lightbox]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var im=a.querySelector('img');li.src=a.getAttribute('href');li.alt=im?im.alt:'';lc.textContent=im?im.alt:'';d.showModal();});});
d.querySelector('.lb-close').addEventListener('click',function(){d.close();});d.addEventListener('click',function(e){if(e.target===d)d.close();});}
var f=document.getElementById('calc');
if(f){var g=function(i){return document.getElementById(i)};
function calc(){var l=parseFloat(g('len').value)||0,w=parseFloat(g('wid').value)||0,dp=parseFloat(g('dep').value)||0;
var yd=(l*w*(dp/12)/27)*parseFloat(g('extra').value);var t=yd*parseFloat(g('mat').value)*0.9072;var m=yd*0.7646;
g('o-yd').textContent=yd.toFixed(1);g('o-t').textContent=t.toFixed(1);g('o-m').textContent=m.toFixed(1);}
f.addEventListener('input',calc);f.addEventListener('submit',function(e){e.preventDefault();});calc();}
})();
