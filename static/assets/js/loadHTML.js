// loadHTML.js
// quick hack for temp header / footer injection for boostrap template
// M A Chatterjee Jan 2023


let fn = function getFile(fname,cb) {
   var x = new XMLHttpRequest();
   x.overrideMimeType("application/json");
   x.open("GET", fname, true); 
   x.onreadystatechange = 
      function () {if (x.readyState == 4 && x.status == "200") {cb(x.responseText);}};
   x.send(null);
}
fn("header.html", (x)=>  document.getElementsByTagName("header")[0].innerHTML = x);
fn("footer.html", (x)=>  document.getElementsByTagName("footer")[0].innerHTML = x);
