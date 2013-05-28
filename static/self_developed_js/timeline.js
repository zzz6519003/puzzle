$(document).ready(function(){
    alert("here i am");
    timeline = new TimeLine();
    timeline.init();
});

function TimeLine()
{
    this.init = function(){
        generateTimeLine();
        bindEvent();
    };

    function bindEvent(){
    }

    function generateTimeLine(){
       createStoryJS({
           type:"timeline",
           width:"800",
           height:"600",
           source:"static/example_json.json",
           embed_id:"J_timeline",
           debug:false
       }); 
    }
}
