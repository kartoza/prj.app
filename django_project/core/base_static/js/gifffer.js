// Taken from:
// https://github.com/krasimir/gifffer/blob/master/lib/gifffer.js
(function webpackUniversalModuleDefinition(root, factory) {
  if(typeof exports === 'object' && typeof module === 'object')
    module.exports = factory();
  else if(typeof define === 'function' && define.amd)
    define("Gifffer", [], factory);
  else if(typeof exports === 'object')
    exports["Gifffer"] = factory();
  else
    root["Gifffer"] = factory();
})(this, function() {
var d = document;
var playSize = 60;

var Gifffer = function() {
  var images, i = 0, gifs = [];

  images = d.querySelectorAll('[data-gifffer]');
  for(; i<images.length; ++i) process(images[i], gifs);
  // returns each gif container to be usable programmatically
  return gifs;
};

function formatUnit(v) {
  return v + (v.toString().indexOf('%') > 0 ? '' : 'px');
};

function createContainer(w, h, el, altText) {
  var alt;
  var con = d.createElement('BUTTON');
  var cls = el.getAttribute('class');
  var id = el.getAttribute('id');

  cls ? con.setAttribute('class', el.getAttribute('class')) : null;
  id ? con.setAttribute('id', el.getAttribute('id')) : null;
  con.setAttribute('style', 'position:relative;cursor:pointer;background:none;border:none;padding:0;');
  con.setAttribute('aria-hidden', 'true');

  // creating play button
  var play = d.createElement('DIV');
  play.setAttribute('class','gifffer-play-button');
  play.setAttribute('style', 'width:' + playSize + 'px;height:' + playSize + 'px;border-radius:' + (playSize/2) + 'px;background:rgba(0, 0, 0, 0.3);position:absolute;');

  var trngl = d.createElement('DIV');
  trngl.setAttribute('style', 'width:0;height: 0;border-top:14px solid transparent;border-bottom:14px solid transparent;border-left:14px solid rgba(0, 0, 0, 0.5);position:absolute;left:26px;top:16px;');
  play.appendChild(trngl);

  // create alt text if available
  if (altText) {
    alt = d.createElement('p');
    alt.setAttribute('class','gifffer-alt');
    alt.setAttribute('style', 'border:0;clip:rect(0 0 0 0);height:1px;overflow:hidden;padding:0;position:absolute;width:1px;');
    alt.innerText = altText + ', image';
  }

  // dom placement
  con.appendChild(play);
  el.parentNode.replaceChild(con, el);
  altText ? con.parentNode.insertBefore(alt, con.nextSibling) : null;
  return { c: con, p: play };
};

function calculatePercentageDim (el, w, h, wOrig, hOrig) {
  var parentDimW = el.parentNode.offsetWidth;
  var parentDimH = el.parentNode.offsetHeight;
  var ratio = wOrig / hOrig;

  if (w.toString().indexOf('%') > 0) {
    w = parseInt(w.toString().replace('%', ''));
    w = (w / 100) * parentDimW;
    h = w / ratio;
  }

  return { w: w, h: h };
};

function process(el, gifs) {
  var url, con, c, w, h, duration,play, gif, playing = false, cc, isC, durationTimeout, dims, altText;

  url = el.getAttribute('data-gifffer');
  w = el.getAttribute('data-gifffer-width');
  h = el.getAttribute('data-gifffer-height');
  duration = el.getAttribute('data-gifffer-duration');
  altText = el.getAttribute('data-gifffer-alt');
  el.style.display = 'block';

  // creating the canvas
  c = document.createElement('canvas');
  isC = !!(c.getContext && c.getContext('2d'));
  if(w && h && isC) cc = createContainer(w, h, el, altText);

  // waiting for image load
  el.onload = function() {
    if(!isC) return;

    w = w || el.width;
    h = h || el.height;

    // creating the container
    if (!cc) cc = createContainer(w, h, el, altText);
    con = cc.c;
    play = cc.p;
    dims = calculatePercentageDim(con, w, h, el.width, el.height);

    // add the container to the gif arraylist
    gifs.push(con);

    // listening for image click
    con.addEventListener('click', function() {
      clearTimeout(durationTimeout);
      if(!playing) {
        playing = true;
        gif = document.createElement('IMG');
        gif.setAttribute('style', 'width:' + dims.w + 'px;height:' + dims.h + 'px;');
        gif.setAttribute('data-uri', Math.floor(Math.random()*100000) + 1);
        setTimeout(function() {
          gif.src = url;
        }, 0);
        con.removeChild(play);
        con.removeChild(c);
        con.appendChild(gif);
        if(parseInt(duration) > 0) {
          durationTimeout = setTimeout(function() {
            playing = false;
            con.appendChild(play);
            con.removeChild(gif);
            con.appendChild(c);
            gif = null;
          }, duration);
        }
      } else {
        playing = false;
        con.appendChild(play);
        con.removeChild(gif);
        con.appendChild(c);
        gif = null;
      }
    });

    // canvas
    c.width = dims.w;
    c.height = dims.h;
    c.getContext('2d').drawImage(el, 0, 0, dims.w, dims.h);
    con.appendChild(c);

    // reposition the play button
    play.style.top = ((dims.h / 2) - (playSize / 2)) + 'px';
    play.style.left = ((dims.w / 2) - (playSize / 2)) + 'px';

    // setting the actual image size
    con.setAttribute('style', 'position:relative;cursor:pointer;width:' + dims.w + 'px;height:' + dims.h + 'px;background:none;border:none;padding:0;');

  }
  el.src = url;
};

return Gifffer;

});
