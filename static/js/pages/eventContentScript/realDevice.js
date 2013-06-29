(function(){
    var body = $("body");

    body.on("click", "#J_realDeviceButton", function(){
        realDeviceButtonClicked($(this));
    });
})();

function realDeviceButtonClicked(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}
