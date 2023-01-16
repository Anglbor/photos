/*
// Below can load a css file, but not before the tagger.js is loaded.
// If the tagger.js can be loaded by this script, then below can be
// used instead of needing to put it directly into the html files.

path = document.currentScript.src
cssfile = path.substr(0, path.lastIndexOf(".")) + ".css"
var link = document.createElement("link");
link.href = cssfile
link.type = "text/css";
link.rel = "stylesheet";
link.media = "screen,print";

document.getElementsByTagName( "head" )[0].appendChild( link );
*/

var tags = tagger(tags_input, {
    allow_duplicates: false,
    allow_spaces: true,
    wrap: true,
    completion: {
        list: js_alltags
    }
});

var taglist = js_tags
for (i = 0; i < taglist.length; i++) {
    console.log(taglist[i]);
    tags.add_tag(taglist[i]);
};
