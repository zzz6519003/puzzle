//记录时间给别的脚本用
var date = new Date();
//你妹！js计算月份是从0开始算的！
var today = date.getFullYear() + '/' + (date.getMonth()+1) + '/' + date.getDate();
var timestamp = Date.parse(today)/1000;

$(document).ready(function(){
    timeline = new TimeLine();
    timeline.init();
});

function TimeLine()
{
    this.init = function(){
        //confiuration 必须要在事件绑定的后面
        bindEvent();
        configuration();
    };

    function configuration(){
        setupEventContent();
        setupMileStone();
    }

    function setupEventContent(){
        $("#J_eventContent").sticky({topSpacing:100});
    }

    function setupMileStone(){

        //过去最近的事件
        var maxPastTimestamp = 0;
        var maxPastTimestampEvent = null;

        //今天是否有事件
        var isToday = false;
        var todayEvent = null;

        //未来最近的事件
        var minRecentTimestamp = 99999999999999;
        var recentEvent = null;

        $(".J_event").each(function(index, value){
            $item = $(value);
            itemTimeStamp = parseInt($item.attr("data-time"));

            if(itemTimeStamp < timestamp){
                //this is the past event
                $item.addClass("past");

                if(itemTimeStamp > maxPastTimestamp){
                    maxPastTimestamp = itemTimeStamp;
                    maxPastTimestampEvent = $item;
                }
            }

            if(itemTimeStamp > timestamp){
                //this is the future event
                if(itemTimeStamp < minRecentTimestamp){
                    minRecentTimestamp = itemTimeStamp;
                    recentEvent = $item;
                }
            }

            if(itemTimeStamp === timestamp){
                //today's event
                $item.addClass("today");
                todayEvent = $item;
                isToday = true;
            }
        });

        if(isToday){
            todayEvent.trigger("click");
        }else if(maxPastTimestampEvent != null){
            maxPastTimestampEvent.trigger("click");
        }else{
            recentEvent.trigger("click");
        }
    }

    function bindEvent(){
        $(".J_event").on('click', function(){
            timelineEventClicked($(this));
        });

        $("#J_copyProject").on('click', function(){
            copyProjectButtonClicked($(this));
        });
    }

    function copyProjectButtonClicked(actionItem){
        var projectId = actionItem.context.dataset['projectId'];
        $.post("/packageBuild/copyProject", {projectId:projectId}, function(data){
            alert(data);
        });
    }

    function timelineEventClicked(actionItem){
        $(".current").removeClass("current");
        actionItem.addClass("current");

        $.smoothScroll({
            offset:actionItem.offset().top-250,
        });

        switch(actionItem.context.dataset['category']){
            case '1':
                replaceHtml(actionItem, $('#J_BackLogTemplate').html());
                break;
            case '2':
                replaceHtml(actionItem, $('#J_KickOffTemplate').html());
                break;
            case '3':
                replaceHtml(actionItem, $('#J_PRDDeliverTemplate').html());
                break;
            case '4':
                replaceHtml(actionItem, $('#J_APIFakeInterfaceTemplate').html());
                break;
            case '5':
                replaceHtml(actionItem, $('#J_APIDeliverTemplate').html());
                break;
            case '6':
                replaceHtml(actionItem, $('#J_SliceDeliverTemplate').html());
                break;
            case '7':
                replaceHtml(actionItem, $('#J_DailyBuildTemplate').html());
                break;
            case '8':
                replaceHtml(actionItem, $('#J_RCBuildTemplate').html());
                break;
            case '9':
                replaceHtml(actionItem, $('#J_RealDeviceTemplate').html());
                break;
            case '10':
                replaceHtml(actionItem, $('#J_ReleaseTemplate').html());
                break;
            default:
                warningPopout("你是怎么点进这儿的？");
                break;
        }
    }

    function replaceHtml(actionItem, contentHtml){
        contentHtml = contentHtml.replace("__project_id__", actionItem.context.dataset['projectId']);
        contentHtml = contentHtml.replace("__category__", actionItem.context.dataset['category']);
        contentHtml = contentHtml.replace("__time__", actionItem.context.dataset['time']);
        $("#J_eventContent").html(contentHtml);
    }
}
