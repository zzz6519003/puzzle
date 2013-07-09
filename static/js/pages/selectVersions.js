$(document).ready(function(){
    var selectVersion = new SelectVersion();
    selectVersion.init();
});

function SelectVersion()
{
    var body = $("body");

    this.init = function(){
        bindEvent();
        configuration();
    };

    function configuration(){
        configVersionBadge();
    }

    function cleanBadgeState(actionItem){
        actionItem.removeClass("badge-success");
        actionItem.removeClass("badge-important");
        actionItem.removeClass("badge-info");
    }

    function setBadgeStateToCurrent(actionItem){
        cleanBadgeState(actionItem);
        actionItem.addClass("badge-success");
    }

    function setBadgeStateToInitVersion(actionItem){
        cleanBadgeState(actionItem);
        actionItem.addClass("badge-info");
    }

    function setBadgeStateToOffLine(actionItem){
        cleanBadgeState(actionItem);
        actionItem.addClass("badge-important");
    }

    function setBadgeStateToDefault(actionItem){
        var isInit = (actionItem.context.dataset['isInit'] == '1')?true:false;
        var isOffLine = (actionItem.context.dataset['isOffLine'] == '1')?true:false;

        cleanBadgeState(actionItem);

        if(isInit){
            setBadgeStateToInitVersion(actionItem);
        }

        if(isOffLine){
            setBadgeStateToOffLine(actionItem);
        }
    }

    function configVersionBadge(){
        $(".J_versionBadge").each(function(index, value){
            $item = $(value);
            setBadgeStateToDefault($item);
            var isCurrent = ($item.context.dataset['isCurrent'] == '1')?true:false;

            if(isCurrent){
                setBadgeStateToCurrent($item);
            }
        });
    }

    function bindEvent(){
        body.on("click", ".J_versionBadge", function(){
            versionBadgeClicked($(this));
        });

        body.on("click", "#J_packageButton", function(){
            packageButtonClicked($(this));
        });
    }

    function packageButtonClicked(actionItem){
        var data = getDependencySha1();
        var contentHtml = getProgressContent(actionItem);
            
        //$.post("/packageBuild/buildPackage", {data:JSON.stringify(data)}).done(function(){
        //});

        $.colorbox({
            html:contentHtml,
            width:"1024px",
            onComplete:function(){
                //todo start checking for prograss bar
            },
            onClosed:function(){
                window.location.href="/project";
            },
        });
    }

    function getProgressContent(actionItem){
        var projectId = actionItem.context.dataset['projectId'];
        var category = actionItem.context.dataset['category'];
        var version = actionItem.context.dataset['version'];
        var appName = actionItem.context.dataset['appName'];
        var projectPath = actionItem.context.dataset['projectPath'];

        var type = "dailybuild"

        if(category == "7"){
            type = "dailybuild";
        }

        if(category == "8"){
            type = "rc";
        }

        var contentUrl = "/showCmdLog?"
            +"projectId="+projectId+"&"
            +"category="+category+"&"
            +"version="+version+"&"
            +"appName="+appName+"&"
            +"projectPath="+projectPath+"&"
            +"type="+type

        var contentHtml = ""
            +"<div class=\"progress progress-striped active\">"
            +"  <div class=\"bar\" style=\"width: 40%;\"></div>"
            +"</div>"
            +"<iframe src=\""+contentUrl+"\" style=\"width:100%;height:600px\"></iframe>"
            ;

        return contentHtml
    }

    function versionBadgeClicked(actionItem){
        actionItem.siblings(".J_versionBadge").each(function(index, value){
            setBadgeStateToDefault($(value));
        });
        setBadgeStateToCurrent(actionItem);
    }

    function getDependencySha1(){
        var data={};
        var dependencyArray = [];

        $(".J_versionBadge.badge-success").each(function(index, value){
            var dependency = {};
            var item = $(value);
            dependency['repoId'] = item.context.dataset['repoId'];
            dependency['sha1'] = item.context.dataset['sha1'];
            dependency['repoName'] = item.context.dataset['repoName'];
            dependencyArray.push(dependency);
        });

        if($("#J_isRelease")[0].checked){
            data['isDebug'] = false;
        }else{
            data['isDebug'] = true;
        }

        data['projectId'] = $("#J_projectInfo")[0].dataset['projectId'];
        data['category'] = $("#J_projectInfo")[0].dataset['category'];
        data['version'] = $("#J_projectInfo")[0].dataset['version'];
        data['appName'] = $("#J_projectInfo")[0].dataset['appName'];
        data['projectPath'] = $("#J_projectInfo")[0].dataset['projectPath'];

        data['dependencyArray'] = dependencyArray;

        return data;
    } 
}
