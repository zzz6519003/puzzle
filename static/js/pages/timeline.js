
$(document).ready(function(){
    timeline = new TimeLine();
    timeline.init();
});

function TimeLine()
{
    var body = $("body");

    this.init = function(){
        //confiuration 必须要在事件绑定的后面
        bindEvent();
        configuration();
    };

    function configuration(){
        setupButtons();
        setupEventContent();
        setupMileStone();
    }

    function setupButtons(){
        $("#J_buttons").sticky({topSpacing:100, width:'1300px'});
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
        body.on('click', '.J_event', function(){
            timelineEventClicked($(this));
        });

        body.on('click', '#J_copyProject', function(){
            copyProjectButtonClicked($(this));
        });

    }

    function copyProjectButtonClicked(actionItem){
        var data = {
            projectId:actionItem.context.dataset['projectId'],
            whoami:$.cookie("puzzleUsername"),
            clientProjectPath:$.cookie("puzzleProjectPath")
        };

        if(typeof(data['whoami']) != "undefined" && typeof(data['clientProjectPath']) != "undefined"){
            var originHtml = actionItem[0].outerHTML;
            var contentHtml = "<img src=\"/static/img/waiting.gif\" id=\"J_waiting\">";
            actionItem[0].outerHTML = contentHtml;
            $.post("/packageBuild/copyProject", {data:JSON.stringify(data)}, function(data){
                $("#J_waiting")[0].outerHTML = originHtml;
            });
        }else{
            warningPopout("不知道你是谁，也不知道你要把项目放在哪儿。");
        }
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
        contentHtml = contentHtml.replace(/__project_id__/g, actionItem.context.dataset['projectId']);
        contentHtml = contentHtml.replace(/__category__/g, actionItem.context.dataset['category']);
        contentHtml = contentHtml.replace(/__time__/g, actionItem.context.dataset['time']);
        $("#J_eventContent").html(contentHtml);
    }
}
