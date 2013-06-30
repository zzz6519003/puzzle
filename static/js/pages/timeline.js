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
        var date = new Date();

        //你妹！js计算月份是从0开始算的！
        var today = date.getFullYear() + '/' + (date.getMonth()+1) + '/' + date.getDate();
        var timestamp = Date.parse(today)/1000;

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
    }

    function timelineEventClicked(actionItem){
        $(".current").removeClass("current");
        actionItem.addClass("current");

        console.log(actionItem);

        switch(actionItem.attr('data-category')){
            case '1':
                addBackLogContentIntoEventContent(actionItem);
                break;
            case '2':
                addKickOffContentIntoEventContent(actionItem);
                break;
            case '3':
                addPRDDeliverContentIntoEventContent(actionItem);
                break;
            case '4':
                addAPIFakeInterfaceContentIntoEventContent(actionItem);
                break;
            case '5':
                addAPIDeliverContentIntoEventContent(actionItem);
                break;
            case '6':
                addSliceDeliverContentIntoEventContent(actionItem);
                break;
            case '7':
                addDailyBuildContentIntoEventContent(actionItem);
                break;
            case '8':
                addRCBuildContentIntoEventContent(actionItem);
                break;
            case '9':
                addRealDeviceContentIntoEventContent(actionItem);
                break;
            case '10':
                addReleaseContentIntoEventContent(actionItem);
                break;
            default:
                warningPopout("你是怎么点进这儿的？");
                break;
        }
    }

    function addBackLogContentIntoEventContent(actionItem){
        var contentHtml = $('#J_BackLogTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }

    function addKickOffContentIntoEventContent(actionItem){
        var contentHtml = $('#J_KickOffTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }

    function addPRDDeliverContentIntoEventContent(actionItem){
        var contentHtml = $('#J_PRDDeliverTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }

    function addAPIFakeInterfaceContentIntoEventContent(actionItem){
        var contentHtml = $('#J_APIFakeInterfaceTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }

    function addAPIDeliverContentIntoEventContent(actionItem){
        var contentHtml = $('#J_APIDeliverTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }

    function addSliceDeliverContentIntoEventContent(actionItem){
        var contentHtml = $('#J_SliceDeliverTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }

    function addDailyBuildContentIntoEventContent(actionItem){
        var contentHtml = $('#J_DailyBuildTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }

    function addRCBuildContentIntoEventContent(actionItem){
        var contentHtml = $('#J_RCBuildTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }

    function addRealDeviceContentIntoEventContent(actionItem){
        var contentHtml = $('#J_RealDeviceTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }

    function addReleaseContentIntoEventContent(actionItem){
        var contentHtml = $('#J_ReleaseTemplate').html();
        var projectId = actionItem.attr("data-project-id");
        contentHtml = contentHtml.replace("__project_id__", projectId);
        $("#J_eventContent").html(contentHtml);
    }
}
