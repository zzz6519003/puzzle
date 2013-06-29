$(document).ready(function(){
    timeline = new TimeLine();
    timeline.init();
});

function TimeLine()
{
    this.init = function(){
        bindEvent();
    };

    function bindEvent(){
        $(".J_event").on('click', function(){
            timelineEventClicked($(this));
        });
    }

    function timelineEventClicked(actionItem){
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
