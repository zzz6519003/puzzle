$(document).ready(function(){
    timeline = new TimeLine();
    timeline.init();
});

function TimeLine()
{
    function generateTimeLine(){
        //this is the losted timeline, but it's perfect. i'm gonna retain it for self-appreciate.:D
//        createStoryJS({
//            type:"timeline",
//            width:"1280",
//            height:"800",
//            source:"static/example_json.json",
//            embed_id:"J_timeline",
//            debug:false
//        }); 
    }

    this.init = function(){
        bindEvent();
    };

    function bindEvent(){
        $("#J_timeLine").on("click", ".J_content", function(){
            timelineEventClicked($(this));
        });

        $("#J_addEventButton").on("click", function(){
            addEvent($(this));
        });

        $("#J_deleteButton").on("click", function(){
            deleteEvent($(this));
        });
    }


    function timelineEventClicked(actionItem){
        $("#J_detail").html(actionItem.html());
        $("#J_deleteButton").attr("data-id", actionItem.attr("data-id"));
    }

    function addEvent(actionItem){
        var Template_add = $("#J_template_add").html();

        $.colorbox({
            opacity:0.5,
            html:Template_add
        });

        $("#cboxLoadedContent .J_addEventConfirmButton").on("click", function(){
            confirmToAddEvent($(this));
        });
    }

    function confirmToAddEvent(actionItem){
        var inputContent = $("#cboxLoadedContent #J_eventInputContent").val();
        var Template_event = $("#J_template_event").html();

        Template_event = Template_event.replace("___content___", inputContent);
        $("#J_timeLine").append(Template_event);

        $.colorbox.close();
    }

    function deleteEvent(actionItem){
        var data_id = actionItem.attr("data-id");
        $li = $("div[data-id="+data_id+"]").parents("li:first");
        $li.slideUp('slow', function(){
            $li.remove();
        });
    }
}
