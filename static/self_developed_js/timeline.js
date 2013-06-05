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
        $(".J_content").on("click", function(){
            timelineEventClicked($(this));
        });

        $("#J_addEventButton").on("click", function(){
            addEvent($(this));
        });
    }


    function timelineEventClicked(actionItem){
        $("#J_detail").html(actionItem.html());
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
}
