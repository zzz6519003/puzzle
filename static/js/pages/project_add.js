$(document).ready(function(){
    var addProject = new AddProject();
    addProject.init();
});

function AddProject()
{
    var body = $("body");

    this.init = function(){
        bindEvent();
    }

    function bindEvent(){

        body.on("click", ".J_addTime", function(){
            clickAddTime($(this));
        });

        body.on("click", ".J_delTime", function(){
            if($("form .J_mileStoneRow").length > 1){
                deleteTime($(this));
            }else{
                warningPopout("别赶尽杀绝啊，留一条生路嘛。");
            }
        });

        body.on("focusin", ".J_pickTime", function(){
            $(this).datepicker({
                dateFormat:"yy-mm-dd",
                inline:true
            });
        });

        body.on("mouseenter", ".J_timeRow", function(){
            hoverInTimePicker($(this));
        });

        body.on("mouseleave", ".J_timeRow", function(){
            hoverOutTimePicker($(this));
        });

        body.on("click", ".J_selectMileStone", function(){
            if($(this).children("label").length > 0){
                switchMilestoneToSelector($(this));
            }
        });

        body.on("mouseleave", ".J_selectMileStone", function(){
            if($(this).children("select").length > 0){
                switchSelectorToMilestone($(this));
            }
        });

        $("#J_submitButton").on("click", function(){
            submitButtonClicked($(this));
        });

        body.on("click", "input", function(){
            $(this).closest(".control-group").removeClass("error");
        });
    }

    function submitButtonClicked(actionItem){
        if(isAvailable()){
            var formData = generateFormData();
            formData = JSON.stringify(formData);
            $.post("/project/add", {data:formData});
            var contentHtml = ""
                +"<div class=\"progress progress-striped active\">"
                +"  <div class=\"bar\" style=\"width: 0%;\" id=\"J_progressBar\"></div>"
                +"</div>";

            $.colorbox({
                html:contentHtml,
                fastIframe:false,
                width:"1024px",
                overlayClose:false,
                escKey:false,
                closeButton:false,
                onComplete:function(){
                    progressNumberUrl = "/initProjectProgress";

                    var intervalId = setInterval(function(){
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
                                    console.log("outer " + progressNumber);
                                    $("#J_progressBar").attr("style", "width: "+progressNumber);

                                    $.post(progressNumberUrl, {data:formData},function(data){
                                        currentProgress = parseInt(currentProgress);
                                        var fetchedProgress = parseInt(data);
                                        var finallyProgress = "";

                                        if(fetchedProgress < currentProgress){
                                            finallyProgress = (currentProgress+1)+"%";
                                        }else{
                                            finallyProgress = data;
                                        }

                                        console.log("inner " + data);
                                        $("#J_progressBar").attr("style", "width: "+finallyProgress);
                                    });
                                }else{
                                    stop();
                                }
                            }
                        }
                    }, 1000);

                    function stop(){
                        clearInterval(intervalId);
                        window.location.href="/project";
                    }
                },
                onClosed:function(){
                    window.location.href="/project";
                }
            });
        }
    }

    function deleteTime(actionItem){
        actionItem.closest(".J_mileStoneRow").slideUp("slow", function(){
            $(this).remove();
        });
    }

    function clickAddTime(actionItem){
        var milestoneHTML = $("#J_milestoneTemplate").html();
        actionItem.closest(".J_mileStoneRow").after(milestoneHTML);
    }

    function hoverInTimePicker(actionItem){
        actionItem.children(".J_operations").removeClass("hide");
    }

    function hoverOutTimePicker(actionItem){
        actionItem.children(".J_operations").addClass("hide");
    }

    function switchMilestoneToSelector(actionItem){
        var selectorHtml = $("#J_selectorTemplate").html();
        actionItem.html(selectorHtml);
    }

    function switchSelectorToMilestone(actionItem){
        var selector = actionItem.children("select");
        var datePicker = actionItem.closest(".J_mileStoneRow").find(".J_pickTime");

        var selectedValue = selector.val();
        var selectedOption = actionItem.find("option:selected");

        var replacedHtml = "<label><font color=\"pink\">"+selectedOption.text()+":</font></label>";
        datePicker.attr("data-type", selectedValue);

        actionItem.html(replacedHtml);
    }

    function generateFormData(){
        var data = {
            eventList:[]
        };

        $("form .J_formData").each(function(index, value){
            var item = {};
            var type = $(value).attr('data-type');
            var value = $(value).val();

            if(isNaN(type)){
                data[type] = value;
            }else{
                item[type] = value;
                data.eventList.push(item);
            }
        });

        data['openXcode'] = $("#J_openXcode")[0].checked;

        data['whoami'] = $.cookie("puzzleUsername");
        data['clienProjectPath'] = $.cookie("puzzleProjectPath");

        if(typeof(data['whoami']) == "undefined" || typeof(data['projectPath']) == "undefined"){
            console.log("no username and project path");
            warningPopout("去时间轴那儿设置用户名和项目路径去，赶紧的。");
            return false;
        }

        return data;
    }

    function isAvailable(data){
        var result = true;

        $("form .control-group").each(function(index, value){
            item = $(value);
            formData = item.find(".J_formData");

            if(typeof formData.val() != "undefined"){
                if(formData.val().length == 0){
                    item.addClass('error');
                    result = false;
                }
            }
        });

        if(typeof($.cookie("puzzleUsername")) == "undefined" || typeof($.cookie("puzzleProjectPath")) == "undefined"){
            console.log("no username and project path");
            warningPopout("去时间轴那儿设置用户名和项目路径去，赶紧的。");
            return false;
        }

        return result;
    }
}
