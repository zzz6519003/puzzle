(function(){
    var body = $("body");

    body.on("click", "#J_backLogButton", function(){
        backLogButtonClicked($(this));
    });
})();

function backLogButtonClicked(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}
