(function(){
    var body = $("body");

    body.on("click", "#J_sliceDeliverButton", function(){
        sliceDeliverButton($(this));
    });
})();

function sliceDeliverButton(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}
