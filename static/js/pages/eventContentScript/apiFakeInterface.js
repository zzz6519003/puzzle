(function(){
    var body = $("body");

    body.on("click", "#J_apiFakeInterfaceButton", function(){
        apiFakeInterfaceButtonClicked($(this));
    });
})();

function apiFakeInterfaceButtonClicked(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}
