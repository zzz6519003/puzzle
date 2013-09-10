(function(){
    var body = $("body");

    body.on("click", "#J_prdDeliverButton", function(){
        prdDeliverButton($(this));
    });
})();

function prdDeliverButton(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}
