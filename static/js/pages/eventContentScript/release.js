(function(){
    var body = $("body");

    body.on("click", "#J_releaseButton", function(){
        releaseButtonClicked($(this));
    });
})();

function releaseButtonClicked(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}
