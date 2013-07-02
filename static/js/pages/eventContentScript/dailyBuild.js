(function(){
    var body = $("body");

    body.on("click", "#J_dailyBuildButton", function(){
        dailyBuildButtonClicked($(this));
    });

})();

function dailyBuildButtonClicked(actionItem){
    alert("project id is "+actionItem.attr("data-project-id"));
}

function DailyBuild()
{
    this.init = function(){
    }
}
