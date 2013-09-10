(function(){
    var body = $("body");

    body.on("click", "#J_apiDeliverButton", function(){
        apiDeliverButtonClicked($(this));
    });
})();

function apiDeliverButtonClicked(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}
