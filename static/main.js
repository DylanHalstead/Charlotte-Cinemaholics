"use strict";
const $ = selector => document.querySelector(selector);

document.addEventListener("DOMContentLoaded", () => {

    checkForTitleWrap();

})

function checkForTitleWrap() {
    if($(".movie-title-sm").innerHTML.length < 25)
    {
        $("movie-card-content-sm").style.setProperty("margin-top", "400px");
    }
}