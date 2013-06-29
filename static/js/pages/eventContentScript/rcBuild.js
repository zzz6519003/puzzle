(function(){
    var body = $("body");

    body.on("click", "#J_rcBuildButton", function(){
        rcBuildButtonClicked($(this));
    });
})();

function rcBuildButtonClicked(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}
