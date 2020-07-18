/* example jq function
$(document).ready(function(){
    alert("jquery loaded");
});*/

// retrieve id of button clicked: stackoverflow.com/questions/10291017
// then disable it and add it to an array of ids
var selected_ids = [];
$(".long-button").click(function() {
    selected_ids.push(this.id);
    //alert(this.id); // or alert($(this).attr('id'));
    $(this).prop('disabled', true);
    console.log(selected_ids);
});


function postJson(){
    var json_string = JSON.stringify(selected_ids);
    console.log(json_string);
    //https://pythonise.com/series/learning-flask/flask-and-fetch-api
    fetch(`${window.origin}/results`, {
        method: "POST",
        credentials: "include",
        body: json_string,
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
}


function postJsonDeletion(){
    var json_string = JSON.stringify(selected_ids);
    console.log(json_string);
    //https://pythonise.com/series/learning-flask/flask-and-fetch-api
    fetch(`${window.origin}/index`, {
        method: "POST",
        credentials: "include",
        body: json_string,
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
}


// Tooltips Initialization from mdbootstrap: https://mdbootstrap.com/docs/jquery/javascript/tooltips/
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})