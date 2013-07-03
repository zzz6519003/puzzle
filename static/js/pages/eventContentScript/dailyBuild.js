(function(){
    var body = $("body");

    body.on("click", "#J_dailyBuildButton", function(){
        dailyBuildButtonClicked($(this));
    });

})();

function dailyBuildButtonClicked(actionItem){
    var projectId = actionItem.context.dataset['projectId'];
    var category = actionItem.context.dataset['category'];
    var url = "/packageBuild/selectVersions?projectId="+projectId+"&category="+category;
    window.location.href = url;
}
