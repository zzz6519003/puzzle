(function(){
    var body = $("body");

    body.on("click", "#J_rcBuildButton", function(){
        rcBuildButtonClicked($(this));
    });
})();

function rcBuildButtonClicked(actionItem){
    gotoSelectVersion(actionItem);
}
