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
        configCheckBox();
    }

    function configCheckBox(){
        $(".J_channelBox").each(function(index, value){
            item = $(value);
            if(item.val() == "A00" || item.val() == "A01" || item.val() == "A02" || item.val() == "A08"){
                item[0].checked = true;
            }
        });
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
        var dependencyId = actionItem.context.dataset['repoId'];

        cleanBadgeState(actionItem);

        if(isInit){
            $(".J_versionOption[data-dependency-id="+dependencyId+"]").attr("data-init-sha1", actionItem.context.dataset['sha1']);
            setBadgeStateToInitVersion(actionItem);
        }

        if(isOffLine){
            setBadgeStateToOffLine(actionItem);
        }
    }

    function configVersionBadge(){
        $(".J_versionBadge").tinyTips({
            content: function(actionItem){
                var commit = actionItem.context.dataset['commit'];
                return commit;
            },
            position: 'top',
            spacing: 8,
            transition: 'fade',
            arrow: true,
            arrowColor: 'rgba(0, 0, 0, 0.8)'
        });

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

        body.on("click", "#J_inputCommitButton", function(){
            inputCommitButtonClicked($(this));
        });

        body.on("click", "#J_packageButton", function(){
            packageButtonClicked($(this));
        });

        body.on("click", ".J_channelBox", function(){
            channelBoxChanged($(this));
        });

        body.on("change", ".J_selectDependencyType", function(){
            dependencyTypeSelected($(this));
        });
    }

    function dependencyTypeSelected(actionItem){

        var projectId = parseInt($("#J_projectInfo").attr('data-project-id'));
        var dependencyType = parseInt(actionItem.val());
        var dependencyId = parseInt(actionItem.attr('data-dependency-id'));
        var initSHA1 = actionItem[0].selectedOptions[0].dataset['initSha1'];

        console.log(actionItem);

        var data = {
            projectId : projectId,
            dependencyType : dependencyType,
            dependencyId : dependencyId,
            initSHA1 : initSHA1
        };

        var postData = $.toJSON(data);

        $.post("/packageBuild/selectVersions", {data:postData}, function(fetchedData){
            var versionBadgeHtml = "";

            $.each(fetchedData, function(index, value){
                versionBadgeHtml +=
                '<a'
                +'  data-repo-id="'+value.dependency.id+'"'
                +'  data-repo-name="'+value.dependency.dependency_name+'"'
                +'  data-sha1="'+value.hash+'"'
                +'  data-type="'+value.type+'"'
                +'  data-is-current="'+value.isCurrent+'"'
                +'  data-is-init="'+value.isInit+'"'
                +'  data-is-off-line="'+value.isOffLine+'"'
                +'  data-commit="'+value.commit+'"'
                +'  class="J_versionBadge badge"'
                +'>'+value.versionName+'</a>&nbsp;';
            });

            var badgeTd = actionItem.closest("tr").find("td").get(2);
            $(badgeTd).html(versionBadgeHtml);

            configVersionBadge();
        },"json");
    }

    function channelBoxChanged(actionItem){
        if($(".J_channelBox:checked").length == 0){
            actionItem[0].checked = true;
        }
    }

    function packageButtonClicked(actionItem){
        var data = getDependencySha1();
        var intervalId = 0;
        if(data){
            var contentHtml = getContentHtml(actionItem);
            $.colorbox({
                html:contentHtml,
                fastIframe:false,
                width:"1024px",
                onComplete:function(){

                    var jsonData = $.toJSON(data);
                    $.post("/packageBuild/buildPackage", {data:jsonData});

                    progressNumberUrl = getContentUrl(actionItem, "/progressNumber");

                    intervalId = setInterval(function(){

                        var progressBar = $("#J_progressBar");
                        var currentProgress = progressBar.attr("style");

                        if(typeof currentProgress == "undefined"){
                            stop();
                        }else{
                            currentProgress = currentProgress.match(/\d+/);
                            if(currentProgress){
                                currentProgress = currentProgress[0];
                            }else{
                                stop();
                            }

                            if(isNaN(currentProgress)){
                                stop();
                            }else{
                                if(currentProgress != 100){
                                    currentProgress = parseInt(currentProgress)+1;
                                    progressNumber = currentProgress + "%";
                                    $("#J_progressBar").attr("style", "width: "+progressNumber);

                                    $.get(progressNumberUrl, function(data){

                                        currentProgress = parseInt(currentProgress);
                                        var fetchedProgress = parseInt(data);
                                        var finallyProgress = "";

                                        if(fetchedProgress < currentProgress){
                                            finallyProgress = (currentProgress+1)+"%";
                                        }else{
                                            finallyProgress = data;
                                        }
                                        $("#J_progressBar").attr("style", "width: "+finallyProgress);
                                    });
                                }
                            }
                        }
                    }, 2000);

                    function stop(){
                        //$.colorbox.close();
                        //clearInterval(intervalId);
                    }

                },
                onClosed:function(){
                    $.colorbox.close();
                    clearInterval(intervalId);
                    window.location.href="/project";
                },
            });
        }else{
            alert("看右边");
        }
    }

    function returnTipContent(actionItem){
        var content = actionItem.context.dataset['commit'];
        return content;
    }

    function getPackageData(actionItem){
        var data = {};
        data['projectId'] = actionItem.context.dataset['projectId'];
        data['category'] = actionItem.context.dataset['category'];
        data['version'] = actionItem.context.dataset['version'];
        data['appName'] = actionItem.context.dataset['appName'];
        data['projectPath'] = actionItem.context.dataset['projectPath'];

        var type = "dailybuild"

        if(data['category'] == "7"){
           type = "dailybuild";
        }

        if(data['category'] == "8"){
            type = "rc";
        }
        data['type'] = type;

        return data;
    }

    function inputCommitButtonClicked(actionItem){
        data = getPackageData(actionItem);

        $.colorbox({
            href:"/packageBuild/inputCommit",
            closeButton:false,
            overlayClose:false,
            onClosed:function(){
                window.location.href="/project";
            },
            data:{data:JSON.stringify(data)}
        });
    }

    function getContentHtml(actionItem){
        var contentUrl = getContentUrl(actionItem, "/showCmdLog");

        var contentHtml = ""
            +"<div class=\"progress progress-striped active\">"
            +"  <div class=\"bar\" style=\"width: 0%;\" id=\"J_progressBar\"></div>"
            +"</div>"
            +"<iframe src=\""+contentUrl+"\" style=\"width:100%;height:600px\"></iframe>"
            ;

        return contentHtml
    }

    function getContentUrl(actionItem, baseUrl){
        data = getPackageData(actionItem)

        var contentUrl = baseUrl
            +"?projectId="+data['projectId']+"&"
            +"category="+data['category']+"&"
            +"version="+data['version']+"&"
            +"appName="+data['appName']+"&"
            +"projectPath="+data['projectPath']+"&"
            +"type="+data['type']

        return contentUrl;
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
        data['mailContent'] = $("#cboxLoadedContent #J_mailContent").val();

        data['dependencyArray'] = dependencyArray;

        data['channelIdList'] = [];
        $(".J_channelBox:checked").each(function(index, value){
            data['channelIdList'].push($(value).val());
        });

        console.log(data);

        return data;
    } 
}
