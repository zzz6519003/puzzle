(function(){
    var body = $("body");

    body.on("click", "#J_dailyBuildButton", function(){
        dailyBuildButtonClicked($(this));
    });

})();

function dailyBuildButtonClicked(actionItem){
    gotoSelectVersion(actionItem);
}

//this is the public function which will be called by release.js
function gotoSelectVersion(actionItem){
    var projectId = actionItem.context.dataset['projectId'];
    var category = actionItem.context.dataset['category'];
    var url = "/packageBuild/selectVersions?projectId="+projectId+"&category="+category;
    window.location.href = url;
}
