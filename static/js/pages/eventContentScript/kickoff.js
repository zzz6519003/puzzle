(function(){
    var body = $("body");

    body.on("click", "#J_kickOffButton", function(){
        kickOffButtonClicked($(this));
    });
})();

function kickOffButtonClicked(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}